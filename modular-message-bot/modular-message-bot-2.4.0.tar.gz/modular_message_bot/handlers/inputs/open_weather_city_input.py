"""
# Open Weather City Input Module
Please read the LICENSE for OpenWeatherMap carefully, it is your responsibility!
Get an API key at https://home.openweathermap.org/users/sign_up

jq-vars test:
`cat tests/component-resources/response-open-weather-city.json | jq "\"Test: \" + .weather[0].description"`

Example Input:
```yaml
- code: open_weather_city
  parameters:
    query:
      q: edinburgh,uk
      appid: "$[OPEN_WEATHER_KEY]"
    jq-vars:
      weather_msg: ".slack_icon + \" \" + .weather[0].description + \" \" + .weather_by_with_link"
      another_msg: ".weather[0].description + \" \" + .weather_by"
```
In the example above, two vars will be created `weather_msg` and `another_msg`
"""
import logging

import requests

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job import JobConfigSection
from modular_message_bot.models.job_run import JobRunVar, JobRunVarCollection
from modular_message_bot.utils.jq_util import jq_filter_data

logger = logging.getLogger(__name__)


def weather_slack_icon(response_dict: dict) -> str:
    weather_id = response_dict["weather"][0]["id"]

    # https://openweathermap.org/weather-conditions
    advanced_map = {
        701: ":droplet:",  # Mist
        711: ":smoking:",  # Smoke
        721: ":cloud:",  # haze
        731: ":dusty_stick:",  # sand/ dust whirls
        741: ":fog:",
        751: ":sandwich:",  # sand
        761: ":dusty_stick:",  # dust
        762: ":clubs:",  # ash
        771: ":wind_blowing_face:",  # Squall
        781: ":tornado_cloud:",
        800: ":eye:",  # Clear
    }
    if weather_id in advanced_map.keys():
        return advanced_map[weather_id]

    simple_id = int(weather_id / 100)
    simple_map = {
        2: ":thunder_cloud_and_rain:",
        3: ":sweat_drops:",  # Drizzle
        5: ":rain_cloud:",  # Rain
        6: ":snow_cloud:",
        8: ":cloud:",
    }
    if simple_id in simple_map.keys():
        return simple_map[simple_id]

    # Unknown
    return ":question:"


class OpenWeatherCityInput(AbstractSimpleInputHandler):
    WEATHER_BY_TEXT_SIMPLE = "Weather by Openweathermap"
    WEATHER_BY_TEXT_WITH_LINK = "Weather by Openweathermap (openweathermap.org)"

    @classmethod
    def get_code(cls) -> str:
        return "open_weather_city"

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        parameters = job_config.parameters
        message_suffix = f"is required for '{self.get_code()}' input"

        # Required parameters
        for required_param_key in ["jq-vars"]:
            if required_param_key not in parameters.keys():
                return f"'{required_param_key}' {message_suffix}"

        # Required query parameters
        # Note: Query may not be there if we only want a weather_by etc
        if "query" in parameters.keys():
            for required_query_param_key in ["q", "appid"]:
                if required_query_param_key not in parameters["query"].keys():
                    return f"query.'{required_query_param_key}' {message_suffix}"

        return super().validate_job_config(job_config)

    def validate_job_run_var(self, job_run_var: JobRunVar):
        string_key = job_run_var.code
        string_value = job_run_var.value

        # https://stackoverflow.com/questions/30826747/using-openweathermap-api-for-free
        if (
            isinstance(string_value, str)
            and string_value.count(self.WEATHER_BY_TEXT_SIMPLE) <= 0
            and string_value.count(self.WEATHER_BY_TEXT_WITH_LINK) <= 0
        ):
            return f"For message '{string_key}' no weather by blurb present in the output message!"
        return super().validate_job_run_var(job_run_var)

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        # Settings
        jq_vars = parameters.get("jq-vars", {})
        jq_var_join = parameters.get("jq-var-join", "")

        # Request
        logger.info("OpenWeather - Loading")

        # Appended data
        weather_results = {
            "weather_by": self.WEATHER_BY_TEXT_SIMPLE,
            "weather_by_with_link": self.WEATHER_BY_TEXT_WITH_LINK,
        }

        # Parameters
        if "query" in parameters:
            url = parameters.get("url", "https://api.openweathermap.org/data/2.5/weather")
            query_parameters = parameters.get("query")
            response = requests.get(url, params=query_parameters)
            logger.info(f"OpenWeather - responseCode = {response.status_code}")
            if response.status_code != 200:
                raise Exception(f"Open weather failed '{str(response.status_code)}'\n'{str(response.content)}'")
            response_dict = response.json()
            weather_results = {
                **response_dict,
                **weather_results,
                "slack_icon": weather_slack_icon(response_dict),
            }

        # Filter data (JQ)
        for key, value in jq_filter_data(jq_vars, jq_var_join, weather_results).items():
            job_run_vars_collection.interpolate(key, value, self.get_code())
