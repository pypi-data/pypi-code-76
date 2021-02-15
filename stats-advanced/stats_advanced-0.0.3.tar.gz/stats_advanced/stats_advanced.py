import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class Mean:
    def __init__(self, data, x_col, f_col):
        self.data = data
        self.x_col = x_col
        self.f_col = f_col

    def __get_ci_list(self):
        """
        For internal use only
        Splits the x_col using the "-" separator
        :return:
        lower: list containing the lower bounds of the class interval
        upper: list containing the upper bounds of the class interval
        mid_values: list containing the mid values of the class interval
        frequency: list containing the frequency of the class interval
        """
        ci_list = list(self.data[self.x_col].str.split("-"))
        lower = [int(sublist[0]) for sublist in ci_list]
        upper = [int(sublist[1]) for sublist in ci_list]
        mid_values = [(lower_val + upper_val) / 2 for lower_val, upper_val in zip(lower, upper)]
        frequency = self.data[self.f_col].values
        return lower, upper, mid_values, frequency

    def calculate_mean_from_ci(self):
        """
        For internal use only
        Calculates the mean from class intervals
        :return:
        mean: The mean of all the values calculated by using the formula sum(f*mid)/sum(f)
        """
        lower, upper, mid_values, frequency = self.__get_ci_list()
        mean = sum([(mid * f) for mid, f in zip(mid_values, frequency)]) / sum(frequency)
        return mean

    def print_mean_df(self):
        """
        Prints the dataframe with all the necessary details for calculating the mean
        """
        lower, upper, mid_values, frequency = self.__get_ci_list()
        final_df = pd.DataFrame()
        final_df['X'] = self.data[self.x_col]
        final_df['F'] = self.data[self.f_col]
        final_df['Mid'] = mid_values
        final_df['F*Mid'] = [(mid * f) for mid, f in zip(mid_values, frequency)]
        return final_df

    def print_mean_from_ci(self):
        """
        Prints the mean of the data with all the necessary details
        """
        mean = self.calculate_mean_from_ci()
        lower, upper, mid_values, frequency = self.__get_ci_list()
        df = self.print_mean_df()
        print("The mean for the given data series is")
        print(df)
        print("\n")
        print(f"The cumulative frequency is {sum(frequency)}")
        print(f"The sum of f*mid is {sum([(mid * f) for mid, f in zip(mid_values, frequency)])}")
        print(f"The mean is {mean}")

    def __get_list_discrete(self):
        """
        For internal use only
        Stores the values in the _col, frequency and the product of x*f in separate lists
        :return:
        x_values: List containing the values in x_col
        f_values: List containing the values in f_col
        prod_list: List containing the product of the values in f_col and x_col
        """
        x_values = self.data[self.x_col].values
        f_values = self.data[self.f_col].values
        prod_list = [x * f for x, f in zip(x_values, f_values)]
        return x_values, f_values, prod_list

    def calculate_mean_discrete(self):
        """
        For internal use only
        Calculates the mean of discrete series by using the formula sum(f*x)/sum(f)
        :return:
        mean: The mean of the discrete series
        """
        x_values, f_values, prod_list = self.__get_list_discrete()
        mean = sum(prod_list) / sum(f_values)
        return mean

    def print_mean_discrete_df(self):
        """
        Prints the dataframe containing all the necessary information required for calculating mean
        """
        x_values, f_values, prod_list = self.__get_list_discrete()
        mean_discrete_df = pd.DataFrame()
        mean_discrete_df["X"] = self.data[self.x_col]
        mean_discrete_df["F"] = self.data[self.f_col]
        mean_discrete_df["F*X"] = prod_list
        return mean_discrete_df

    def print_mean_discrete(self):
        """
        Prints the mean of the discrete series with all the necessary details
        """
        mean = self.calculate_mean_discrete()
        x_values, f_values, prod_list = self.__get_list_discrete()
        mean_discrete_df = self.print_mean_discrete_df()
        print("The mean for the given data series is")
        print(mean_discrete_df)
        print("\n")
        print(f"The sum of f*x is {sum(prod_list)}")
        print(f"The sum of f is {sum(f_values)}")
        print(f"The mean is {mean}")
    @staticmethod
    def get_mean_individual(val_list):
        """
        For internal use only
        :param val_list: list of values in the individual series
        :return:
        mean: mean of the values in the individual series
        sum(val_list): The sum of the list passed to it
        len(val_list): The number of observations in the list passed to it
        """
        mean = sum(val_list)/len(val_list)
        return mean, sum(val_list), len(val_list)
    @staticmethod
    def print_mean_individual(val_list):
        """
        :param val_list: The list of values for which the mean has to be calculated
        Prints the mean of the individual series along with necessary details
        """
        mean, sum_data, len_data = Mean.get_mean_individual(val_list)
        print(f"The sum of all the observations in the series is {sum_data}")
        print(f"The number of observations is {len_data}")
        print(f"Hence the mean is {mean}")


