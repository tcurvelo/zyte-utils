import os
from pathlib import Path
from typing import List

from yaml import Loader, load


def find_project_file(folder: Path = Path(os.getcwd()), filename="scrapinghub.yml"):
    previous = None
    # search for the file in the current folder or its parents
    while not (proj_file := folder / filename).exists() and folder != previous:
        previous = folder
        folder = folder.parent

    if folder == previous:
        raise FileNotFoundError(f"Could not find {filename}")

    return proj_file


def get_ids(projects_file=None) -> List[str]:
    projects_file = projects_file or find_project_file()
    with open(projects_file, "r") as zyte_file:
        zyte_config = load(zyte_file, Loader=Loader)
    projects_ids = {p.get("id") for p in zyte_config.get("projects").values()}
    return projects_ids
