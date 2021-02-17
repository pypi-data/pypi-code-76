from aristonremotethermo.aristonaqua import AquaAristonHandler
import time

sensors = [
    "errors",
    'errors_count',
    "current_temperature",
    "required_temperature",
    "mode",
    "power",
    "showers",
    "heating",
    "antilegionella",
    "eco",
    "remaining_time",
    "antilegionella_minimum_temperature",
    "antilegionella_maximum_temperature",
    "antilegionella_set_temperature",
    "online_version",
    "installed_version",
    "update",
    "time_program",
    "energy_use_in_day",
    "energy_use_in_week",
    "energy_use_in_month",
    "energy_use_in_year",
    "energy_use_in_day_periods",
    "energy_use_in_week_periods",
    "energy_use_in_month_periods",
    "energy_use_in_year_periods"
]

username = 's.zadurian@gmail.com'
password = 'Qwerty12!'
# username = 'viotemp1@icloud.com'
# password = '2iQnG0X6kk@3K9'

# username = 'lmcluis@gmail.com'
# password = 'pass123Temp'

api = AquaAristonHandler(
    username=username,
    password=password,
    sensors=sensors,
    boiler_type="velis",
    store_file=True,
    logging_level="DEBUG",
    #store_folder="D:/HASSIO/ariston-remotethermo-api/test/velis_http_logs"
)

api.start()

def sensors_updated(sensors, *args, **kwargs):
    print("*** Sensors were updated")
    print(f"*** Sensors are: {sensors}")

def status_updated(statuses, *args, **kwargs):
    print(f"*** Statuses were updated")
    print(f"*** Statuses are: {statuses}")

api.subscribe_sensors(sensors_updated)

api.subscribe_statuses(status_updated)

time.sleep(300)

api.stop()