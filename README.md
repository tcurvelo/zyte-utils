# Zyte Utils

Yet another bunch of cli utilities for Zyte's Scrapy Cloud.

## Scripts

- `stats-per-spider`

Collect stats from all projects listed in `scrapinhub.yml`, and group them by spider:

    ./bin/stats-per-spider "links/pages" \
        --start 2022-01-01 --end 2022-02-01 \
        --shub-file="my_awesome_project/scrapinghub.yml" \
        --csv --output="page_count_jan22.csv"

- `requests-per-spider`

Do the same but for count for valid (aka. chargeable) SPM/Crawlera response codes

    ./bin/requests-per-spider.py
        --start 2022-01-01 --end 2022-02-01 \
        --csv --output="requests_feb.py"
