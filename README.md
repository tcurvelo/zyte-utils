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

### `spiders-health`

Compile the last run status for all spiders, from the projects listed in `scrapinghub.yml`.

    ❯ spiders-health --shub-file="my_awesome_project/scrapinghub.yml"
         spider  project  id                  last_run last_item_count last_error_count
        bar.org     1234 137 2022-04-30 11:34:50+00:00            18.0                -
        baz.com     5678  47 2021-06-10 14:57:54+00:00               -             47.0
        foo.com     1234 138 2022-04-30 05:56:46+00:00               -              1.0
