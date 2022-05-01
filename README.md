# Zyte Utils

Yet another bunch of cli utilities for Zyte's Scrapy Cloud.

## Scripts

- `stats-per-spider`

Collect stats from all projects listed in `scrapinghub.yml`, and group them by spider:

    ❯ stats-per-spider "links/pages" \
        --shub-file="my_awesome_project/scrapinghub.yml" \
        --start 2022-01-01 --end 2022-02-01 \
        --output="page_count_jan22.csv"

- `requests-per-spider`

Do the same but count for valid (aka. chargeable) SPM/Crawlera response codes

    ❯ requests-per-spider --start 2022-01-01 --output="requests_feb.csv"
