#!/usr/bin/env python
import os
import re
from collections import defaultdict
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import pandas as pd
import typer
from scrapinghub.client.projects import Project
from yaml import Loader, load

from zyte_tools.dash import get_jobs_from_timespan, get_shub_client
from zyte_tools.utils import now

client = get_shub_client()

crawlera_stats_re = re.compile(
    r"crawlera/response/status/(\d+(?!403|407|408|429|502|503|504|999))"
)


app = typer.Typer()


def get_projects() -> List[str]:
    filename = "scrapinghub.yml"
    previous = None
    folder = Path(os.getcwd())

    # search for the file in the current folder or its parents
    while not (proj_file := folder / filename).exists() and folder != previous:
        previous = folder
        folder = folder.parent

    if folder == previous:
        raise FileNotFoundError(f"Could not find {filename}")

    with open(proj_file, "r") as zyte_file:
        zyte_config = load(zyte_file, Loader=Loader)
    projects_ids = {p["id"] for p in zyte_config.get("projects").values()}
    return projects_ids


def get_stats_from_period(
    start: datetime,
    end: datetime,
    extract_stat: Callable[[Project, dict], int],
) -> Dict[str, int]:
    startts = int(start.timestamp() * 1000)
    endts = int(end.timestamp() * 1000)

    total = defaultdict(int)

    for proj_id in get_projects():
        project = client.get_project(proj_id)
        jobs = get_jobs_from_timespan(project, startts, endts)
        with typer.progressbar(jobs, label=f"Getting jobs from {proj_id}") as progress:
            for job_summary in progress:
                total[job_summary["spider"]] += extract_stat(project, job_summary)
    return total


def _requests_extractor(project, job_summary) -> int:
    stats = project.jobs.get(job_summary["key"]).metadata.get("scrapystats") or {}
    return sum(v for k, v in stats.items() if crawlera_stats_re.search(k))


def _objects_extractor(project, job_summary) -> int:
    stats = project.jobs.get(job_summary["key"]).metadata.get("scrapystats") or {}
    return stats.get("objects", 0)


# class Command:
#     def __init__(self, stat, extractor=None):
#         self._stat_name = stat

#     def __call__(
#         self,
#         start: datetime = now(),
#         end: datetime = now() - timedelta(days=30),
#         output: str = "spm_requests_{start}_{end}.csv",
#     ):
#         total = self.get_stats(start, end)
#         df = pd.DataFrame(requests.items(), columns=["spider", self._stat_name])
#         df.to_csv(output.format(start=start, end=end), index=False)


# requests = Command(stat="requests", extractor=)


@app.command()
def requests(
    start: datetime = now(),
    end: datetime = now() - timedelta(days=30),
    output: str = "spm_requests_{start}_{end}.csv",
):
    requests = get_stats_from_period(start, end, _requests_extractor)
    df = pd.DataFrame(requests.items(), columns=["spider", "requests"])
    df.to_csv(output.format(start=start, end=end), index=False)


@app.command()
def items(
    start: datetime = now(),
    end: datetime = now() - timedelta(days=30),
    output: str = "items_{start}_{end}.csv",
):
    total = get_stats_from_period(start, end, lambda _, j: j.get("items", 0))
    df = pd.DataFrame(total.items(), columns=["spider", "items"])
    df.to_csv(output.format(start=start, end=end), index=False)


@app.command()
def objects(
    start: datetime = now(),
    end: datetime = now() - timedelta(days=30),
    output: str = "objects_{start}_{end}.csv",
):
    total = get_stats_from_period(start, end, _objects_extractor)
    df = pd.DataFrame(total.items(), columns=["spider", "objects"])
    df.to_csv(output.format(start=start, end=end), index=False)


if __name__ == "__main__":
    app()
