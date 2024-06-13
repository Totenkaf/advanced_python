# Copyright (c) 2023 Artem Ustsov

import json
from http import HTTPStatus
from http.client import HTTPException
import logging
from typing import Dict, Optional
from urllib.request import urlopen
from urllib.error import HTTPError

from client.utils import ERR_MESSAGE_TEMPLATE


LOG = logging.getLogger()


class YandexWeatherAPI:
    """
    Base class for requests
    """

    @staticmethod
    def __do_req(url: str) -> Dict:
        """Base request method

        :param: url: url as str
        :return: response data
        """

        try:
            with urlopen(url) as response:
                resp_body = response.read().decode("utf-8")
                data = json.loads(resp_body)
            if response.status != HTTPStatus.OK:
                raise Exception(
                    f"Error during execute request. "
                    f"{resp_body.status}: {resp_body.reason}"
                )
            LOG.info(f"Successfully get a response for {url}")
            return data
        except ValueError as exc:
            LOG.error("%s for %s", str(exc), url)
            raise ValueError(f"{type(exc).__name__}: {exc}") from exc
        except HTTPError as exc:
            LOG.error("%s for %s", str(exc), url)
            raise HTTPException(f"{type(exc).__name__}: {exc}") from exc
        except Exception as exc:
            LOG.error("%s for %s", str(exc), url)
            raise Exception(ERR_MESSAGE_TEMPLATE.format(error=exc, url=url))

    def get_forecasting(self, url: str) -> Optional[Dict]:
        """Make a request to YandexWeatherApi and get a weather data
        :param url: url as str
        :return: response data
        """

        try:
            return self.__do_req(url)
        except (HTTPException, ValueError) as exc:
            LOG.warning("Exception in YandexWeather loader during fetching data by url %s: %s", url, str(exc))
            return {}
