#!/usr/bin/env python

import re
from datetime import datetime, timedelta

import typer

from zyte_utils import cli, misc

crawlera_valid_status_re = re.compile(
    r"crawlera/response/status/(\d+(?!403|407|408|429|502|503|504|999))"
)
app = typer.Typer()


def requests_extractor(project, job_summary) -> int:
    stats = project.jobs.get(job_summary["key"]).metadata.get("scrapystats") or {}
    return sum(v for k, v in stats.items() if crawlera_valid_status_re.search(k))


@app.command()
def main(
    start: datetime = typer.Option(misc.now() - timedelta(days=30)),
    end: datetime = typer.Option(misc.now()),
    shub_file: str = typer.Option("scrapinghub.yml"),
    csv: bool = typer.Option(False),
    output: str = typer.Option("output.csv"),
):
    cli.stats_command(
        "requests",
        start,
        end,
        shub_file,
        csv,
        output,
        requests_extractor,
    )


if __name__ == "__main__":
    app()
