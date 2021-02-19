from typing import List
from alpacka.functions import statistic_methods as s
from alpacka.functions import presentation_functions as pf


class ncof_pipeline:

    def __init__(self, num_words, class_perspective):
        self.Dot = 10
        self.Class_perspective = class_perspective
        self.Verbose = True
        self.num_words = num_words
    def print_all_methods(self):
        object_methods = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        print(object_methods)

    def set_num_words(self, new_val):
        self.num_words=new_val
    def get_num_words(self):
        return self.num_words
    #### Check input data type ####
    def check_data_type(self, data):
        """self function that checks if the input data type is known to be compatible with the remaining functions"""
        ok = ['list' , 'Series']
        if type(data).__name__ not in ok:
            raise TypeError(
                f"Input type ({type(data)}) not supported as an input. "
                f"Please format the input in on of the supported formats. "
                f"Supported formats: {ok}")

    #### calc_NCOF ####
    def calc_ncof(self, data: List[List[str]], labels: List[int], stop_words: List = None):
        """
        Calculates the NCOF score the the input data. Returns a list with a score and a dictionary of the data.
        The score for each index is associated with the word with the same index in the dictionary

        @param data: List[List[str]]
        @param labels: List[int]
        @param stop_words: List[str]
        @return: Score, Dict: List[float], dict
        """
        self.check_data_type(data)
        if stop_words != None: # removes the stop words pre calculating the NCOF score.
            new_data = []
            for sent in data:
                words = sent.split()
                for s_word in stop_words:
                    while s_word in words: words.remove(s_word)
                new_data.append(words)
            data = new_data
        score, self.dict = s.calc_NCOF_from_raw_data(data, labels, self.get_class_perspective(), self.num_words)
        if self.Verbose:
            print(f"NCOF score calculated successfully, no errors occured" )
        return score , self.dict

    ####
    # def get_score(self):
    #     """Returns the NCOF score for the object as a list"""
    #     return self.score

    ####
    def get_dict(self):
        """Returns the dictionary of the object as a dict"""
        return self.dict

    #### Split score ####
    def split_score(self, score):
        """splits the NCOF score into three categories based on the NCOF value for each element. Returns the element
        indexes corresponding to the following three categories. Inliers:      elements with NCOF score between mean
        +- 1 sigma, Pos_outliers: elements with NCOF score greater than mean +1 sigma, Neg_outliers: elements with
        NCOF score less than mean - 1 sigma. The outliers are returned as a list of lists where index 0 is the 1-2
        sigma outliers, index 1 is the 2-3 sigma outlers, and index 2 is 3-> outliers """
        inliers, pos_outliers, neg_outliers = pf.sigma_splitter(score)
        if self.Verbose:
            print(
                f"Score split successfully, no errors occured ")
        return inliers, pos_outliers, neg_outliers
    ####
    # def get_inliers(self):
    #     """Returns the NCOF inliers as a list"""
    #     return self.inliers

    ####
    # def get_pos_outliers(self):
    #     """Returns the Positive NCOF outliers as a list of lists"""
    #     return self.pos_outliers
    #
    # ####
    # def get_neg_outliers(self):
    #     """Returns the Negative NCOF outliers as a list of lists"""
    #     return self.neg_outliers

    ####

    #### indexes 2 words ####
    def ind_2_txt(self, list_of_list_of_list: list) -> List[List[List]]:
        """
        Transforms a list of integer indexes to their corresponding words in the objects dictionary, Returns a list
        of list of words
        @param list_of_list_of_list: List[List[List]] @return: words_all: List[List[List]]
        """
        words_all = []

        if len(list_of_list_of_list) == 3: # in input is pos or neg outliers
            for list in list_of_list_of_list:
                words = pf.ind_2_txt(list, self.dict)
                words_all.append(words)
            return words_all
        else: # if input is inliers
            return pf.ind_2_txt(list_of_list_of_list, self.dict)


    #### PLOT ####
    def scatter(self, score, inliers, pos_outliers, neg_outliers):
        """Creates a scatter plot of the NCOF score and parameters saved in the object"""
        pf.NCOF_plot(score, inliers, pos_outliers, neg_outliers,
                     self.get_dot(), self.get_class_perspective())

    #### PLOT histograms ####
    def plot_histogram(self, data=list, bins: int = None, x_label: str = None, y_label: str = None, title: str = None,
                       legend: List[str] = None):
        """
        Plots a histogram over the input data with the specified parameters
        @param data: list
        @param bins: int
        @param x_label: str
        @param y_label: str
        @param title: str
        @param legend: List[str]
        """
        pf.plot_histogram(data, bins, x_label, y_label, title, legend)
        if self.Verbose:
            print(f"Printing merged histograms")

    #### remove stop words ####
    def remove_stop_words(self, list_of_list: List[List[str]], stop_words: List[str]) -> List[List[str]]:
        """
        Removes stopwords from the input
        @param list_of_list: List[List[str]]
        @param stop_words: List[str]
        @return: words_all_no_stopwords: List[List[str]]
        """
        words_all_no_stopwords = []
        if len(list_of_list) == 3: # input is pos or neg outliers
            for lst in list_of_list:
                # words = []
                words = [w for w in lst if w not in stop_words]
                # words.append(a)
                words_all_no_stopwords.append(words)
            return words_all_no_stopwords
        else: # input is inliers
            return [w for w in list_of_list if w not in stop_words]

    #####  CONFIG  ###
    #### Verbose ####
    def get_verbose(self):
        """Returns the Verbose class variable"""
        return self.Verbose

    def set_verbose(self, bol: bool = False):
        """Sets the Verbose class variable"""
        self.Verbose = bol

    #### DOT ####
    def set_dot(self, new_val: int):
        """
        Sets the Dot class variable
        @param new_val: int
        """
        self.Dot = new_val

    ####
    def get_dot(self):
        """Returns the Dot class variable"""
        return self.Dot

    #### Class_perspective ####
    def set_class_perspective(self, new_val: int = 1):
        """
        Sets the Class_perspective class variable
        @param new_val: int, defult value 1
        """
        self.Class_perspective = new_val

    ####
    def get_class_perspective(self):
        """Returns the Class_perspective class variable"""
        return self.Class_perspective

    def get_result(self, score ,lst: List[List[list]], sort: bool = True):
        """
        prints the input text outliers to the terminal window with sorted into the sigma outlier
        @param lst: list
        @param sort: bool
        """
        if len(lst) == 3: # input is pos or neg outliers
            sigmas = ["1", "2", "3"]
            for outliers, sigma in zip(lst, sigmas):
                if sort:
                    for elm in lst:
                        elm.sort()
                    print(f"Printing {sigma}-sigma outliers, alphabetically sorted")
                else:
                    print(f"Printing {sigma}-sigma outliers")
                print(20 * "#")
                for word in outliers:
                    index = list(self.dict.values()).index(word)
                    print(f"{word}: {score[index]}")
                print(20 * "#")
        else: # input is inliers
            if sort:
                lst.sort()
                print(f"Printing inliers, alphabetically sorted")
            else:
                print(f"Printing inliers")
            print(20 * "#")
            for word in lst:
                index = list(self.dict.values()).index(word)
                print(f"{word}: {score[index]}")
            print(20 * "#")