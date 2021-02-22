from emobpy import Consumption, HeatInsulation, BEVspecs, DataBase

DB = DataBase('db')                                  # Instance of profiles' database whose input is the pickle files' folder
DB.loadfilesBatch(kind="driving")                    # loading mobility pickle files to the database
mname = list(DB.db.keys())[0]                        # getting the id of the first mobility profile

HI = HeatInsulation(True)                            # Creating the heat insulation configuration by copying the default configuration
BEVS = BEVspecs()                                    # Database that contains BEV models
VW_ID3 = BEVS.model(('Volkswagen','ID.3',2020))      # Model instance that contains vehicle parameters
VW_ID3.add({                                         # Adding required parameters that are not included in BEVS
            'Battery_charging_efficiency': 0.9,
            'Battery_discharging_efficiency': 0.95,
            'Transmission_efficiency': 0.95,
            'Auxiliary_power_W': 300,
            'Cabin_volume_m3': 3.5,
            'HVAC_COP_heating': 2,
            'HVAC_COP_cooling':2
            })
c = Consumption(mname, VW_ID3)
c.loadSettingMobility(DB)
c.run(
    heat_insulation=HI,
    weather_country='DE', 
    weather_year=2016, 
    passenger_mass=75,                   # kg
    passenger_sensible_heat=70,          # W
    passenger_nr=1.5, 
    air_cabin_heat_transfer_coef=20,     # W/(m2K)
    air_flow = 0.02,                     # m3/s
    driving_cycle_type='WLTC',
    road_type=0,
    road_slope=0
    )
c.save_profile('db')