class Median:
    def __init__(self, data, x_col, f_col):
        self.data = data
        self.x_col = x_col
        self.f_col = f_col

    def __get_lists(self):
        """
        For interval use
        Takes the x_col and splits it using the "-" separator
        :returns
        lower: list containing lower bounds of each class interval
        upper: list containing upper bounds of each class interval
        f_list: list containing frequency of each class interval
        cf_list: list containing cumulative frequency of each class interval
        """
        combined_list = list(self.data[self.x_col].str.split("-"))
        lower = [int(val[0]) for val in combined_list]
        upper = [int(val[1]) for val in combined_list]
        f_list = self.data[self.f_col].values
        cf_list = self.data[self.f_col].cumsum().values
        return lower, upper, f_list, cf_list

    def print_df(self):
        """
        Prints the dataframe containing X, F and CF columns
        """
        df = self.data
        df["CF"] = df[self.f_col].cumsum()
        print(df)

    def __find_median_continuous(self):
        """
        For internal use
        Calculates the median
        :returns
         concerned_n: The n for which the observation at that position should be considered while calculating median
         lower_val: The lower bound of the class interval which contains that particular observation
         cf_above: The cumulative frequency of class interval above the required class interval
         corresponding_f: The frequency of the required class interval
         ci: The class interval (given by the formula: upper_bound-lower_bound)
         median_value: The median of the given data
        """
        lower, upper, f_list, cf_list = self.__get_lists()
        cf = sum(f_list)
        concerned_n = (cf / 2)
        for i in range(1, len(cf_list) - 1):
            if cf_list[i - 1] <= concerned_n <= cf_list[i + 1]:
                idx = i
        lower_val = lower[idx]
        cf_above = cf_list[idx - 1]
        corresponding_f = f_list[idx]
        ci = upper[0] - lower[0]
        median_value = lower_val + (((concerned_n - cf_above) / corresponding_f) * (ci))
        return concerned_n, lower_val, cf_above, corresponding_f, ci, median_value

    def return_median_continuous(self):
        concerned_n, lower_val, cf_above, corresponding_f, ci, median_value = self.__find_median_continuous()
        return median_value

    def __find_quartiles(self):
        """
        For internal use
        Finds the first and the third quartile of the given data
        :returns
        n_q1: The position of the observation to be considered for Q1
        n_q3: The position of the observation to be considered for Q3
        lower_q1: The lower bound of the class interval containing the required observation for Q1
        lower_q3: The lower bound of the class interval containing the required observation for Q3
        cf_above_q1: The cf above the required class interval for Q1
        cf_above_q3: The cf above the required class interval for Q3
        f_corresponding_q1: The frequency for the corresponding class interval for Q1
        f_corresponding_q3: The frequency for the corresponding class interval for Q3
        ci: The class interval (given by the formula of upper_bound-lower_bound)
        q1: The first quartile for the given distribution
        q3: The third quartile for the given distribution
        """
        lower, upper, f_list, cf_list = self.__get_lists()
        cf = sum(f_list)
        n_q1 = (cf / 4)
        n_q3 = ((3 * cf) / 4)
        for i in range(1, len(cf_list) - 1):
            if cf_list[i - 1] <= n_q1 <= cf_list[i + 1]:
                idx_q1 = i
            elif cf_list[i - 1] <= n_q3 <= cf_list[i + 1]:
                idx_q3 = i
        lower_q1 = lower[idx_q1]
        cf_above_q1 = cf_list[idx_q1 - 1]
        f_corresponding_q1 = f_list[idx_q1]
        ci = upper[0] - lower[0]
        lower_q3 = lower[idx_q3]
        cf_above_q3 = cf_list[idx_q3 - 1]
        f_corresponding_q3 = f_list[idx_q3]
        q1 = lower_q1 + (((n_q1 - cf_above_q1) / f_corresponding_q1) * ci)
        q3 = lower_q3 + (((n_q3 - cf_above_q3) / f_corresponding_q3) * ci)
        return n_q1, n_q3, lower_q1, lower_q3, cf_above_q1, cf_above_q3, f_corresponding_q1, f_corresponding_q3, ci, q1, q3

    def print_median_continuous(self):
        """
        Prints the median of the distribution along with relevant details
        """
        concerned_n, lower_val, cf_above, corresponding_f, ci, median_value = self.__find_median_continuous()
        print(f"The n for median is {concerned_n}")
        print(f"The lower value of the class interval for median is {lower_val}")
        print(f"The cf above the required interval is {cf_above}")
        print(f"The frequency of the corresponding interval is {corresponding_f}")
        print(f"The class interval is {ci}")
        print(f"Hence the median according to the formula is {median_value}")

    def print_quartiles(self):
        """
        Prints the first and the third quartile of the distribution along with the relevant details
        """
        n_q1, n_q3, lower_q1, lower_q3, cf_above_q1, cf_above_q3, f_corresponding_q1, f_corresponding_q3, ci, q1, q3 = self.__find_quartiles()
        print("For Q1")
        print(f"The n for Q1 is {n_q1}")
        print(f"The lower bound of the interval for Q1 is {lower_q1}")
        print(f"The cf above the interval for Q1 is {cf_above_q1}")
        print(f"The corresponding frequency for Q1 is {f_corresponding_q1}")
        print(f"The class interval for Q1 is {ci}")
        print(f"Hence the value of Q1 is {q1}")
        print("\n")
        print("For Q3")
        print(f"The n for Q3 is {n_q3}")
        print(f"The lower bound of the interval for Q3 is {lower_q3}")
        print(f"The cf above the interval for Q3 is {cf_above_q3}")
        print(f"The corresponding frequency for Q3 is {f_corresponding_q3}")
        print(f"The class interval for Q3 is {ci}")
        print(f"Hence the value of Q3 is {q3}")

    def __get_list_discrete(self):
        """
        For internal use only
        returns:
        x_val: The values in the x_col
        f_val: The values in the f_col
        cf_val: The cumulative frequency
        """
        x_val = self.data[self.x_col].values
        f_val = self.data[self.f_col].values
        cf_val = self.data[self.f_col].cumsum().values
        return x_val, f_val, cf_val

    def __get_median_discrete(self):
        """
        For internal use only
        Returns:
        The median of the discrete data series
        """
        x, f, cf_col = self.__get_list_discrete()
        required_n = (sum(f) + 1) / 2
        for i in range(1, len(cf_col) - 1):
            if cf_col[i - 1] <= required_n <= cf_col[i + 1]:
                index = i
        median_value = x[index]
        return median_value

    def print_median_discrete(self):
        """
        Prints the median for discrete data series
        """
        x, f, cf_col = self.__get_list_discrete()
        print(f"The cumulative frequency is {sum(cf_col)}")
        print(f"The required observation is at position {(sum(f) + 1) / 2}")
        print(f"The median (observation at the position) is {self.__get_median_discrete()}")

    def __get_quartiles_discrete(self):
        """
        For internal use only
        Returns:
        q1_value: First quartile of discrete data series
        q3_value: Third quartile of discrete data series
        """
        x, f, cf_col = self.__get_list_discrete()
        n_q1 = (sum(f) + 1) / 4
        n_q3 = ((3 * sum(f)) + 1) / 4
        for i in range(1, len(cf_col) - 1):
            if cf_col[i - 1] <= n_q1 <= cf_col[i + 1]:
                index_q1 = i
            elif cf_col[i - 1] <= n_q3 <= cf_col[i + 1]:
                index_q3 = i
        q1_value = x[index_q1]
        q3_value = x[index_q3]
        return q1_value, q3_value

    def print_quartiles_discrete(self):
        """
        Prints the quartiles with necessary information
        """
        x, f, cf_col = self.__get_list_discrete()
        q1, q3 = self.__get_quartiles_discrete()
        print(f"The cumulative frequency is {sum(f)}")
        print(f"The position of element of first quartile is {(sum(f) + 1) / 4}")
        print(f"The first quartile (element at this position) is {q1}")
        print("\n")
        print(f"The position of element of third quartile is {((3 * sum(f)) + 1) / 4}")
        print(f"The third quartile (element at this position) is {q3}")

    def __get_lists_open_ended(self):
        """
        For internal use only
        Returns:
        lower: Lower bound of the class intervals of the open ended series
        upper: Upper bound of the class intervals of the open ended series
        frequency: Frequency of the class intervals of the open ended series
        cf: Cumulative frequency of the class intervals of the open ended series
        """
        x_list = self.data[self.x_col].values
        x_list_new = x_list[1:-1]
        split_list = [val.split("-") for val in x_list_new]
        lower = [int(val[0]) for val in split_list]
        upper = [int(val[1]) for val in split_list]
        frequency = self.data[self.f_col].values
        cf = self.data[self.f_col].cumsum().values
        return lower, upper, frequency, cf

    def __get_quartiles_open_ended(self):
        """
        For internal use only
        Returns:
        The first, second and the third quartiles of the open ended series
        """
        lower, upper, frequency, cf = self.__get_lists_open_ended()
        cf_val = frequency.sum()
        n_q1 = cf_val / 4
        n_q2 = cf_val / 2
        n_q3 = 3 * cf_val / 4
        for i in range(1, len(cf) - 1):
            if cf[i - 1] <= n_q1 <= cf[i + 1]:
                idx_q1 = i
            elif cf[i - 1] <= n_q2 <= cf[i + 1]:
                idx_q2 = i
            elif cf[i - 1] <= n_q3 <= cf[i + 1]:
                idx_q3 = i
        lower_q1 = lower[idx_q1 - 1]
        lower_q2 = lower[idx_q2 - 1]
        lower_q3 = lower[idx_q3 - 1]
        q1_val = lower_q1 + (((n_q1) - cf[idx_q1 - 1]) / frequency[idx_q1]) * (upper[0] - lower[0])
        q2_val = lower_q2 + (((n_q2) - cf[idx_q2 - 1]) / frequency[idx_q2]) * (upper[0] - lower[0])
        q3_val = lower_q3 + (((n_q3) - cf[idx_q3 - 1]) / frequency[idx_q3]) * (upper[0] - lower[0])
        return q1_val, q2_val, q3_val

    def print_quartiles_open_ended(self):
        lower, upper, frequency, cf = self.__get_lists_open_ended()
        df = self.data
        df["CF"] = cf
        print(df)
        print("\n")
        q1, q2, q3 = self.__get_quartiles_open_ended()
        print(f"The value of Q1 is {q1}")
        print(f"The value of Q2 is {q2}")
        print(f"The value of Q3 is {q3}")

    def return_quartile_open_ended(self):
        q1_val, q2_val, q3_val = self.__get_quartiles_open_ended()
        return q1_val, q2_val, q3_val

