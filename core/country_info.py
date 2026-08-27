from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parents[1]

COUNTRY_INFO_DIR = (
    BASE_DIR
    / "data"
    / "country_info"
)


def load_country_info(country):

    filename = (
        country
        .replace("/", "_")
        .replace("\\", "_")
        .strip()
    )

    candidates = [

        COUNTRY_INFO_DIR
        / f"{filename}.json",

        COUNTRY_INFO_DIR
        / f"{filename.replace(' ', '_')}.json"
    ]

    for path in candidates:

        if path.exists():

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                if isinstance(data, dict):
                    return data

                return {
                    "description": str(data)
                }

            except (
                OSError,
                json.JSONDecodeError
            ):

                return {}

    return {}