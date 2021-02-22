from emobpy import Mobility

hrs = 168 # one week
steps = 0.25 # 15 minutes

for _ in range(2):  # creating five profiles
    try:
        m = Mobility()
        m.setParams("CFT", hrs, steps, "commuter", "01/01/2020")
        m.setStats(
            "TripsPerDay.csv",
            "DepartureDestinationTrip_Worker.csv",
            "DistanceDurationTrip.csv",
        )
        m.setRules("fulltime")
        m.run()
        m.save_profile("db")
    except:
        continue

for _ in range(2):  # creating five profiles
    try:
        m = Mobility()
        m.setParams("CPT", hrs, steps, "commuter", "01/01/2020")
        m.setStats(
            "TripsPerDay.csv",
            "DepartureDestinationTrip_Worker.csv",
            "DistanceDurationTrip.csv",
        )
        m.setRules("parttime")
        m.run()
        m.save_profile("db")
    except:
        continue

for _ in range(2):  # creating five profiles
    try:
        m = Mobility()
        m.setParams("NFT", hrs, steps, "non-commuter", "01/01/2020")
        m.setStats(
            "TripsPerDay.csv",
            "DepartureDestinationTrip_Free.csv",
            "DistanceDurationTrip.csv",
        )
        m.setRules("freetime")
        m.run()
        m.save_profile("db")
    except:
        continue
