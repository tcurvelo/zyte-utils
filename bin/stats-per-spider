#!/usr/bin/env python

from datetime import datetime, timedelta

import typer

from zyte_utils import cli, misc

app = typer.Typer()


@app.command()
def main(
    stat: str = typer.Argument("item_scraped_count"),
    start: datetime = typer.Option(misc.now() - timedelta(days=30)),
    end: datetime = typer.Option(misc.now()),
    shub_file: str = typer.Option("scrapinghub.yml"),
    csv: bool = typer.Option(False),
    output: str = typer.Option("output.csv"),
):
    extractor = cli.stat_extractor(stat)
    cli.stats_command(stat, start, end, shub_file, csv, output, extractor)


if __name__ == "__main__":
    app()
