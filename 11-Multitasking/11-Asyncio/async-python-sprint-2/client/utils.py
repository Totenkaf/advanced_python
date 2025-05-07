# Copyright (c) 2023 Artem Ustsov


ERR_MESSAGE_TEMPLATE = "Unexpected error: {error} for {url}"
CITIES = {
    "MOSCOW": "https://code.s3.yandex.net/async-module/moscow-response.json",
    "PARIS": "https://code.s3.yandex.net/async-module/paris-response.json",
    "LONDON": "https://code.s3.yandex.net/async-module/london-response.json",
    "BERLIN": "https://code.s3.yandex.net/async-module/berlin-response.json",
    "BEIJING": "https://code.s3.yandex.net/async-module/beijing-response.json",
    "KAZAN": "https://code.s3.yandex.net/async-module/kazan-response.json",
    "SPETERSBURG": "https://code.s3.yandex.net/async-module/spetersburg-response.json",
    "VOLGOGRAD": "https://code.s3.yandex.net/async-module/volgograd-response.json",
    "NOVOSIBIRSK": "https://code.s3.yandex.net/async-module/novosibirsk-response.json",
    "KALININGRAD": "https://code.s3.yandex.net/async-module/kaliningrad-response.json",
    "ABUDHABI": "https://code.s3.yandex.net/async-module/abudhabi-response.json",
    "WARSZAWA": "https://code.s3.yandex.net/async-module/warszawa-response.json",
    "BUCHAREST": "https://code.s3.yandex.net/async-module/bucharest-response.json",
    "ROMA": "https://code.s3.yandex.net/async-module/roma-response.json",
    "CAIRO": "https://code.s3.yandex.net/async-module/cairo-response.json",
    "GIZA": "https://code.s3.yandex.net/async-module/giza-response.json",
    "MADRID": "https://code.s3.yandex.net/async-module/madrid-response.json",
    "TORONTO": "https://code.s3.yandex.net/async-module/toronto-response.json"
}


def get_url_by_city_name(city_name: str) -> str:
    """Extract city url to make request by city name

    :param: city_name: City name like MOSCOW
    :return: City url
    """

    try:
        return CITIES[city_name]
    except KeyError as exc:
        raise Exception(
            "CITIES variable does not contain URL for city with name {city_name}"
        ) from exc
