from multiprocessing import Lock, Process, Queue, Manager, cpu_count
import numpy as np
import numba
from .constants import AIR_SPECIFIC_HEAT

T_RNG = np.array(list(AIR_SPECIFIC_HEAT.keys()))
CP_RNG = np.array(list(AIR_SPECIFIC_HEAT.values()))


def Parallelize(function=None, inputdict: dict = None, nr_workers=1, **kargs):
    """
    input is a dictionary that contains numbered keys and as value any object
    the queue contains tuples of keys and objects, the function must be
    consistent when getting data from queue
    """
    total_cpu = cpu_count()
    print(f"Workers: {nr_workers} of {total_cpu}")
    if nr_workers > total_cpu:
        nr_workers = total_cpu
        print(f"Workers: {nr_workers}")
    with Manager() as manager:
        dc = manager.dict()
        queue = Queue()
        for key, item in inputdict.items():
            queue.put((key, item))
        queue_lock = Lock()
        processes = {}
        for i in range(nr_workers):
            if kargs:
                processes[i] = Process(target=parallel_func,
                                       args=(
                                           dc,
                                           queue,
                                           queue_lock,
                                           function,
                                           kargs,
                                       ))
            else:
                processes[i] = Process(target=parallel_func,
                                       args=(
                                           dc,
                                           queue,
                                           queue_lock,
                                           function,
                                       ))
            processes[i].start()
        for i in range(nr_workers):
            processes[i].join()
        outputdict = dict(dc)
    return outputdict


def parallel_func(dc, queue=None, queue_lock=None, function=None, kargs={}):
    while True:
        queue_lock.acquire()
        if queue.empty():
            queue_lock.release()
            return None
        key, item = queue.get()
        queue_lock.release()
        obj = function(**item, **kargs)
        dc[key] = obj
    return None


def rolling_resistance_coeff(method='M1', **kwargs):
    '''
    M1 depends on v:velocity (km/h), temp: degC and road_type: int  -> Wang et al.
    M2 depends on v:velocity (km/h), tire_type: int, road_type: int -> Rahka et al.

    M1 options:
        v: km/h
        temp: degC
        road_type 
            0: ordinary car tires on concrete, new asphalt, cobbles small new, coeff: 0.01 - 0.015
            1: car tires on gravel - rolled new, on tar or asphalt, coeff: 0.02
            2: car tires on cobbles  - large worn, coeff: 0.03
            3: car tire on solid sand, gravel loose worn, soil medium hard, coeff: 0.04 - 0.08
            4: car tire on loose sand, coeff: 0.2 - 0.4
    M2 options:
        v: km/h
        tire_type
            0: Radial,    c2:0.0328, c3: 4.575
            1: Bias ply,  c2:0.0438, c3: 6.100
        road_type
            Concrete: excelente 0: 1.00, good 1: 1.50, poor 2: 2.00
            Asphalt: good 3: 1.25, fair 4: 1.75, poor 5: 2.25
            Macadam: good 6: 1.50, fair 7: 2.25, poor 8: 3.75
            Cobbles: ordinary 9: 5.50, poor 10: 8.50
            Snow: 2 inch 11: 2.50, 4 inch 12: 3.75
            Dirt: Smooth 13: 2.50, sandy 14: 3.75
            Sand not implemented range 6.00 - 30.00
    '''
    if method == 'M1':
        return rolling_resistance_coeff_M1(**kwargs)
    elif method == 'M2':
        return rolling_resistance_coeff_M2(**kwargs)
    else:
        raise Exception('Method must be M1 or M2')


@numba.jit(nopython=True)
def rolling_resistance_coeff_M1(temp, v, road_type=0):
    '''
    v: km/h
    temp: degC
    road_type 
        0: ordinary car tires on concrete, new asphalt, cobbles small new, coeff: 0.01 - 0.015
        1: car tires on gravel - rolled new, on tar or asphalt, coeff: 0.02
        2: car tires on cobbles  - large worn, coeff: 0.03
        3: car tire on solid sand, gravel loose worn, soil medium hard, coeff: 0.04 - 0.08
        4: car tire on loose sand, coeff: 0.2 - 0.4
    reference: Wang, J.; Besselink, I.; Nijmeijer, H. Electric Vehicle Energy Consumption Modelling and Prediction Based on Road Information.
    World Electr. Veh. J. 2015, 7, 447-458. https://doi.org/10.3390/wevj7030447
    '''
    factor = [1, 1.5, 2.2, 4, 20]
    return (1.9e-6 * temp**2 - 2.1e-4 * temp + 0.013 +
            5.4e-5 * v) * factor[road_type]