class Mode:

    def __init__(self, data, x_col, f_col):
        self.data = data
        self.x_col = x_col
        self.f_col = f_col

    def __get_lists(self):
        """
        For internal use only
        Creates the lists required for calculating mode
        Returns:
        lower: A list containing the lower bound of the intervals
        upper: A list containing the upper bound of the intervals
        f_list: A list containing the frequency of the intervals
        """
        split_list = list(self.data[self.x_col].str.split("-"))
        lower = [int(sublist[0]) for sublist in split_list]
        upper = [int(sublist[1]) for sublist in split_list]
        f_list = list(self.data[self.f_col].values)
        return lower, upper, f_list

    def __find_mode_from_ci(self):
        """
        For internal use only
        Calculates the mode from class intervals
        Returns:
        mode: The mode of the series
        f1: f-f_upper of the series
        f2: f-f_lower of the series
        ci: The class innterval containing the mode
        idx_max: The index of the class interval containing the mode
        """
        lower, upper, f_list = self.__get_lists()
        idx_max = f_list.index(max(f_list))
        f1 = f_list[idx_max]-f_list[idx_max-1]
        f2 = f_list[idx_max]-f_list[idx_max+1]
        ci = upper[0]-lower[0]
        mode = lower[idx_max] + (f1/(f1+f2))*ci
        return mode, f1, f2, ci, idx_max

    def print_mode_from_ci(self):
        """
        Prints the mode of the continuous series with the necessary details
        Returns:
        None
        """
        mode, f1, f2, ci, idx_max = self.__find_mode_from_ci()
        lower, upper, f =  self.__get_lists()
        print(self.data)
        print("\n")
        print(f"The max frequency is {f[idx_max]}")
        print(f"F1 is {f1}")
        print(f"F2 is {f2}")
        print(f"The class interval is {ci}")
        print(f"The lower bound of class interval corresponding to max frequency is {lower[idx_max]}")
        print(f"Hence the mode is {mode}")


    def return_mode(self):
        """
        Returns all the necessary values required by other functions
        """
        mode, f1, f2, ci, idx_max = self.__find_mode_from_ci()
        return mode

    def __get_lists_discrete(self):
        """
        For internal use only
        Gets the list of x values and f values from the data
        Returns:
        x_values: The values contained in the x_col of the data
        f_values: The values contained in the f_col of the data
        """
        x_values = list(self.data[self.x_col].values)
        f_values = list(self.data[self.f_col].values)
        return x_values, f_values

    def find_mode_discrete(self):
        """
        For internal use only
        Calculates the mode of the discrete data series
        Returns:
        mode: Mode of the discrete data series
        """
        x, f = self.__get_lists_discrete()
        idx_max = f.index(max(f))
        mode = x[idx_max]
        return mode

    def print_mode_discrete(self):
        """
        Prints the mode of the discrete series with necessary details
        """
        x, f = self.__get_lists_discrete()
        mode = self.find_mode_discrete()
        print(self.data)
        print("\n")
        idx_max = f.index(max(f))
        print(f"The maximum frequency is {f[idx_max]}")
        print(f"Hence the mode corresponding to maximum frequency is {mode}")


