import numpy as np

class NumericOutlier:

    def _zscore(self, data = []):
        """
        remove outlier with z - score fomula
        (x - mean) / standard deviation
        """

        mean = np.mean(data)
        std = np.std(data)
        result = []
        
        # calculate z - score
        for i in range(0, len(data)):
            calculation = (data[i] - mean) / std
            if calculation > 2 or calculation < -2:
                result.append(data[i])
            
        return result

    def _iqr(self, data = []):
        """
        remove outlier with Interquartile Range Score
        iqr = Q3 - Q1
        min = Q1 - (1.5 * iqr)
        max = Q3 + (1.5 * iqr)
        """
        # sorting data

        x = data
        x.sort()

        # find Q1, Q2 and Q3

        q2 = np.median(x)
        q1 = np.median([x[i] for i in range(0, round(len(x) / 2) - 1)])
        q3 = np.median([x[i] for i in range(round(len(x) / 2), len(x))])

        # iqr
        iqr = q3 - q1

        # find outlier
        min_data = q1 - (1.5 * iqr)
        max_data = q1 + (1.5 * iqr)
        result = []

        for n in x:
            if n < min_data or n > max_data:
                result.append(n)
        
        return result

    def find(self, x = [], method=None):
        """
        remove outlier
        it take list parameter and method (zscore, iqr score)
        """
        if method != None:
            if method.lower() == "zscore":
                return self._zscore(x)
            else:
                return self._iqr(x)
        else:
            return ["Please tell me what kind of method do you want ? (zsocre, iqr)"]
