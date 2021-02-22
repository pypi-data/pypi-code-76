import scipy.stats as stats
from scipy.stats import chi2_contingency

class ChiSquare:
    """"
    Chi-Square Test for Categorical Features.
    H0: No association between two variables.
    H1: There is evidence to suggest there is an association between two variables.

    Parameters
    ----------
    data: pd.DataFrame

    Examples
    --------
    >>> chi_test = ChiSquare(data)
    >>> chi_test.test(categorical_cols, "target")
    >>> important_cat_features = chi_test.get_important_features()
    >>> unimportant_cat_features = chi_test.get_unimportant_features()
    """
    def __init__(self, data):
        self.data = data
        self.p_value = None
        self.chi2 = None
        self.dof = None
        self.data_observed = None
        self.data_expected = None
        self.important_features = []
        self.unimportant_features = []

    def print_result(self, col, alpha=0.05):
        if self.p_value < alpha:
            # Reject null hypothesis H0
            print(f"{col} is an IMPORTANT feature.")
        else:
            # Accept null hypothesis H0
            print(f"{col} is NOT an IMPORTANT feature.")

    def get_result(self, col, alpha=0.05):
        if self.p_value < alpha:
            # Reject null hypothesis H0
            self.important_features.append(col)
        else:
            # Accept null hypothesis H0
            self.unimportant_features.append(col)

    def get_important_features(self):
        return self.important_features

    def get_unimportant_features(self):
        return self.unimportant_features

    def test(self, col_features, col_y, alpha=0.05):
        for col_x in col_features:
            X = self.data[col_x].astype(str)
            y = self.data[col_y].apply(lambda label: 0 if label==0.0 else 1).astype(str)

            self.data_observed = pd.crosstab(y, X)
            chi2, p_value, dof, expected = chi2_contingency(self.data_observed.values)
            self.chi2 = chi2
            self.p_value = p_value
            self.dof = dof
            self.data_expected = pd.DataFrame(
                expected,
                columns=self.data_observed.columns,
                index=self.data_observed.index)
            self.get_result(col_x, alpha)
            self.print_result(col_x, alpha)