class StandardDeviation:

    def __init__(self, data, x_col, f_col):
        self.data = data
        self.x_col = x_col
        self.f_col = f_col

    def __get_lists(self):
        """
        For internal use only
        Returns the lists required for further use
        :return:
        lower: List containing the lower bounds of all the class intervals in the data
        upper: List containing the upper bounds of all the class intervals in the data
        f_list: List containing the frequency of all the class intervals in the data
        mid_list: List containing the mid values of all the class intervals in the data
        """
        split_list = list(self.data[self.x_col].str.split("-"))
        lower = [int(sublist[0]) for sublist in split_list]
        upper = [int(sublist[1]) for sublist in split_list]
        f_list = self.data[self.f_col].values
        mid_list = [(low+up)/2 for low, up in zip(lower, upper)]
        return lower, upper, f_list, mid_list

    def __get_standard_deviation_cont(self):
        """
        For internal use only
        Calculates the standard deviation of the continuous data series
        :return:
        difference: List containing x-mean(x)
        squared_difference: List containing (x-mean(x))*2
        product_squared_difference: List containing f*(x-mean(x))*2
        standard_deviation: Standard deviation of the continous data series
        prod_list: List containing f*mid(x)
        """
        lower_list, upper_list, frequency_list, mid_values_list = self.__get_lists()
        prod_list = [mid*f for mid, f in zip(mid_values_list, frequency_list)]
        mean_mid = sum(prod_list)/sum(frequency_list)
        difference = [(x-mean_mid) for x in mid_values_list]
        squared_difference = [diff**2 for diff in difference]
        product_squared_difference = [f*((val - mean_mid)**2) for f, val in zip(frequency_list, mid_values_list)]
        variance = sum(product_squared_difference)/sum(frequency_list)
        standard_deviation = variance**(1/2)
        return difference, squared_difference, product_squared_difference, standard_deviation, prod_list

    def return_standard_deviation_cont(self):
        difference, squared_difference, product_squared_difference, standard_deviation, prod_list = self.__get_standard_deviation_cont()
        return standard_deviation

    def print_stdev_cont(self):
        """
        Prints the dataframe with necessary details for calculating the standard deviation of the data series along with the standard deviation
        """
        lower_value, upper_value, freq_value, mid_value = self.__get_lists()
        diff, sqdiff, prodsqdiff, stdev, prod_list= self.__get_standard_deviation_cont()
        df = self.data
        df["Mid"] = mid_value
        df["Prod"] = prod_list
        df["Diff"] = diff
        df["SqDiff"] = sqdiff
        df["ProdSqDiff"] = prodsqdiff
        print(df)
        print(f"The standard deviation is {stdev}")

    def __standard_deviation_discrete(self):
        """
        For internal use only
        Calculates the standard deviation of discrete series
        :return:
        diff_discrete: List containing x-mean(x)
        squared_diff_discrete: List containing (x-mean(x))**2
        product_discrete: List containing f*(x-mean(x))**2
        stdev_discrete: Standard deviation of discrete series
        prod_mean_discrete: List containing f*x
        """
        x_val_discrete = self.data[self.x_col].values
        f_val_discrete = self.data[self.f_col].values
        prod_mean_discrete = [x*f for x, f in zip(x_val_discrete, f_val_discrete)]
        mean_x_discrete = sum(prod_mean_discrete)/sum(f_val_discrete)
        diff_discrete = [x_discrete - mean_x_discrete for x_discrete in x_val_discrete]
        squared_difference_discrete = [val_discrete**2 for val_discrete in diff_discrete]
        product_discrete = [f_disc * sq_disc for f_disc, sq_disc in zip(f_val_discrete, squared_difference_discrete)]
        var_discrete = sum(product_discrete)/sum(f_val_discrete)
        stdev_discrete = var_discrete**(1/2)
        return diff_discrete, squared_difference_discrete, product_discrete, stdev_discrete, prod_mean_discrete

    def return_stdev_discrete(self):
        diff_discrete, squared_difference_discrete, product_discrete, stdev_discrete, prod_mean_discrete = self.__standard_deviation_discrete()
        return stdev_discrete

    def print_stdev_discrete(self):
        """
        Prints the dataframe containing necessary informnation for calculating the standard deviation of discrete series and the standard deviation of discrete series
        """
        diff_discrete, squared_difference_discrete, product_discrete, stdev_discrete, prod_mean_discrete = self.__standard_deviation_discrete()
        df_disc = self.data
        df_disc["F*X"] = prod_mean_discrete
        df_disc["difference"] = diff_discrete
        df_disc["squareddifference"] = squared_difference_discrete
        df_disc["product"] = product_discrete
        print(df_disc)
        print(f"The standard deviation is {stdev_discrete}")
    @staticmethod
    def __standard_deviation_individual(series):
        """
        For internal use only
        Calculates the standard deviation of individual series
        :param series: List of values for which standard deviation has to be calculated
        :return:
        diff_series: The series containing x-mean(x)
        sq_diff_series: The series containing (x-mean(x))**2
        stdev_individual: Standard deviation of individual series

        """
        mean_x_individual = sum(series)/len(series)
        diff_series =[x-mean_x_individual for x in series]
        sq_diff_series = [diff**2 for diff in diff_series]
        variance_individual = sum(sq_diff_series)/len(sq_diff_series)
        stdev_individual = variance_individual**(1/2)
        return diff_series, sq_diff_series, stdev_individual
    @staticmethod
    def print_stdev_individual(series):
        """
        Prints the dataframe containing the standard deviation of individual series along with the standard deviation of individual series
        :param series: List of values for which standard deviation has to be calculated
        """
        diff_series, sq_diff_series, stdev_individual = StandardDeviation.__standard_deviation_individual(series)
        stdev_individual_df = pd.DataFrame()
        stdev_individual_df["X"] = series
        stdev_individual_df["Difference"] = diff_series
        stdev_individual_df["Squared Difference"] = sq_diff_series
        print(stdev_individual_df)
        print(f"The standard deviation for this series is {stdev_individual}")