@numba.jit(nopython=True)
def rolling_resistance_coeff_M2(v, tire_type=0, road_type=4):
    '''
    v: km/h
    tire_type
        0: Radial,    c2:0.0328, c3: 4.575
        1: Bias ply,  c2:0.0438, c3: 6.100
    road_type
        Concrete: excelente 0: 1.00, good 1: 1.50, poor 2: 2.00
        Asphalt: good 3: 1.25, fair 4: 1.75, poor 5: 2.25
        Macadam: good 6: 1.50, fair 7: 2.25, poor 8: 3.75
        Cobbles: ordinary 9: 5.50, poor 10: 8.50
        Snow: 2 inch 11: 2.50, 4 inch 12: 3.75
        Dirt: Smooth 13: 2.50, sandy 14: 3.75
        Sand not implemented range 6.00 - 30.00

    reference: Rahka et al. 2001. Vehicle Dynamics Model for Predicting Maximum Truck Acceleration Levels.
    https://doi.org/10.1061/(ASCE)0733-947X(2001)127:5(418)
    '''

    road = {
        0: {
            'Cr': 1.0
        },
        1: {
            'Cr': 1.5
        },
        2: {
            'Cr': 2.0
        },
        3: {
            'Cr': 1.25
        },
        4: {
            'Cr': 1.75
        },
        5: {
            'Cr': 2.25
        },
        6: {
            'Cr': 1.5
        },
        7: {
            'Cr': 2.25
        },
        8: {
            'Cr': 3.75
        },
        9: {
            'Cr': 5.5
        },
        10: {
            'Cr': 8.5
        },
        11: {
            'Cr': 2.5
        },
        12: {
            'Cr': 3.75
        },
        13: {
            'Cr': 2.5
        },
        14: {
            'Cr': 3.75
        }
    }
    tire = {0: {'c2': 0.0328, 'c3': 4.575}, 1: {'c2': 0.0438, 'c3': 6.100}}

    Cr = road[road_type]['Cr']
    c2 = tire[tire_type]['c2']
    c3 = tire[tire_type]['c3']

    return Cr * (c2 * v + c3) / 1000


@numba.jit(nopython=True)
def vehicle_mass(curb_weight, passengers_weight):
    return curb_weight + passengers_weight


@numba.jit(nopython=True)
def Prollingresistance(rolling_resistance_coeff,
                       vehicle_mass,
                       g,
                       v,
                       slop_angle=0):
    return rolling_resistance_coeff * vehicle_mass * g * np.cos(
        np.deg2rad(slop_angle)) * v


@numba.jit(nopython=True)
def Pairdrag(air_density, frontal_area, drag_coeff, v, wind_speed=0):
    '''
    wind_speed: wind speed in direction of the vehicle.
    reference: Wang, J.; Besselink, I.; Nijmeijer, H. Electric Vehicle Energy Consumption Modelling and Prediction Based on Road Information.
    World Electr. Veh. J. 2015, 7, 447-458. https://doi.org/10.3390/wevj7030447
    '''
    return 1 / 2 * air_density * frontal_area * drag_coeff * (
        v - wind_speed)**2 * v


@numba.jit(nopython=True)
def Pgravity(vehicle_mass, g, v, slop_angle=0):
    return vehicle_mass * g * np.sin(np.deg2rad(slop_angle)) * v


@numba.jit(nopython=True)
def Pinertia(inertial_mass, vehicle_mass, acceleration, v):
    return (vehicle_mass + inertial_mass) * acceleration * v


@numba.jit(nopython=True)
def Pwheel(p_rollingresistance, p_airdrag, p_gravity, p_inertia):
    return p_rollingresistance + p_airdrag + p_gravity + p_inertia


@numba.jit(nopython=True)
def Pmotorout(p_wheel, transmission_eff):
    only_positive = p_wheel.copy()
    only_positive[only_positive < 0.0] = 0.0
    result = only_positive / transmission_eff
    mask = np.isnan(result)
    result[mask] = 0
    return result


@numba.jit(nopython=True)
def Pgeneratorin(p_wheel, transmission_eff, regenerative_breaking_eff):
    only_negative = p_wheel.copy()
    only_negative[only_negative > 0.0] = 0.0
    result = only_negative * transmission_eff * regenerative_breaking_eff
    mask = np.isnan(result)
    result[mask] = 0
    return result


