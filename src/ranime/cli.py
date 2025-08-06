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
@click.option("--auth-key", "-a", default=None, help="Authentication token")
@click.option("--id", "-i", default=None, help="ID of the generated list from randomanime.org")
@click.option("--preset-name", "-p", default=None, help="Name of the preset to save --auth-key and --id under")
def main(auth_key: str, id: str, preset_name: str):
    def load_or_save(name: str, flag_name: str, value: str, tip: str):
        path = CACHE_PATH / name
        if not value:
            try:
                value = path.read_text()
            except FileNotFoundError:
                print(
                    f"ERROR: --{flag_name} was not provided but {path} doesn't exist yet either.\n\nTIP: {tip}"
                )
                exit(1)
        else:
            path.write_text(value)
        return value

    preset_name = load_or_save("active_preset", "preset-name", preset_name, "Run ranime with --preset-name at least once.")
    auth_key = load_or_save(f"{preset_name}_auth_key", "auth-key", auth_key, "Run ranime with --auth-key at least once.")
    id = load_or_save(f"{preset_name}_id", "id", id, "Run ranime with --id at least once.")

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