class Skewness:

    def __init__(self, data, x_col, f_col):
        self.data = data
        self.x_col = x_col
        self.f_col = f_col

    def __create_classes(self):
        """
        Creates instances of classes from above code required for finding skewness
        Returns:
        mean_class: Instance of Mean class
        median_class: Instance of Median class
        mode_class: Instance of Mode class
        standard_deviation_class: Instance of StandardDeviation class
        """
        mean_class = Mean(data=self.data, x_col=self.x_col, f_col=self.f_col)
        median_class = Median(data=self.data, x_col=self.x_col, f_col=self.f_col)
        mode_class = Mode(data=self.data, x_col=self.x_col, f_col=self.f_col)
        standard_deviation_class = StandardDeviation(data=self.data, x_col=self.x_col, f_col=self.f_col)
        return mean_class, median_class, mode_class, standard_deviation_class

    def __get_skewness_from_continuous(self):
        """
        Calculates the skewness of continuous series
        Returns:
        skewness: The skewness of the continous series
        mean_value: The mean of the continuous series
        mode_value: The mode of the continuous series
        standard_deviation_value: The standard deviation of the continuous series
        """
        mean_class, median_class, mode_class, standard_deviation_class = self.__create_classes()
        mean_value = mean_class.calculate_mean_from_ci()
        mode_value = mode_class.return_mode()
        standard_deviation_value = standard_deviation_class.return_standard_deviation_cont()
        skewness = (mean_value-mode_value)/standard_deviation_value
        return skewness, mean_value, mode_value, standard_deviation_value

    def __get_skewness_discrete(self):
        """
        Calculates the skewness of discrete series
        Returns:
        skewness: The skewness of the discrete series
        mean_discrete: The mean of the discrete series
        mode_discrete: The mode of the discrete series
        standard_deviation_discrete: The standard deviation of the discrete series
        """
        mean_class, median_class, mode_class, standard_deviation_class = self.__create_classes()
        mean_discrete = mean_class.calculate_mean_discrete()
        mode_discrete = mode_class.find_mode_discrete()
        standard_deviation_discrete = standard_deviation_class.return_stdev_discrete()
        skewness = (mean_discrete-mode_discrete)/standard_deviation_discrete
        return skewness, mean_discrete, mode_discrete, standard_deviation_discrete

    def __get_skewness_open_ended(self):
        """
        Calculates the skewness of open ended series
        Returns:
        skewness: The skewness of the open ended series
        q1: The first quartile of the open ended series
        q2: The second quartile of the open ended series
        q3: The third quartile of the open ended series
        """
        mean_class, median_class, mode_class, standard_deviation_class = self.__create_classes()
        q1, q2, q3 = median_class.return_quartile_open_ended()
        skewness = (q1+q3-(2*q2))/(q3-q1)
        return skewness, q1, q2, q3

    def print_skewness_continuous(self):
        """
        Prints the skewness of the continuous series with necessary details
        """
        skewness, mean_value, mode_value, standard_deviation_value = self.__get_skewness_from_continuous()
        print(f'The Mean of the continuous series is {mean_value}')
        print(f'The Mode of the continuous series is {mode_value}')
        print(f'The Standard Deviation value of the continuous series is {standard_deviation_value}')
        print(f'Hence the Skewness of the continuous series is {skewness}')

    def print_skewness_discrete(self):
        """
        Prints the skewness of the continuous series with necessary details
        """
        skewness, mean_discrete, mode_discrete, standard_deviation_discrete = self.__get_skewness_discrete()
        print(f'The Mean of the discrete series is {mean_discrete}')
        print(f'The Mode of the discrete series is {mode_discrete}')
        print(f'The Standard Deviation value of the discrete series is {standard_deviation_discrete}')
        print(f'Hence the Skewness of the discrete series is {skewness}')

    def print_skewness_open_ended(self):
        """
        Prints the skewness of the open ended series with necessary details
        """
        skewness, q1, q2, q3 = self.__get_skewness_open_ended()
        print(f'The value of the first quartile of the open ended series is {q1}')
        print(f'The value of the second quartile of the open ended series is {q2}')
        print(f'The value of the third quartile of the open ended series is {q3}')
        print(f'Hence the skewness of the series is {skewness}')