@numba.jit(nopython=True)
def EFFICIENCYregenerative_breaking(acceleration):
    neg_acceleration = acceleration.copy()
    neg_acceleration[neg_acceleration > 0.0] = 0.0
    result = (np.exp(0.0411 / np.abs(neg_acceleration)))**(-1)
    mask = np.isnan(result)
    result[mask] = 0
    return result


@numba.jit(nopython=True)
def Pmotorin(p_motor_out, motor_eff):
    result = p_motor_out / motor_eff
    mask = np.isnan(result)
    result[mask] = 0
    return result


@numba.jit(nopython=True)
def Pgeneratorout(p_generator_in, generator_eff):
    result = p_generator_in * generator_eff
    mask = np.isnan(result)
    result[mask] = 0
    return result


# Heat transfer
@numba.jit(nopython=True)
def Q_person(Q_sensible, Persons=1):
    '''
    Q_sensible: W
    number_persons: int
    '''
    return Q_sensible * Persons


@numba.jit(nopython=True)
def Q_ventilation(Density_air, Flow_air, Cp_air, Temp_air):
    '''
    Density_air: kg/m3, Flow_air: m3/s, Cp_air: J/(kg*K), Temp_air: degC
    '''
    Temp_kelvin = Temp_air + 273.15
    return Density_air * Flow_air * Cp_air * Temp_kelvin


@numba.jit(nopython=True)
def Q_transfer(zone_layer,
               zone_area,
               layer_conductivity,
               layer_thickness,
               t_air_cabin,
               t_air_out,
               vehicle_speed,
               air_cabin_heat_transfer_coef=10):
    t_air_cabin_K = t_air_cabin + 273.15
    t_air_out_K = t_air_out + 273.15
    R = Resistances(zone_layer, zone_area, layer_conductivity, layer_thickness,
                    vehicle_speed, air_cabin_heat_transfer_coef)
    return (t_air_cabin_K - t_air_out_K) * R


@numba.jit(nopython=True)
def htc_air_out(vehicle_speed, limit=5):
    h = 6.14 * np.power(vehicle_speed, 0.78)
    if vehicle_speed < limit:
        h = 6.14 * np.power(limit, 0.78)
    # print(h)
    return h


@numba.jit(nopython=True)
def Resistances(zone_layer, zone_area, layer_conductivity, layer_thickness,
                vehicle_speed, air_cabin_heat_transfer_coef):
    x_z = zone_layer * layer_thickness
    R_c = x_z / layer_conductivity
    h_i = air_cabin_heat_transfer_coef
    h_o = htc_air_out(vehicle_speed)
    S_rc = R_c.sum(axis=1)
    R_hz = 1 / h_i + S_rc + 1 / h_o
    R_z = zone_area / R_hz
    return R_z.sum()


# @numba.jit(nopython=True)
def Qhvac(D,
          T_out,
          T_targ,
          cabin_volume,
          Flow_air,
          zone_layer,
          zone_area,
          layer_conductivity,
          layer_thickness,
          vehicle_speed,
          Q_sensible=70,
          Persons=1,
          P_out=1013.25,
          h_out=60,
          air_cabin_heat_transfer_coef=10):
    '''
    Q indexes 0: Qtotal, 1: Q_in_per, 2: Q_in_vent, 3: Q_out_vent, 4: Q_tr
    '''
    mass_flow_in = Flow_air * D(T_out, P_out, h=h_out)

    T = np.zeros((vehicle_speed.shape[0], ))
    Q = np.zeros((vehicle_speed.shape[0], 8))
    if T_targ is None:
        return Q, T
    t_diff = T_out - T_targ  # positive if cooling, negative if heating
    if t_diff > 0:
        plus = -0.05
        sign = -1  # cooling
    else:
        plus = 0.05
        sign = 1  # heating

    for tm in range(vehicle_speed.shape[0]):
        if tm == 0:
            t_1 = T_out
            t = T_out + plus
        else:
            t_1 = T[tm - 1]
            if sign == -1:
                if np.round(t, 2) > T_targ:
                    t += plus
                else:
                    t = T_targ
            else:
                if np.round(t, 2) < T_targ:
                    t += plus
                else:
                    t = T_targ

        Q_in_per = Q_person(Q_sensible, Persons)
        Q[tm][1] = Q_in_per
        Q_in_vent = Q_ventilation(D(T_out, P_out, h=h_out), Flow_air,
                                  Cp(T_out), T_out)
        Q[tm][2] = Q_in_vent
        Q_out_vent = Q_ventilation(D(t, P_out, h=h_out),
                                   mass_flow_in / D(t, P_out, h=h_out), Cp(t),
                                   t)
        Q[tm][3] = Q_out_vent
        Q_tr = Q_transfer(zone_layer, zone_area, layer_conductivity,
                          layer_thickness, t, T_out, vehicle_speed[tm],
                          air_cabin_heat_transfer_coef)
        Q[tm][4] = Q_tr
        Q[tm][0] = cabin_volume * D(t, P_out, h=h_out) * Cp(t) * (
            t - t_1) - Q_in_per - Q_in_vent + Q_out_vent + Q_tr
        T[tm] = t

        # more info for debugging
        Q[tm][5] = D(T_out, P_out, h=h_out)
        Q[tm][6] = D(t, P_out, h=h_out)
        Q[tm][7] = Resistances(zone_layer, zone_area, layer_conductivity,
                               layer_thickness, vehicle_speed[tm],
                               air_cabin_heat_transfer_coef)
    return Q, T


