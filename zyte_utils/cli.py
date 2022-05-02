from collections import defaultdict
from datetime import datetime
from typing import Callable, Dict

import pandas as pd
import typer
from scrapinghub.client.projects import Project

from zyte_utils import dash, project

client = dash.get_shub_client()


def echo_df(df):
    typer.echo(df.to_string(index=False, na_rep="-"))


def get_stats_from_period(
    start: datetime,
    end: datetime,
    extract_stat: Callable[[Project, dict], int],
    project_file: str = None,
) -> Dict[str, int]:
    startts = int(start.timestamp() * 1000)
    endts = int(end.timestamp() * 1000)

    total = defaultdict(int)

    for proj_id in project.get_ids(project_file):
        proj = client.get_project(proj_id)
        jobs = dash.get_jobs_from_timespan(proj, startts, endts)
        with typer.progressbar(jobs, label=f"Getting jobs from {proj_id}") as progress:
            for job_summary in progress:
                total[job_summary["spider"]] += extract_stat(proj, job_summary)
    return total


def stat_extractor(stat) -> int:
    def extractor(project, job_summary):
        # look up for the stat in the summary before requesting for the job
        if not (result := job_summary.get(stat)):
            stats = project.jobs.get(job_summary["key"]).metadata.get("scrapystats", {})
            result = stats.get(stat, 0)
        return result

    return extractor


def stats_command(
    stat: str,
    start: datetime,
    end: datetime,
    shub_file: str,
    output: str,
    extractor,
):
    total = get_stats_from_period(start, end, extractor, shub_file)
    df = pd.DataFrame(total.items(), columns=["spider", stat])

    if output:
        file_output = output.format(start=start, end=end)
        df.to_csv(file_output, index=False)
        typer.echo(f"Wrote {file_output}", err=True)
    else:
        echo_df(df)
