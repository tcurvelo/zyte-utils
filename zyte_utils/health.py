import os
from collections import defaultdict
from functools import reduce

import httpx
from dateutil.parser import parse
from jmespath import search as jmes

from zyte_utils import project


def get_session():
    if not (apikey := os.environ.get("SH_APIKEY")):
        raise ValueError("SH_APIKEY environment variable must be set")
    return httpx.Client(auth=(apikey, ""))


def make_project_status_url(project_id, page=1):
    return (
        f"https://app.scrapinghub.com/api/v2/projects/{project_id}/spiders"
        f"?archived=false&ordering=-last_run&page={page}&page_size=100&search="
    )


def fetch_all_spiders_from_project(session, project_id):
    next_url = make_project_status_url(project_id)

    while next_url:
        result = session.get(next_url).json()
        yield from jmes(
            """
            results[].{
                spider: name,
                project: project.id,
                id: jobq_id,
                last_run: last_run,
                last_item_count: last_item_count,
                last_error_count: last_error_count
            }
         """,
            result,
        )
        next_url = result.get("next", False)


def fetch_all_spiders_from_all_projects(projects_file=None):
    session = get_session()
    spiders = [
        spider
        for proj_id in project.get_ids(projects_file)
        for spider in fetch_all_spiders_from_project(session, proj_id)
    ]
    return reduce(_update_last_job, spiders, defaultdict(dict))


def _update_last_job(last_jobs, job):
    last_run = parse(job["last_run"]) if job["last_run"] else None
    if not (previous_run := last_jobs[job["spider"]].get("last_run")) or (
        last_run and last_run > previous_run
    ):
        last_jobs[job["spider"]] = {**job, "last_run": last_run}
    return last_jobs


if __name__ == "__main__":
    import sys

    import pandas as pd

    df = pd.DataFrame(fetch_all_spiders_from_all_projects(sys.argv[1]).values())
    print(df.to_string(index=False))