class UnivariateRegression:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate_coef(self):
        """
        This function calculates the regression coefficients based on the given data
        Inputs:
        data: a pandas dataframe on which you would like to perform regression analysis
        x_col: column name containing the independent variable
        y_col: column name containing the dependent variable
        Returns:
        The alpha and beta regression coefficients of regression
        """
        nrows = len(self.x)
        mean_x = self.x.mean()
        mean_y = self.y.mean()
        stdev_x = self.x.std(ddof=0)
        stdev_y = self.y.std(ddof=0)
        covariance = sum((x_val - mean_x) * (y_val - mean_y) for x_val, y_val in zip(self.x, self.y))/nrows
        correlation = covariance / (stdev_x * stdev_y)
        beta = correlation * (stdev_y / stdev_x)
        alpha = mean_y - beta * mean_x
        return alpha, beta

    def print_equation(self):
        """
        Prints the regression equation based on given data
        Inputs:
        None
        Returns:
        A f string containing the equation
        """
        alpha, beta = self.calculate_coef()
        return f"The equation is {alpha} + {beta}*x"

    def predict(self, x):
        """
        This function predicts the values using our regression model on a given series x
        Inputs:
        x: a series of data [type = numpy array or list]
        Returns:
        The list containing predictions based on our regression model
        """
        alpha, beta = self.calculate_coef()
        predictions = [alpha + beta*val for val in x]
        return predictions

    def standard_error(self):
        predictions = self.predict(self.x)
        y_values = self.y
        std_err = (sum([(y-pred)**2 for y, pred in zip(y_values, predictions)])/len(self.x))**(1/2)
        return std_err

    def plot_data(self, **kwargs):
        """
        This function plots the predictions from our regression model on a graph
        Inputs:
        x_col: The name of column that contains the independent variable
        y_col: The name of column that contains the dependent variable
        **kwargs: Other values like title, x-label,y-label,etc
        Returns:
        A matplotlib figure
        """
        predictions = self.predict(self.x)
        try:
            fig, ax = plt.subplots(figsize=kwargs['figsize'])
        except:
            fig, ax = plt.subplots()
        ax.scatter(self.x, self.y, label="Data Points")
        ax.plot(self.x, predictions, label="Regression Line")
        try:
            ax.set_xlabel(kwargs['xlabel'])
            ax.set_ylabel(kwargs['ylabel'])
            ax.set_title(kwargs['title'])
        except:
            pass
        ax.legend()
        return fig

    def compare(self, eqn=True, **kwargs):
        """
        This function compares our model to the most predominant libraries in python:
        SciKitLearn and StatsModels
        This function also shows a figure of predictions made by all three models in a separate comparitive plot
        Inputs:
        eqn: Prints the equations from all three models if True [default:True]
        **kwargs: Other arguments like figsize,etc
        Returns:
        A matplotlib figure and dictionary of equations
        """
        nrows = len(self.x)
        X_val = self.x.reshape(nrows, 1)
        y_val = self.y.reshape(nrows, 1)
        # own model
        pred = self.predict(self.x)
        # sklearn
        regressor = LinearRegression()
        regressor.fit(X_val,y_val)
        prediction_sklearn = regressor.predict(X_val)
        # statsmodels
        X_new = sm.add_constant(self.x)
        olsmod = sm.OLS(self.y, X_new)
        olsres = olsmod.fit()
        prediction_statsmodels = olsres.predict(X_new)
        # for labelling and neatness
        title_list = ["Regression using our own model",
                      "Regression using SciKitLearn",
                      "Regression using StatsModels"]
        label_list = ["Prediction by own model",
                      "Prediction by SciKitLearn",
                      "Prediction by StatsModels"]
        # storing predictions in a list
        prediction_list = [pred, prediction_sklearn, prediction_statsmodels]
        try:
            fig, ax = plt.subplots(figsize=kwargs['figsize'], nrows=1, ncols=3)
        except:
            fig, ax = plt.subplots(nrows=1, ncols=3)
        for i in range(3):
            ax[i].scatter(self.x, self.y, label="Data Points")
            ax[i].plot(self.x, prediction_list[i], label=label_list[i])
            ax[i].set_title(title_list[i])
            ax[i].set_xlabel("X")
            ax[i].set_ylabel("Y")
            ax[i].legend()
        plt.tight_layout()
        equations_dict = {"Own Model": f"{self.print_equation()}",
                          "SciKitLearn": f"{regressor.coef_[0][0]}+{regressor.intercept_[0]}*x",
                          "StatsModels": f"{olsres.params[0]}+{olsres.params[1]}*x"}
        if eqn:
            return fig, equations_dict
        else:
            return fig

    def find_r_squared(self):
        """
        Finds the R squared for the regression model
        :return:
        r_squared: The R squared for the regression model
        """
        predictions = self.predict(self.x)
        mean_pred = sum(predictions)/len(predictions)
        variance_pred = sum([(prediction - mean_pred)**2 for prediction in predictions])/len(predictions)
        variance_y = (self.y.std(ddof=0))**2
        r_squared = variance_pred/variance_y
        return r_squared

    def find_adjusted_r_squared(self):
        """
        Finds the adjusted R squared for the regression model
        :return:
        adjusted_r_squared: The adjusted R squared for the regression model
        """
        r_squared_value = self.find_r_squared()
        n = len(self.x)  # since it is a univariate linear regression
        n_predictors = 1  # since it is a univariate linear regression
        adjusted_r_squared_value = 1 - ((1 - r_squared_value) * (n - 1)) / (n - n_predictors - 1)
        return adjusted_r_squared_value


