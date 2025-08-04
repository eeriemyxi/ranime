import math
import random

import click
from term_image.image import from_url

from ranime import (CACHE_PATH, display_anime_info, fetch_anilist_cover_image,
                    get_randomeanime_page)


@click.command(
    help="Find random anime from https://randomanime.org",
    epilog="Source code: https://github.com/eeriemyxi/ranime",
)
@click.option("--auth-key", "-a", default=None)
@click.option("--id", "-i", default=None)
def main(auth_key: str, id: str):
    path = CACHE_PATH / "auth_key"
    if not auth_key:
        try:
            auth_key = path.read_text()
        except FileNotFoundError:
            print(
                f"ERROR: --auth-key was not provided but {path} doesn't exist yet either.\n\nTIP: Run ranime with --auth-key at least once."
            )
            exit(1)
    else:
        with open(path, "w") as file:
            file.write(auth_key)

    path = CACHE_PATH / "id"
    if not id:
        try:
            id = path.read_text()
        except FileNotFoundError:
            print(
                f"ERROR: --id was not provided but {path} doesn't exist yet either.\n\nTIP: Run ranime with --id at least once."
            )
            exit(1)
    else:
        with open(path, "w") as file:
            file.write(id)

    page_amnt = get_randomeanime_page(auth_key=auth_key, id=id, page=1).json()[
        "resultsTotal"
    ]
    random_page = random.randint(1, math.floor(page_amnt / 50))

    anime = random.choice(
        get_randomeanime_page(auth_key=auth_key, id=id, page=random_page).json()[
            "results"
        ]
    )
    image_url = fetch_anilist_cover_image(anime["ani_list_id"])

    from_url(image_url).draw()
    display_anime_info(anime)
