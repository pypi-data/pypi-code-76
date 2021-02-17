from aristonremotethermo.ariston import AristonHandler
import time

sensors = [
    'internet_weather',
    'dhw_economy_temperature',
    'holiday_mode',
    'water_last_24h_list',
    'dhw_flame',
    'heating_last_365d',
    'heating_last_365d_list',
    'water_last_7d',
    'water_last_30d',
    'heating_last_24h',
    'update',
    'heating_last_30d',
    'heat_pump',
    'water_last_24h',
    'ch_flame',
    'water_last_7d_list',
    'ch_detected_temperature',
    'dhw_thermal_cleanse_cycle',
    'dhw_thermal_cleanse_function',
    # 'online_version',
    'electricity_cost',
    'mode',
    'ch_comfort_temperature',
    'gas_type',
    'errors_count',
    'signal_strength',
    'dhw_storage_temperature',
    'ch_auto_function',
    'water_last_30d_list',
    'dhw_set_temperature',
    'ch_set_temperature',
    'ch_pilot',
    'errors',
    'ch_antifreeze_temperature',
    'ch_program',
    'account_dhw_electricity',
    'dhw_comfort_temperature',
    'ch_mode',
    'internet_time',
    # 'units',
    'account_dhw_gas',
    'flame',
    'account_ch_gas',
    'heating_last_7d_list',
    'heating_last_7d',
    'heating_last_30d_list',
    'water_last_365d_list',
    'ch_economy_temperature',
    'outside_temperature',
    'gas_cost',
    'account_ch_electricity',
    'dhw_mode',
    'water_last_365d',
    'dhw_comfort_function',
    'dhw_program',
    'heating_last_24h_list',
    'cooling_last_24h',
    'cooling_last_7d',
    'cooling_last_30d',
    'cooling_last_365d',
    'cooling_last_24h_list',
    'cooling_last_7d_list',
    'cooling_last_30d_list',
    'cooling_last_365d_list',
    # 'ch_water_temperature'
]

# help(AristonHandler)

api = AristonHandler(
    username='pashchuk.oleg@gmail.com',
    password='maybe1+Krypton',
    sensors=sensors,
    units='metric',
    store_file=True,
    logging_level="DEBUG",
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