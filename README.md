# Zyte Utils

Yet another bunch of cli utilities for Zyte's Scrapy Cloud.

## Scripts

### `stats-per-spider`

Collect a given _stat_ from all projects listed in `scrapinghub.yml`, and group them by spider:

    ❯ stats-per-spider "links/pages" \
        --shub-file="my_awesome_project/scrapinghub.yml" \
        --start 2022-01-01 --end 2022-02-01 \
        --output="page_count_jan22.csv"

It can be specially useful to keep track of custom stats along the time, such as product categories, pagination requests, etc.

### `requests-per-spider`

Do the same than before, but count for chargeable SPM/Crawlera responses.

    ❯ requests-per-spider --start 2022-01-01 --output="requests_feb.csv"

It counts all responses with status not in `[403, 407, 408, 429, 502, 503, 504, 999]`