class MultiVariateRegression:
    def __init__(self,data):
        self.data = data
        self.x = np.array(self.data.iloc[:, :-1])
        self.y = np.array(data.iloc[:, -1:])

    def calculate_coef(self):
        """
        This function calculates the regression coefficients based on the given data
        Inputs:
        data: a pandas dataframe on which you would like to perform regression analysis
        Returns:
        The beta coefficient of regression
        """
        x_transpose = self.x.transpose()
        term1 = np.matmul(x_transpose, self.x)
        term1_inv = np.linalg.inv(term1)
        term2 = np.matmul(term1_inv, x_transpose)
        beta = np.matmul(term2, self.y)
        return beta

    def predict(self, x_list):
        """
        This function predicts the values using our regression model on a given series x
        Inputs:
        x: a series of data [type = numpy array or list]
        Returns:
        The list containing predictions based on our regression model
        """
        beta_value = self.calculate_coef()
        predictions = np.dot(x_list,beta_value)
        return predictions

    def calculate_r_squared(self):
        """
        Finds the R squared for the regression model
        :return:
        r_squared: The R squared for the regression model
        """
        predictions_own = self.predict(self.x)
        variance_predictions = np.var(predictions_own, ddof=0)
        variance_y = np.var(self.y, ddof=0)
        r_squared = variance_predictions/variance_y
        return r_squared

    def calculate_adjusted_r_squared(self):
        """
        Finds the adjusted R squared for the regression model
        :return:
        adjusted_r_squared: The adjusted R squared for the regression model
        """
        n_predictors = self.data.shape[1]-1
        r_squared_value = self.calculate_r_squared()
        n = self.data.shape[0]
        adjusted_r_squared_value = 1 - ((1 - r_squared_value) * (n - 1)) / (n - n_predictors - 1)
        return adjusted_r_squared_value

    def compare(self):
        """
        Compares our regression model with the StatsModels regression model
        """
        regressor = sm.OLS(self.y,self.x)
        fitted_regressor = regressor.fit()
        summary = fitted_regressor.summary()
        print(summary)
        results_own = self.calculate_coef()
        print(f"The coefficients by our method are{results_own}")
        r_squared = self.calculate_r_squared()
        print(f"The r-squared by our own method is {r_squared}")
        adjusted_r_squared = self.calculate_adjusted_r_squared()
        print(f"The adjusted r squared is {adjusted_r_squared}")
