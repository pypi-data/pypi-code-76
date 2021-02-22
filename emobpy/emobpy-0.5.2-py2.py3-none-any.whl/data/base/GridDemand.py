from emobpy import Charging, DataBase


DB = DataBase('db')                                  # Instance of profiles' database whose input is the pickle files' folder
DB.loadfilesBatch(kind="availability")               # loading availability pickle files to the database
aname = list(DB.db.keys())[0]                        # getting the id of the first availability profile

strategies = ["immediate", "balanced", "from_0_to_24_at_home", "from_23_to_8_at_home"]

for option in strategies:
    c = Charging(aname)
    c.loadScenario(DB)
    c.setSubScenario(option)
    c.run()
    c.save_profile('db')
