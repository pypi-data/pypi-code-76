# FIRST DRAFT OF FUNCTIONS
# ZONE PLANNING TEAM

class CurrentOperation:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @staticmethod
    def get_past_status(n_days):
        return n_days

    @staticmethod
    def get_cross_zone(city_code):
        city_code += " - City"
        return city_code


class Zonification(object):
    def __init__(self):
        self.name = "Zonification"

    def get_layout_kpi(self, df):
        columns = df.columns
        name = self.name
        # kpi = df.columns
        return columns, name


class DispatcherSearchParameters(object):
    def __init__(self):
        self.name = "Parameters"

    def get_current_parameters(self, city):
        name = self.name
        query = "SELECT "+city
        return query, name
