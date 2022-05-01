import logging

from scrapinghub import ScrapinghubClient

logger = logging.getLogger(__name__)


def get_shub_client():
    return ScrapinghubClient(connection_timeout=180, use_msgpack=True)


def get_jobs_from_timespan(resource, startts, endts, **kwargs):
    step = 1000
    count = offset = 0
    done = False

    while not done:
        for count, job in enumerate(
            resource.jobs.iter(start=offset, startts=startts, **kwargs), 1
        ):
            if "running_time" not in job or job["running_time"] > endts:
                continue
            yield job

        if not (done := count < step):
            offset += step