@numba.jit(nopython=True)
def Cp(T):
    return np.interp(T, T_RNG, CP_RNG)


def plot_multi(data, cols=None, spacing=.1, **kwargs):

    from pandas import plotting

    # Get default color style from pandas - can be changed to any other color list
    if cols is None: cols = data.columns
    if len(cols) == 0: return
    colors = getattr(
        getattr(plotting, '_matplotlib').style,
        '_get_standard_colors')(num_colors=len(cols))

    # First axis
    ax = data.loc[:, cols[0]].plot(label=cols[0], color=colors[0], **kwargs)
    ax.set_ylabel(ylabel=cols[0])
    lines, labels = ax.get_legend_handles_labels()

    for n in range(1, len(cols)):
        # Multiple y-axes
        ax_new = ax.twinx()
        ax_new.spines['right'].set_position(('axes', 1 + spacing * (n - 1)))
        data.loc[:, cols[n]].plot(ax=ax_new,
                                  label=cols[n],
                                  color=colors[n % len(colors)],
                                  **kwargs)
        ax_new.set_ylabel(ylabel=cols[n])

        # Proper legend position
        line, label = ax_new.get_legend_handles_labels()
        lines += line
        labels += label

    ax.legend(lines, labels, loc=0)
    return ax


# TODO: This function should go in a reporting module like report.py
def balance(DB, tscode, include=None):
    if DB.db[tscode]["kind"] != "consumption":
        raise Exception(
            "code '{}' does not correspond to a consumption profile".format(
                tscode))
    if include is None:
        # all trips
        flag = True
        cons = 0
        distance = 0
        for trip in DB.db[tscode]["Trips"].trips:
            if flag:
                value = np.zeros(trip.balance["value"].shape)
                flag = False
            value = value + trip.balance["value"]
            cons = cons + trip.consumption['value']  # kWh
            distance = distance + trip.distance['value']  # km
        label = trip.balance["label"]
        source = trip.balance["source"]
        target = trip.balance["target"]
        consumption = cons
        rate = consumption * 100 / distance
    elif isinstance(include, int):
        value = DB.db[tscode]["Trips"].trips[include].balance["value"]
        label = DB.db[tscode]["Trips"].trips[include].balance["label"]
        source = DB.db[tscode]["Trips"].trips[include].balance["source"]
        target = DB.db[tscode]["Trips"].trips[include].balance["target"]
        distance = DB.db[tscode]["Trips"].trips[include].distance["value"]
        consumption = DB.db[tscode]["Trips"].trips[include].consumption[
            "value"]
        rate = consumption * 100 / distance  # kWh/100 km
    elif isinstance(include, list):
        flag = True
        cons = 0
        distance = 0
        count = -1
        for trip in DB.db[tscode]["Trips"].trips:
            count += 1
            if count >= include[0] and count < include[1]:
                if flag:
                    value = np.zeros(trip.balance["value"].shape)
                    flag = False
                value = value + trip.balance["value"]
                cons = cons + trip.consumption["value"]
                distance = distance + trip.distance["value"]
        label = trip.balance["label"]
        source = trip.balance["source"]
        target = trip.balance["target"]
        consumption = cons
        rate = consumption * 100 / distance  # kWh/100 km
    return distance, consumption, rate, label, source, target, value
