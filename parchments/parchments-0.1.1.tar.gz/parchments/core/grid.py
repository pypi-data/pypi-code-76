from parchments.core.row import Row
from parchments.core.period import Period
from parchments.core.choices import PERIOD_ITERATION_CHOICES, OVER_PERIOD_ITERATION_CHOICES
import json


class Grid:

    def __init__(self, row_index, period_iteration='month', over_period_iteration='year'):
        if period_iteration in PERIOD_ITERATION_CHOICES:
            self.period_iteration = period_iteration
        else:
            raise SyntaxError('Invalid period iteration choices %s' % PERIOD_ITERATION_CHOICES)

        if over_period_iteration in OVER_PERIOD_ITERATION_CHOICES:
            self.over_period_iteration = over_period_iteration
        else:
            raise SyntaxError('Invalid layer iteration choices %s' % OVER_PERIOD_ITERATION_CHOICES)

        self.row_index = row_index
        self.row_dict = dict()

        self.column_index = list()
        self.column_dict = dict()

        for row in self.row_index:
            self.row_dict[row[0]] = Row(row[0], row[1], row[2], self.period_iteration, self.over_period_iteration)

    def add_period(self, datetime, value_list):
        period = Period(datetime, self.period_iteration)

        self.column_index.append(period.key)
        self.column_index.sort()
        self.column_dict[period.key] = period

        if type(value_list) is list:
            for loop_index, row in enumerate(self.row_index):
                self.row_dict[row[0]].add_block(period, value_list[loop_index])

    def as_dict(self, verbose_only=False, sum=True, average=True, json_dump=False):
        grid_dict = dict()
        grid_dict['column_data'] = list()

        for column in self.column_index:
            grid_dict['column_data'].append(self.column_dict[column].as_dict(verbose_only, json_dump=json_dump))

        grid_dict['row_data'] = dict()

        for row in self.row_index:
            grid_dict['row_data'][row[0]] = self.row_dict[row[0]].as_dict(verbose_only, sum, average)

        return grid_dict

    def as_list(self, verbose_only=False):
        grid_list = list()
        grid_list.append(self.column_index)

        for row in self.row_index:
            grid_list.append(self.row_dict[row[0]].as_list())

        return grid_list

    def as_json(self, verbose_only=False):
        return json.dumps(self.as_dict(verbose_only, json_dump=True))

    def as_html(self):
        pass

    def get_row(self, row_index_key):
        if row_index_key in list(self.row_dict.keys()):
            return self.row_dict[row_index_key]
        else:
            raise ValueError('Invalid row index. Your choices are %s' % list(self.row_dict.keys()))

    def get_block(self, row_index_key, datetime):
        period = Period(datetime, self.period_iteration)

        if row_index_key in list(self.row_dict.keys()):
            return self.row_dict[row_index_key].get_block(period.key)
        else:
            raise ValueError('Invalid row index. Your choices are %s' % list(self.row_dict.keys()))

