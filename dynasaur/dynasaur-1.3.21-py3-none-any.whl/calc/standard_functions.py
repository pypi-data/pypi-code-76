import numpy as np
from scipy.integrate import cumtrapz, odeint
from scipy.integrate import cumtrapz, odeint

from scipy.interpolate import interp1d
from scipy.stats import norm
from scipy import signal

from ..calc.cfc import CFC
from ..calc.risk_function_util import DCDF, RibCriteria
from ..calc.object_calculation_util import ObjectCalcUtil, UniversalLimit
from ..data.ls_dyna import EloutIndex
from ..utils.constants import LOGConstants, PluginsParamDictDef, OutputStringForPlugins


class StandardFunction:

    @staticmethod
    def res(data_vector: np.ndarray, units):
        """
        :param data_vector:
        :return:
        """
        return np.linalg.norm(data_vector, axis=1).reshape(-1, 1)

    @staticmethod
    def max(data_vector: np.ndarray, units):
        """
        Return the maximum of an array. 
        Further info : https://numpy.org/doc/stable/reference/generated/numpy.amax.html
        :param data_vector: The data_vector from which the maximum value should be 
        :type data_vector: np.ndarray
        :param units: Units object, information about the used system of units in the simulated output
        :type units: Units as implemented in /dynasaur/data/dynasaur_definitions.py

        :returns: Maximum of data_vector
        :rtype: scalar
        """

        return np.max(data_vector)

    @staticmethod
    def absmax(data_vector: np.ndarray, units):
        """
        :param data_vector:
        :param absolute:
        :return:
        """
        data_vector = np.abs(data_vector)
        return np.max(data_vector)

    @staticmethod
    def max_in_row(data_vector: np.ndarray, units):
        """
        :param data_vector:
        :return:
        """
        assert len(data_vector.shape) == 2
        return np.max(data_vector, axis=1)

    @staticmethod
    def argmax(data_vector: np.ndarray, units):
        """
        :param data_vector:
        :return:
        """
        index_of_maximum = np.argmax(np.abs(data_vector))
        return index_of_maximum

    @staticmethod
    def min(data_vector: np.ndarray, units):
        """
        :param data_vector:
        :return:
        """
        return np.min(data_vector)

    @staticmethod
    def mult(data_vector_1: np.ndarray, data_vector_2: np.ndarray, units):
        """
        :param data_vector_1:
        :param data_vector_2:
        :return:
        """

        return np.multiply(data_vector_1, data_vector_2)

    @staticmethod
    def abs(data_vector: np.ndarray, units):
        """
        :param data_vector:
        :return:
        """
        return np.abs(data_vector)

    @staticmethod
    def transform2origin(data_vector: np.ndarray, units):
        """
        :param data_vector:
        :return:
        """
        return data_vector - data_vector[0]

    @staticmethod
    def at_index(index: int, data_vector: np.ndarray, units):
        """
        :param index:
        :param data_vector:
        :return:
        """
        return data_vector[index]

    @staticmethod
    def linspace(start, stop, num, endpoint, units):
        """

        :param start:
        :param stop:
        :param num:
        :param endpoint:
        :return:
        """

        return np.linspace(start, stop, num, endpoint).reshape(-1, 1)

    @staticmethod
    def sub(data_vector_1: np.ndarray, data_vector_2: np.ndarray, units):
        """

        :param data_vector_1:
        :param data_vector_2:
        :return:
        """
        return np.subtract(data_vector_1, data_vector_2)

    @staticmethod
    def add(data_vector_1: np.ndarray, data_vector_2: np.ndarray, units):
        """

        :param data_vector_1:
        :param data_vector_2:
        :return:
        """
        return np.add(data_vector_1, data_vector_2)

    @staticmethod
    def div(data_vector_1: np.ndarray, data_vector_2: np.ndarray, units):
        """
        :param data_vector_1:
        :param data_vector_2:
        :return:
        """
        return np.divide(data_vector_1, data_vector_2)

    @staticmethod
    def row_sum(matrix: np.ndarray, units):
        """
        :param matrix:
        :return:
        """
        return np.sum(matrix, axis=1)

    @staticmethod
    def abs_sub(data_vector_1: np.ndarray, data_vector_2: np.ndarray, units):
        """
        :param data_vector_1:
        :param data_vector_2:
        :return:
        """
        return np.abs(np.subtract(data_vector_1, data_vector_2))

    @staticmethod
    def abs_add(data_vector_1: np.ndarray, data_vector_2: np.ndarray, units):
        """
        :param data_vector_1:
        :param data_vector_2:
        :return:
        """
        return np.abs(np.add(data_vector_1, data_vector_2))

    @staticmethod
    def abs_sub_res(data_vector_1: np.ndarray, data_vector_2: np.ndarray, units):
        """
        :param data_vector_1:
        :param data_vector_2:
        :return:
        """
        rel_dist = []
        rel_dist_m = np.subtract(data_vector_1, data_vector_2)
        for i in range(len(rel_dist_m)):
            rel_dist.append((rel_dist_m[i, 0] ** 2 + rel_dist_m[i, 1] ** 2 + rel_dist_m[i, 2] ** 2) ** (1 / 2))

        return np.abs(rel_dist)

    @staticmethod
    def time_of_first_negative(data_vector: np.ndarray, time: np.ndarray, units):
        """
        :param data_vector:
        :param time:
        :return:
        """
        time_where_data_vector_less_zero = time[(np.where(data_vector < 0))]
        return time_where_data_vector_less_zero[0] if len(time_where_data_vector_less_zero) != 0 else np.inf

    @staticmethod
    def ccdf_weibull(x: float, lambda_: float, k: float, units):
        """
        :param lambda_:
        :param k:
        :param x:

        :return:
        """
        return 1 - np.exp(-(x / lambda_) ** k)

    @staticmethod
    def ccdf_sigmoid(x: float, x0: float, k: float, units):
        """

        :param x:
        :param x0:
        :param k:
        :return:

        Logistic function
        https://en.wikipedia.org/wiki/Logistic_function

        """
        return 1 / (1 + np.exp(-k * (x - x0)))


    @staticmethod
    def ASI(time_:np.ndarray, acc_x:np.ndarray,
            acc_y: np.ndarray, acc_z: np.ndarray,
            limit_acc_x:float,
            limit_acc_y:float,
            limit_acc_z:float,
            filter_option:str,
            units):
        """

        :param time
        :param acceleration_x:
        :param acceleration_y:
        :param acceleration_z:
        :param limit_acceleration_x:
        :param lim_acceleration_y:
        :param lim_acceleration_z:
        :param filter_option:
        :param units:
        :return:
        """
        g = 9.81

        # average over time
        N = np.where(time_.flatten() / units.second() < 0.05)[0][-1]  # 50 ms

        acc_x /= units.meter() / (units.second() ** 2) * g # acc_x in [m/s^2]
        acc_y /= units.meter() / (units.second() ** 2) * g # acc_y in [m/s^2]
        acc_z /= units.meter() / (units.second() ** 2) * g # acc_z in [m/s^2]

        assert (filter_option in ["butter", "mean"])

        if filter_option == "mean":
            acceleration_x = np.convolve(acc_x.flatten(), np.ones(N) / N, mode='same').reshape(-1, 1)
            acceleration_y = np.convolve(acc_y.flatten(), np.ones(N) / N, mode='same').reshape(-1, 1)
            acceleration_z = np.convolve(acc_z.flatten(), np.ones(N) / N, mode='same').reshape(-1, 1)
        else:
            sos = signal.butter(4, 13, 'lowpass', fs=1000, output='sos')
            acceleration_x = signal.sosfilt(sos, acc_x.flatten()).reshape(-1, 1)
            acceleration_y = signal.sosfilt(sos, acc_y.flatten()).reshape(-1, 1)
            acceleration_z = signal.sosfilt(sos, acc_z.flatten()).reshape(-1, 1)

        return np.sqrt((acceleration_x/limit_acc_x)**2
                       + (acceleration_y/limit_acc_y)**2
                        + (acceleration_z/limit_acc_z)**2)

    @staticmethod
    def ASI_from_velocity(time_:np.ndarray, vel_x:np.ndarray,
            vel_y: np.ndarray, vel_z: np.ndarray,
            limit_acc_x:float,
            limit_acc_y:float,
            limit_acc_z:float,
            filter_option:str,
            units):
        """

        :param time
        :param acceleration_x:
        :param acceleration_y:
        :param acceleration_z:
        :param limit_acceleration_x:
        :param lim_acceleration_y:
        :param lim_acceleration_z:
        :param units:
        :return:
        """

        acc_x = np.gradient(vel_x, axis=0)
        acc_y = np.gradient(vel_y, axis=0)
        acc_z = np.gradient(vel_z, axis=0)
        return StandardFunction.ASI(time_, acc_x, acc_y, acc_z, limit_acc_x, limit_acc_y, limit_acc_z,
                                    filter_option, units)

    @staticmethod
    def THIV(time_: np.ndarray, acc_x: np.ndarray,
            acc_y: np.ndarray, rvel_z: np.ndarray,
            Dx: float,
            Dy: float,
            units):
        """

        :param time_
        :param acc_x:
        :param acc_y:
        :param rvel_z:
        :param Dx:
        :param Dy:
        :param units:
        :return:
        """
        time_si = time_ / units.second()
        time_si = time_si.flatten()

        acc_x = np.gradient(acc_x, time_si, axis=0)
        acc_y = np.gradient(acc_y, time_si, axis=0)

        rvel_z *= units.second()
        rvel_z = rvel_z.flatten()

        acc_x = acc_x.flatten()
        acc_y = acc_y.flatten()

        rdisp_z = np.append(0, np.array([cumtrapz(rvel_z, x=time_si, axis=-1)]))

        acc_x_floor = np.cos(rdisp_z) * acc_x - np.sin(rdisp_z) * acc_y
        acc_y_floor = np.sin(rdisp_z) * acc_x + np.cos(rdisp_z) * acc_y

        vel_x_floor = np.append(0, np.array([cumtrapz(acc_x_floor, x=time_si, axis=-1)]))
        vel_y_floor = np.append(0, np.array([cumtrapz(acc_y_floor, x=time_si, axis=-1)]))

        dist_x_floor = np.append(0, np.array([cumtrapz(vel_x_floor, x=time_si, axis=-1)]))
        dist_y_floor = np.append(0, np.array([cumtrapz(vel_y_floor, x=time_si, axis=-1)]))

        x_0 = 0
        y_0 = 0

        dist_head_x = ((x_0 - dist_x_floor) * np.cos(rdisp_z)) + ((y_0-dist_y_floor) * np.sin(rdisp_z))
        dist_head_y = -((x_0 - dist_x_floor) * np.sin(rdisp_z)) + (y_0-dist_y_floor) * np.cos(rdisp_z)

        # v_head
        # cosψ −Y & c sinψ + yb(t) ψ &
        vel_x_head = -vel_x_floor*np.cos(rdisp_z) - vel_y_floor*np.sin(rdisp_z) + dist_head_y * rvel_z
        vel_y_head = vel_x_floor*np.sin(rdisp_z) - vel_y_floor*np.cos(rdisp_z) - dist_head_x * rvel_z

        index_flight_time = np.min(np.where(np.logical_or(np.round(dist_head_x, 1) == Dx + x_0,
                                                         (np.round(dist_head_y, 1) == Dy),
                                                         (np.round(dist_head_y, 1) == -Dy))))
        return (np.sqrt(vel_x_head**2 + vel_y_head**2) * 3.6)[:index_flight_time]


    @staticmethod
    def ccdf_normal_dist(x: float, mean: float, standard_deviation: float, units):
        """

        :param x:
        :param mean:
        :param standard_deviation:
        :return:

        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
        """
        return norm.cdf(x, loc=mean, scale=standard_deviation)


    @staticmethod
    def cfc(time: np.ndarray, sampled_array: np.ndarray, cfc: int, units, mirroring: bool = False):
        """

        :param time:
        :param sampled_array:
        :param cfc:
        :param mirroring:
        :param units:
        :return:
        """
        assert len(time >= 2)

        Time = (time[1] - time[0])[0] / units.second()
        cfc = CFC(cfc=cfc, T=Time)
        nr_sampled_array_data_series = sampled_array.shape[1]
        return np.transpose(cfc.filter(
            sampled_array=np.transpose(sampled_array.reshape(-1, nr_sampled_array_data_series)),
            time=time, time_to_seconds_factor=units.second(), mirroring_flag=mirroring))

    @staticmethod
    def central_differences(data_vector_1: np.ndarray, data_vector_2: np.ndarray, units):
        """
        :param data_vector_1:
        :param data_vector_2:
        :return:
        """
        v = data_vector_1.flatten()
        time = data_vector_2
        a = np.gradient(v, np.squeeze(time))
        return np.array(a).reshape(-1, 1)

    @staticmethod
    def tibia_index(Mx: float, My: float, Fz: float, critical_bending_moment: float, critical_compression_force: float,
                    units):
        """

        :param Mx:
        :param My:
        :param Fz:
        :param critical_bending_moment:
        :param critical_compression_force:
        :param units:
        :return:
        """

        mx = Mx / ((units.meter() ** 2) / (units.second() ** 2))
        my = My / ((units.meter() ** 2) / (units.second() ** 2))
        fz = Fz / (units.meter() / (units.second() ** 2))
        critical_bending_moment = critical_bending_moment  # Input def: Nm
        critical_compression_force = critical_compression_force  # Input def: N

        mr = np.linalg.norm(np.stack([mx, my], axis=1)[:, :, 0], axis=1)
        ti = np.abs(mr / critical_bending_moment) + np.abs(fz / critical_compression_force)

        return ti



    @staticmethod
    def NIC(a_t1: np.ndarray, a_head: np.ndarray, time_: np.ndarray, units):
        """
        :param a_head:
        :param a_t1:
        :param time_:
        :param units:
        :return:
        """

        a_t1 = a_t1.flatten()
        a_head = a_head.flatten()
        a_t1 /= units.meter() / (units.second() ** 2)  # a_t1 in [m/s^2]
        a_head /= units.meter() / (units.second() ** 2)  # a_head in [m/s^2]
        a_rel = a_t1 - a_head

        t = time_.flatten() / units.second()  # t in [s]
        v_rel = cumtrapz(a_rel, t, initial=0)  # integral

        return_value_nic = 0.2 * a_rel + v_rel ** 2

        return np.array(return_value_nic).reshape(-1, 1)

    @staticmethod
    def DAMAGE(time: np.array, ra_x:np.array, ra_y:np.array, ra_z:np.array, mx: float, my: float, mz: float,
               kxx: float, kyy: float, kzz: float, kxy: float, kyz: float, kxz: float, a0: float, a1: float, beta: float,
               units):

        def stiffness_matrix(kxx, kyy, kzz, kxy, kyz, kxz):
            return np.array([[kxx + kxy + kxz, -kxy, -kxz],
                             [-kxy, kxy + kyy + kyz, -kyz],
                             [-kxz, -kyz, kxz + kyz + kzz]])

        def damping_matrix(m, k, a0, a1):
            return a0 * m + a1 * k

        def create_matrices(mx, my, mz, kxx, kyy, kzz, kxy, kyz, kxz, a0, a1):
            m = np.diag([mx, my, mz])
            k = stiffness_matrix(kxx, kyy, kzz, kxy, kyz, kxz)
            c = damping_matrix(m, k, a0, a1)
            return m, c, k

        def equation_of_motion(y, t, m, m_inv, c, k, f_a_x, f_a_y, f_a_z):
            delta_x, delta_y, delta_z, d_delta_x, d_delta_y, d_delta_z = y
            delta = np.array([delta_x, delta_y, delta_z])
            d_delta = np.array([d_delta_x, d_delta_y, d_delta_z])

            a = np.array([f_a_x(t), f_a_y(t), f_a_z(t)])
            dd_delta = np.dot(m_inv, np.dot(m, a) - (np.dot(c, d_delta) + np.dot(k, delta)))
            dydt = [d_delta_x, d_delta_y, d_delta_z, dd_delta[0], dd_delta[1], dd_delta[2]]
            return dydt

        # initial values of delta and delta' are zero
        t = time.flatten() / units.second()
        ra_x = ra_x.flatten() / (1 / (units.second() ** 2))   # to [rad/s^2]
        ra_y = ra_y.flatten() / (1 / (units.second() ** 2))   # to [rad/s^2]
        ra_z = ra_z.flatten() / (1 / (units.second() ** 2))   # to [rad/s^2]

        y0 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        m, c, k = create_matrices(mx, my, mz, kxx, kyy, kzz, kxy, kyz, kxz, a0, a1)

        m_inv = np.linalg.inv(m)
        # since mass matrix is identity matrix with parameters from settings file this could be considered in the
        # calculation if speed is an issue

        f_a_x = interp1d(t, ra_x, fill_value='extrapolate')
        f_a_y = interp1d(t, ra_y, fill_value='extrapolate')
        f_a_z = interp1d(t, ra_z, fill_value='extrapolate')
        sol = odeint(equation_of_motion, y0, t,
                     args=(m, m_inv, c, k, f_a_x, f_a_y, f_a_z))

        # alternative solution for faster execution (but less precise):
        #
        # sol = solve_ivp(equation_of_motion, (time_ang_acc[0], time_ang_acc[-1]), y0, method='RK45', t_eval=time_ang_acc,
        #                  args=(m, m_inv, c, k, time_ang_acc, ang_acc_x, ang_acc_y, ang_acc_z))
        #     print(ptime.time() - t_start)
        #     delta = sol['y'][:3, :]
        #     delta_norm = np.linalg.norm(delta, axis=0)

        delta = sol[:, :3]
        delta_norm = np.linalg.norm(delta, axis=1)
        damage = beta * np.max(delta_norm)

        return damage


    @staticmethod
    def HIC(time: np.ndarray, a_res: np.ndarray, units, nidx):
        """
        time vector in ms
        a_res in mm/s²

        make that consistent and use definitions here!
        use more outputs here!
        possible to return HIC for each time step
        :param time:
        :param a_res:
        :param units:
        :param flag(HIC15/HIC36):

        :return:
        """
        t = time.flatten() / units.second()  # t in [s]
        a_res = a_res.flatten()
        a_res /= units.meter() / (units.second() ** 2)  # a_res in [m/s^2]
        a_res /= units.grav_const  # a_res in [g]

        vel = cumtrapz(a_res, t, initial=0)
        hic15 = []
        time2 = []
        dt = (t[1] - t[0])
        nidx = int(round(nidx / dt))

        # TODO
        # RuntimeWarning: invalid value encountered in double_
        # scalars temp.append((tdiff) * (((vel[jt] - vel[ut]) / (tdiff)) ** 2.5))
        # problem None values

        for ut in range(len(t) - 1):
            temp = []
            for jt in range(ut + 1, min([len(t), ut + nidx])):
                tdiff = t[jt] - t[ut]
                temp.append(tdiff * (((vel[jt] - vel[ut]) / tdiff) ** 2.5))

            m = np.nanmax(temp)
            hic15.append(m)
            time2.append(t[ut])

        hic15.append(hic15[-1])
        return np.array(hic15).reshape(-1, 1)

    @staticmethod
    def HIC_15(time: np.ndarray, a_res: np.ndarray, units):
        return StandardFunction.HIC(time=time, a_res=a_res, units=units, nidx=0.015)

    @staticmethod
    def HIC_36(time: np.ndarray, a_res: np.ndarray, units):
        return StandardFunction.HIC(time=time, a_res=a_res, units=units, nidx=0.036)

    @staticmethod
    def percentile(object_data: dict, selection_tension_compression: str,
                   integration_point: str, percentile: str, units):
        """
        only one value possible to return

        :param object_data:
        :param selection_tension_compression:
        :param integration_point:
        :param percentile:
        :return:
        """

        part_ids = object_data["part_ids"]
        part_data = object_data["part_data"]
        part_idx = object_data["part_idx"]
        # time_step_indices = object_data["time_step_indices"]

        if len(part_ids) == 0:
            return 0

        # SELECTION_TENSION_COMPRESSION = "selection_tension_compression"
        # INTEGRATION_POINT = "integration_point"
        # PERCENTILE = "percentile"

        # selection_tension_compression = param_dict[PluginsParamDictDef.SELECTION_TENSION_COMPRESSION]
        # integration_point = param_dict[PluginsParamDictDef.INTEGRATION_POINT]
        # percentile = param_dict[PluginsParamDictDef.PERCENTILE]

        obj_calc = ObjectCalcUtil()
        (function_overall_tension_compression, integration_point_function) = \
            obj_calc.retrieve_functions(selection_tension_compression, integration_point)

        percentile_values = []
        element_count = 0

        for part_id in part_ids:
            index = part_idx[part_id]
            data = part_data[part_id]
            element_ids = np.unique(index[:, 0])
            element_count += len(element_ids)

            for element_id in element_ids:
                row_ids = np.where(index[:, 0] == element_id)[0]

                reduced_integration_point_data = integration_point_function(data[:, row_ids, :], axis=1)
                result_data = function_overall_tension_compression(reduced_integration_point_data, axis=1)
                result_data = result_data[~np.isnan(result_data)]

                # max value for histogram
                max_value_time_index = np.nanargmax(result_data)
                max_value = result_data[max_value_time_index]
                percentile_values.append(max_value)

        # percentile calculation
        percentile_values = sorted(percentile_values)
        if selection_tension_compression == UniversalLimit.TENSION_COMPRESSION_VALUES[2]:
            # compression, flip array to descending order
            percentile_values.reverse()

        value_size = len(percentile_values)
        percentile_value = float(percentile)

        percentile_upper_limit = 1 - (1 / element_count)
        if percentile_value <= percentile_upper_limit:
            percentile_limit = percentile_values[int(np.ceil(percentile_value * value_size))]
        else:
            percentile_limit = percentile_values[int(np.ceil(percentile_upper_limit * value_size))]

        return percentile_limit

    @staticmethod
    def object_strain_stress_hist(object_data: dict, limit: float, selection_tension_compression: str,
                                  integration_point: str, bins: int, units):
        """
        :param object_data:
        :param limit:
        :param selection_tension_compression:
        :param integration_point:
        :param bins:

        :return:
        """

        part_ids = object_data["part_ids"]
        part_data = object_data["part_data"]
        part_idx = object_data["part_idx"]

        # limit = param_dict[PluginsParamDictDef.LIMIT]
        # selection_tension_compression = param_dict[PluginsParamDictDef.SELECTION_TENSION_COMPRESSION]
        # integration_point = param_dict[PluginsParamDictDef.INTEGRATION_POINT]

        obj_calc = ObjectCalcUtil()
        (function_overall_tension_compression, integration_point_function) = \
            obj_calc.retrieve_functions(selection_tension_compression, integration_point)

        histogram_data = [0] * (bins + 1)
        for part_id in part_ids:
            index = part_idx[part_id]
            data = part_data[part_id]
            element_ids = np.unique(index[:, 0])

            for element_id in element_ids:
                row_ids = np.where(index[:, 0] == element_id)[0]

                reduced_integration_point_data = integration_point_function(data[:, row_ids, :], axis=1)
                result_data = function_overall_tension_compression(reduced_integration_point_data, axis=1)
                result_data = result_data[~np.isnan(result_data)]

                # max value for histogram
                max_value_time_index = np.nanargmax(result_data)
                max_value = result_data[max_value_time_index]

                histogram_index = min(bins, int(bins * max_value / limit))
                histogram_data[histogram_index] += 1

        return np.array([histogram_data]).reshape(-1, 1)

    # @staticmethod
    # def surface_strain(object_data: dict, units):
    #
    #     part_ids = object_data["part_ids"]
    #     part_data = object_data["part_data"]
    #     part_idx = object_data["part_idx"]
    #
    #     for part_id in part_ids:
    #         index = part_idx[part_id]
    #         data = part_data[part_id]
    #         element_ids = np.unique(index[:, 0])
    #         for element_id in element_ids:
    #             row_ids = np.where(index[:, 0] == element_id)[0]
    #
    #             reduced_integration_point_data = data[:, row_ids, :]
    #
    #             a = 0

    @staticmethod
    def osccar_rib_criteria(object_data: dict, nr_largest_elements: int, age: float, risk_curve, units):
        """

        :param object_data:
        :param nr_largest_elements:
        :param age:
        :param risk_curve:

        :return histogram probability broken ribs:
        """
        part_ids = object_data["part_ids"]
        part_data = object_data["part_data"]
        part_idx = object_data["part_idx"]

        rib_criteria = RibCriteria(risk_curve)
        smax = {}
        element_count = 0

        # NOTE
        # compare with universal controller
        # calculate mean for the main directions ... maybe
        # maximum value for all timesteps
        # maximum over the time!
        for part_id in part_ids:
            abs_max_all = np.empty(shape=(0, 2))
            index = part_idx[part_id]
            data = part_data[part_id]
            element_ids = np.unique(index[:, 0])
            element_count += len(element_ids)

            for element_id in element_ids:
                row_ids = np.where(index[:, 0] == element_id)[0]
                reduced_integration_point_data = np.mean(data[:, row_ids, :], axis=1)
                result_data = np.max(reduced_integration_point_data, axis=1)
                try:
                    res = np.max(np.abs(result_data[~np.isnan(result_data)]))
                except ValueError:
                    res = 0
                abs_max_all = np.concatenate((abs_max_all, [[res, element_id]]), axis=0)

            ind_of_largest_elements = abs_max_all[:, 0].argsort()[-nr_largest_elements:][::-1]
            max_index = ind_of_largest_elements[-1]

            abs_max_value = abs_max_all[max_index][0]
            if np.isnan(abs_max_value):
                print(LOGConstants.WARNING[0],
                      "Due to deleted elements, the maximum Value for " + str(part_id) + " is NaN!")

            smax[part_id] = abs_max_value

        rib_ids = list(smax.keys())

        risk = {id: rib_criteria.calculate_age_risk(smax[id], age) for id in rib_ids}
        broken_ribs_prob = np.array(rib_criteria.calc_num_frac(rib_ids, risk))

        return broken_ribs_prob

    @staticmethod
    def forman_rib_criteria(object_data: dict, nr_largest_elements: int, age: float, dcdf, units):
        """

        :param object_data:
        :param nr_largest_elements:
        :param age:
        :param risk_curve:
        :return:
        """

        part_ids = object_data["part_ids"]
        part_data = object_data["part_data"]
        part_idx = object_data["part_idx"]

        dcdf = DCDF(dcdf)
        rib_criteria = RibCriteria(dcdf)
        smax = {}
        element_count = 0

        # NOTE
        # compare with universal controller
        # calculate mean for the main directions ... maybe
        # maximum value for all timesteps
        # maximum over the time!
        for part_id in part_ids:
            abs_max_all = np.empty(shape=(0, 2))
            index = part_idx[part_id]
            data = part_data[part_id]
            element_ids = np.unique(index[:, 0])
            element_count += len(element_ids)

            for element_id in element_ids:
                row_ids = np.where(index[:, 0] == element_id)[0]
                reduced_integration_point_data = np.mean(data[:, row_ids, :], axis=1)
                result_data = np.max(reduced_integration_point_data, axis=1)

                try:
                    res = np.max(np.abs(result_data[~np.isnan(result_data)]))
                except ValueError:
                    res = 0
                abs_max_all = np.concatenate((abs_max_all, [[res, element_id]]), axis=0)

            ind_of_largest_elements = abs_max_all[:, 0].argsort()[-nr_largest_elements:][::-1]
            max_index = ind_of_largest_elements[-1]

            abs_max_value = abs_max_all[max_index][0]
            if np.isnan(abs_max_value):
                print(LOGConstants.WARNING[0],
                      "Due to deleted elements, the maximum Value for " + str(part_id) + " is NaN!")

            smax[part_id] = abs_max_value

        rib_ids = list(smax.keys())

        risk = {id: rib_criteria.calculate_age_risk(smax[id], age) for id in rib_ids}
        broken_ribs_prob = np.array(rib_criteria.calc_num_frac(rib_ids, risk))

        return broken_ribs_prob

    @staticmethod
    def forman_age_correction(us: np.ndarray, age: int, units):
        """

        :param us:
        :param age:
        :param units:
        :return:
        """

        sus = 100. * (us / (1.0 - (age - 25.) * 0.0051))
        return sus

    @staticmethod
    def binom(risk: np.ndarray, max_broken_ribs: int, units):
        """

        :param param_dict:
        :param units:
        :return:
        """
        import itertools

        rib_ids = np.arange(len(risk))
        sf = []
        for f in range(max_broken_ribs):
            s = 0.0
            # for i in itertools.permutations(a,f):
            for i in itertools.combinations(rib_ids, f):
                p1 = 1.0
                for j in i:
                    p1 = p1 * risk[j]

                p2 = 1.0
                for k in np.setdiff1d(np.array(rib_ids), np.array(i)):
                    p2 = p2 * (1.0 - risk[k])

                s = s + p1 * p2
            sf.append(s)
        sf.append(1 - np.sum(sf))

        #sf = []
        #for f in range(12):
        #    s = 0.0
        #    for i in itertools.combinations(rib_ids, f):
        #        i_list = list(i)
        #        p1 = np.prod(risk[i_list])
        #        xy = np.setdiff1d(rib_ids, i_list)
        #        p2 = np.prod((1.0 - risk[xy]))

        #        s = s + p1 * p2
        #    sf.append(s)
        #sf.append(1 - np.sum(sf))

        return np.array(sf)

    @staticmethod
    def ecdf(x: np.ndarray, steps: np.ndarray, units):

        x_step = np.asarray(steps)[:, 0]
        x_step[0] = -np.Inf
        prob = np.asarray(steps)[:, 1]

        return np.array([prob[np.where(value > x_step)][-1] for value in x])

    @staticmethod
    def stress_strain_part_max(object_data: dict, selection_tension_compression: str, integration_point: str,
                               nr_largest_elements: float, units):
        """

        :param object_data:
        :param selection_tension_compression:
        :param integration_point:
        :return:
        """
        part_ids = object_data["part_ids"]
        part_data = object_data["part_data"]
        part_idx = object_data["part_idx"]

        obj_calc = ObjectCalcUtil()
        (function_overall_tension_compression, integration_point_function) = \
            obj_calc.retrieve_functions(selection_tension_compression, integration_point)
        part_max_elment = {}

        for part_id in part_ids:
            max_elem = np.empty(shape=(0, 2))

            index = part_idx[part_id]
            data = part_data[part_id]
            element_ids = np.unique(index[:, 0])

            for i, element_id in enumerate(element_ids):
                row_ids = np.where(index[:, 0] == element_id)[0]
                reduced_integration_point_data = integration_point_function(data[:, row_ids, :], axis=1)
                result_data = function_overall_tension_compression(reduced_integration_point_data, axis=1)
                result_data = result_data[~np.isnan(result_data)]

                max_value_time_index = np.nanargmax(result_data)
                max_value = result_data[max_value_time_index]
                max_elem = np.concatenate((max_elem, [[max_value, element_id]]), axis=0)

            ind_of_largest_elements = max_elem[:, 0].argsort()[-nr_largest_elements:][::-1]
            max_index = ind_of_largest_elements[-1]

            part_max_elem_value = max_elem[max_index][0]
            if np.isnan(part_max_elem_value):
                print(LOGConstants.WARNING[0],
                      "Due to deleted elements, the maximum Value for " + str(part_id) + " is NaN!")

            part_max_elment[part_id] = max_elem[max_index]

        return np.array([part_max_elment[i][0] for i in part_max_elment])

    @staticmethod
    def stress_strain_time_history(object_data: dict, selection_tension_compression: str, integration_point: str,
                               percentile: float, interpolation:str, units):
        """

        :param object_data: data container for parts of the defined object
        :param selection_tension_compression: selection how principle components are treated
        :param integration_point: selection how integration points are treated
        :param percentile: percentile caclulation of the resulting data_matrix (time x nr_elements in object), for each
        timestep the nth percentile value is returned
        :param interpolation: percentile calculation

        :return: percentile element value over time
        """

        part_ids = object_data["part_ids"]
        part_data = object_data["part_data"]
        part_idx = object_data["part_idx"]

        obj_calc = ObjectCalcUtil()
        (function_overall_tension_compression, integration_point_function) = \
            obj_calc.retrieve_functions(selection_tension_compression, integration_point)

        element_data = np.empty((len(object_data["time"]),0))
        for idx, part_id in enumerate(part_ids):
            data = part_data[part_id]
            index = part_idx[part_id]
            element_ids = np.unique(index[:, 0])
            part_elem_data = np.empty(shape=(len(element_ids), len(object_data["time"])))
            for elem_idx, element_id in enumerate(element_ids):
                row_ids = np.where(index[:, 0] == element_id)[0]
                reduced_integration_point_data = integration_point_function(data[:, row_ids, :], axis=1)
                result_data = function_overall_tension_compression(reduced_integration_point_data, axis=1)
                part_elem_data[elem_idx] = result_data
            element_data = np.hstack((element_data, part_elem_data.T))

        element_data = element_data.T

        return np.nanpercentile(element_data, percentile, interpolation=interpolation, axis=0) # element_data[np.arange(element_data.shape[0]), column_index_of_n_highest]



    @staticmethod
    def object_time(object_data: dict, units):
        """

        :param object_data:
        :return:
        """

        return object_data["time"]

    @staticmethod
    def csdm(object_data: dict, limit: float, units):
        """
        :param object_data:
        :param limit:
        :return:
        """

        part_ids = object_data["part_ids"]
        part_data = object_data["part_data"]
        part_idx = object_data["part_idx"]
        volume_data = object_data["part_value"]
        element_volume_by_part_id_and_element_id = object_data["el_by_part_id_el_id"]

        limit = float(limit) if 0.0 < float(limit) < 1.0 else 0.2
        injvol = 0.0
        sumvol = 0.0

        for part_id in part_ids:
            index = part_idx[part_id]
            data = part_data[part_id]
            part__volume = volume_data[part_id]

            # calculate csdm
            # absolute maximum over all time steps for each element
            abs_max_all = np.max(np.max(np.abs(data), axis=2), axis=0)
            # get element ids which are greater than the limit
            element_ids_greater_limit = index[np.where(abs_max_all > limit)[0], 0]

            csdm = 0.0
            if len(element_ids_greater_limit) != 0:
                volumes = [element_volume_by_part_id_and_element_id[part_id][element_id] for
                           element_id in
                           element_ids_greater_limit]
                csdm = sum(volumes) / part__volume

            sumvol += part__volume
            injvol += (part__volume * csdm)

        csdm = injvol / sumvol
        return csdm

    @staticmethod
    def BrIC(r_vel: np.ndarray, crit_rx_velocity: float, crit_ry_velocity: float, crit_rz_velocity: float, units):
        """

        :param r_vel:
        :param crit_rx_velocity: # [rad/s]
        :param crit_ry_velocity:   [rad/s]
        :param crit_rz_velocity:   [rad/s]
        :param units:
        :return:
        """
        r_vel *= units.second()
        bric = np.linalg.norm([np.max(np.abs(r_vel[:, 0])) / crit_rx_velocity,
                               np.max(np.abs(r_vel[:, 1])) / crit_ry_velocity,
                               np.max(np.abs(r_vel[:, 2])) / crit_rz_velocity])

        return bric

    @staticmethod
    def uBRIC(r_vel: np.ndarray, r_acc: np.ndarray, crit_rx_velocity: float, crit_ry_velocity: float,
              crit_rz_velocity: float, crit_rx_acceleration: float, crit_ry_acceleration: float,
              crit_rz_acceleration: float, units):
        """

        :param r_vel:
        :param r_acc:
        :param crit_rx_velocity:        # [rad/s]
        :param crit_ry_velocity:        # [rad/s]
        :param crit_rz_velocity:        # [rad/s]
        :param crit_rx_acceleration:    # [rad/s^2]
        :param crit_ry_acceleration:    # [rad/s^2]
        :param crit_rz_acceleration:    # [rad/s^2]
        :param units:
        :return:
        """

        r_vel = r_vel * units.second()
        r_acc = r_acc * (units.second() ** 2)

        # absolute max. of r_vel and r_acc normalized
        wx = np.max(np.abs(r_vel[:, 0])) / crit_rx_velocity
        wy = np.max(np.abs(r_vel[:, 1])) / crit_ry_velocity
        wz = np.max(np.abs(r_vel[:, 2])) / crit_rz_velocity
        ax = np.max(np.abs(r_acc[:, 0])) / crit_rx_acceleration
        ay = np.max(np.abs(r_acc[:, 1])) / crit_ry_acceleration
        az = np.max(np.abs(r_acc[:, 2])) / crit_rz_acceleration

        ubric = ((wx + (ax - wx) * np.exp(-(ax / wx))) ** 2 + (wy + (ay - wy) * np.exp(-(ay / wy))) ** 2 + (
                wz + (az - wz) * np.exp(-(az / wz))) ** 2) ** (1 / 2)

        return ubric

    @staticmethod
    def vc(y: np.ndarray, time: np.ndarray, scaling_factor: float, deformation_constant: float, units):
        """

        :param y:
        :param time:
        :param scaling_factor:
        :param deformation_constant:
        :param units:
        :return:
        """

        scfa = scaling_factor
        defconst = deformation_constant
        y = y / units.meter()
        t = time / units.second()

        delta_t = t[1] - t[0]

        # vc derivative
        deformation_velocity = np.zeros(len(t))
        for i in range(2, len(t) - 2):
            deformation_velocity[i] = (8 * (y[i + 1] - y[i - 1]) - (y[i + 2] - y[i - 2]))

        deformation_velocity[0] = (8 * (y[1] - y[0]) - (y[2] - y[0]))
        deformation_velocity[1] = (8 * (y[2] - y[0]) - (y[3] - y[0]))
        deformation_velocity[-2] = (8 * (y[-1] - y[-3]) - (y[-1] - y[-4]))
        deformation_velocity[-1] = (8 * (y[-1] - y[-2]) - (y[-1] - y[-3]))

        deformation_velocity /= (12 * delta_t)
        vc = np.multiply(scfa * (y / defconst), deformation_velocity.reshape(-1, 1))

        return vc

    @staticmethod
    def nij(force_x: np.ndarray, force_z: np.ndarray, moment_y: np.ndarray, distance_occipital_condyle: float,
            nij_fzc_te: float, nij_fzc_co: float, nij_myc_fl: float, nij_myc_ex: float, units):
        """

        :param force_x:
        :param force_z:
        :param moment_y:
        :param distance_occipital_condyle:
        :param nij_fzc_te:
        :param nij_fzc_co:
        :param nij_myc_fl:
        :param nij_myc_ex:
        :param units:
        :return:
        """
        force_x = force_x / (units.meter() / (units.second() ** 2))
        force_z = force_z / (units.meter() / (units.second() ** 2))
        moment_y = moment_y / ((units.meter() ** 2) / (units.second() ** 2))

        moc_d = distance_occipital_condyle  # m
        nij_fzc_te = nij_fzc_te  # N
        nij_fzc_co = nij_fzc_co  # N
        nij_myc_fl = nij_myc_fl  # Nm
        nij_myc_ex = nij_myc_ex  # Nm

        nij = np.zeros(shape=(len(force_z)))
        temp_n_value = np.zeros(shape=(4,))

        moc = moment_y - moc_d * force_x

        for o in range(len(force_z)):
            # NCF
            temp_n_value[0] = force_z[o] / nij_fzc_co + moc[o] / nij_myc_fl if force_z[o] <= 0 and moc[o] > 0 else 0
            # NCE
            temp_n_value[1] = force_z[o] / nij_fzc_co + moc[o] / nij_myc_ex if force_z[o] <= 0 and moc[o] <= 0 else 0
            # NTF
            temp_n_value[2] = force_z[o] / nij_fzc_te + moc[o] / nij_myc_fl if force_z[o] > 0 and moc[o] > 0 else 0
            # NTE
            temp_n_value[3] = force_z[o] / nij_fzc_te + moc[o] / nij_myc_ex if force_z[o] > 0 and moc[o] <= 0 else 0

            nij[o] = np.max(temp_n_value)
            temp_n_value = np.zeros(shape=(4,))

        return nij.reshape((-1, 1))

    @staticmethod
    def a3ms(time: np.ndarray, a_res: np.ndarray, units):
        """
        :param time:
        :param a_res:
        :param units:
        :return:
        """

        time = time.flatten()  # t in [s]
        a_res = a_res.flatten()
        # TODO
        # implementation in a central point
        t = time / units.second()
        a_res /= units.meter() / (units.second() ** 2)
        a_res /= units.grav_const

        ls_ind = []
        last = 0  # possible because time is ascending!
        for i in range(len(t)):
            if last == len(t) - 1:
                ls_ind.append((i, last + 1))
                # continue

            for j in range(last, len(t)):
                if t[j] - t[i] > 0.003:  # found start stop indices
                    ls_ind.append((i, j))
                    last = j
                    break

        a3ms_values = np.array([np.min(a_res[ind_tuple[0]:ind_tuple[1]]) for ind_tuple in ls_ind])
        return a3ms_values.reshape((-1, 1))
