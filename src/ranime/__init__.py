import functools
import hashlib
import html
import os
import pathlib
import pickle
import time

import requests
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

CACHE_PATH = pathlib.Path(
    os.environ.get("CACHE_PATH") or pathlib.Path.home() / ".cache/ranime/"
)
CACHE_PATH.mkdir(exist_ok=True)


def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def cache_call(path: pathlib.Path, expiry: int, args_to_cache: list):
    assert len(args_to_cache) > 0, "Can't make a cache file for that amount of args"

    def decorator(func):
        key_name = func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            assert len(kwargs) > 0, "Can't make a cache file for that amount of args"
            args_c = "+".join(str(kwargs[a]) for a in args_to_cache)
            args_hash = sha256_hash(args_c)
            result_file_path = CACHE_PATH / key_name / args_hash

            if result_file_path.is_file():
                with open(result_file_path, "rb") as file:
                    data = pickle.load(file)
                    if not time.time() > data["expiry"]:
                        return data["result"]

            result = func(*args, **kwargs)

            result_file_path.parent.mkdir(exist_ok=True)
            with open(result_file_path, "wb") as file:
                pickle.dump(dict(result=result, expiry=int(time.time()) + expiry), file)

            return result

        return wrapper

    return decorator


@cache_call(CACHE_PATH, 31200, ["id", "page"])
def get_randomeanime_page(*, auth_key: str, id: str, page: int = 1):
    response = requests.get(
        "https://www.randomanime.org/api/list/custom",
        params=dict(id=id, page=page),
        headers=dict(authorization=auth_key),
    )
    return response


def fetch_anilist_cover_image(anilist_id: int) -> str:
    """
    Fetches the cover image URL for an anime using AniList GraphQL API.
    Returns the image URL as a string.
    """
    url = "https://graphql.anilist.co"
    query = """
    query ($id: Int) {
      Media(id: $id, type: ANIME) {
        coverImage {
          extraLarge
          large
          medium
        }
      }
    }
    """
    variables = {"id": anilist_id}

    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        response.raise_for_status()
        data = response.json()
        image_url = data["data"]["Media"]["coverImage"]["extraLarge"]
        return image_url
    except Exception as e:
        print(f"[!] Error fetching image: {e}")
        return None


def display_anime_info(data: dict):
    console = Console()

    # Header Panel with Title
    title = data["name"]
    header_text = Text(f"{title}", style="bold magenta")
    if data["english_name"]:
        header_text.append(f" ({data['english_name']})", style="dim")

    console.print(Align.center(Panel(header_text, style="bold magenta", expand=False)))

    # Description Panel
    description = html.unescape(data["description"].replace("<br/>", "\n"))
    console.print(
        Align.center(
            Panel(
                description,
                title="Description",
                title_align="left",
                box=box.ROUNDED,
                expand=False,
            )
        )
    )

    # Info Table
    info_table = Table(title="Info", show_header=False, box=box.SIMPLE)
    info_table.add_row("Episodes", data["episodes"])
    info_table.add_row("Episode Duration", f"{data['episode_duration']} min")
    info_table.add_row("Release Date", data["release_date"])
    info_table.add_row("Rating", data["tv_rating"])
    info_table.add_row("Source", data["source"])
    info_table.add_row("Genres", ", ".join(data["genres"]))
    if data.get("tags"):
        info_table.add_row("Tags", ", ".join(data["tags"]))
    if data.get("ani_list_score") or data.get("my_anime_list_score"):
        scores = []
        if data.get("ani_list_score"):
            scores.append(f"AniList: {data['ani_list_score']}")
        if data.get("my_anime_list_score"):
            scores.append(f"MyAnimeList: {data['my_anime_list_score']}")
        info_table.add_row("Scores", " | ".join(scores))

    console.print(Align.center(info_table))

    # Streaming Links Table
    if data.get("links"):
        links_table = Table(
            title="Watch Links",
            show_header=True,
            header_style="bold cyan",
            box=box.SIMPLE,
        )
        links_table.add_column("Platform")
        links_table.add_column("Audio")
        links_table.add_column("URL")

        for link in data["links"]:
            audio = ", ".join(link["audio"]) if link.get("audio") else "N/A"
            links_table.add_row(link["name"], audio, link["url"])

        console.print(Align.center(links_table))

    # Anime List Links
    mal_url = (
        f"https://myanimelist.net/anime/{data['my_anime_list_id']}"
        if data.get("my_anime_list_id")
        else None
    )
    anilist_url = (
        f"https://anilist.co/anime/{data['ani_list_id']}"
        if data.get("ani_list_id")
        else None
    )

    if mal_url or anilist_url:
        list_table = Table(
            title="Anime Database Links",
            show_header=True,
            header_style="bold blue",
            box=box.SIMPLE,
        )
        list_table.add_column("Site")
        list_table.add_column("URL")

        if mal_url:
            list_table.add_row("MyAnimeList", mal_url)
        if anilist_url:
            list_table.add_row("AniList", anilist_url)

        console.print(Align.center(list_table))

    # Optional Trailer
    if data.get("trailer"):
        console.print(
            Align.center(
                Panel(
                    f"Trailer: https://youtu.be/{data['trailer']}",
                    style="green",
                    expand=False,
                )
            )
        )
