#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

from typing import List
import uuid
import pandas as pd
import json
from copy import deepcopy
import uuid 


from mitosheet.steps import STEPS, STEP_TYPE_TO_STEP
from mitosheet.updates import UPDATES
from mitosheet.steps.initial_steps.initalize import execute_initialize_step
from mitosheet.steps.initial_steps.initial_rename import execute_initial_rename_step
from mitosheet.sheet_functions import FUNCTIONS
from mitosheet.utils import dfs_to_json, get_column_filter_type
from mitosheet.transpiler.transpile import transpile
from mitosheet.user.user_utils import get_user_field


class WidgetStateContainer():
    """
    Holds the state of the steps, which represents operations that
    have been performed on the input dataframes. 
    """

    def __init__(self, dfs: pd.DataFrame):
        # Just in case they are a tuple, make them a list - as it's easier to operate with.
        # We also make a copy so we don't modify the original dataframes.
        dfs = deepcopy(list(dfs))

        # We also save a copy of the initial dataframe's keys, for easy access
        self.original_df_keys = [df.keys() for df in dfs]

        # For now, we just randomly generate analysis names. 
        # We append a UUID to note that this is not an analysis the user has saved.
        self.analysis_name = 'UUID-' + str(uuid.uuid4())

        # We generate an initial rename step, which handles any issues with invalid headers
        # by converting them all to valid headers - which occurs before any formula step.
        dfs = execute_initial_rename_step(dfs)

        # Then we initialize the first initalize step
        self.steps = []
        execute_initialize_step(self, dfs)

    @property
    def curr_step_idx(self):
        """
        The ID of the current step
        """
        return len(self.steps) - 1

    @property
    def curr_step(self):
        """
        Returns the current step object as a property of the object,
        so reference it with self.curr_step
        """
        return self.steps[self.curr_step_idx]

    @property
    def num_sheets(self):
        """
        Duh. :)
        """
        return len(self.steps[self.curr_step_idx]['dfs'])

    @property
    def dfs(self) -> List[pd.DataFrame]:
        return self.steps[self.curr_step_idx]['dfs']

    @property
    def df_names_json(self):
        """
        A JSON object containing the names of the dataframes
        """
        return json.dumps({'df_names': self.curr_step['df_names']})

    @property
    def sheet_json(self):
        """
        sheet_json contains a serialized representation of the data
        frames that is then fed into the ag-grid in the front-end. 

        NOTE: we only display the _first_ 2,000 rows of the dataframe
        for speed reasons. This results in way less data getting 
        passed around
        """
        return dfs_to_json(self.curr_step['dfs'])
    
    @property
    def df_shape_json(self):
        """
        Returns the df shape (rows, columns) of each dataframe in the 
        current step!
        """
        return json.dumps([
            {'rows': df.shape[0], 'cols': df.shape[1]}
            for df in self.curr_step['dfs']
        ])

    @property
    def column_spreadsheet_code_json(self):
        """
        column_spreadsheet_code_json is a list of all the spreadsheet
        formulas that users have used, for each sheet they have. 
        """
        return json.dumps(self.curr_step['column_spreadsheet_code'])

    @property
    def code_json(self):
        """
        This code json string is sent to the front-end and is what
        ends up getting displayed in the codeblock. 
        """
        return json.dumps(transpile(self))

    @property
    def column_filters_json(self):
        """
        This column_filters list is used by the front end to display
        the filtered icons in the UI
        """
        return json.dumps(self.curr_step['column_filters'])
    
    @property
    def column_type_json(self):
        """
        Returns a list of JSON objects that hold the type of each
        data in each column.
        """
        return json.dumps(self.curr_step['column_type'])

    @property
    def user_email(self):
        """
        Returns the user_email from user.json
        """
        return get_user_field('user_email')

    
    @property
    def step_data_list_json(self):
        """
        Returns a list of step data
        """
        step_data_list = []
        for step in self.steps:
            STEP_OBJ = STEP_TYPE_TO_STEP[step['step_type']]
            params = {key: value for key, value in step.items() if key in STEP_OBJ['params']}
            step_data_list.append({
                'step_id': step['step_id'],
                'step_type': step['step_type'],
                'step_display_name': STEP_OBJ['step_display_name'],
                'step_description': STEP_OBJ['describe'](
                    self,
                    step,
                    **params
                )
            })

        return json.dumps(step_data_list)

    def handle_edit_event(self, edit_event):
        """
        Updates the widget state with a new step that was created
        by the edit_event. Each edit_event creates at most one step. 

        If there is an error in the creation of the new step, this
        function will delete the new, invalid step.
        """
        previous_last_step = None
        for new_step in STEPS:
            if edit_event['type'] == new_step['event_type']:
                # Get the params for this event
                params = {key: value for key, value in edit_event.items() if key in new_step['params']}

                # If this event has an id that is the same as the previous id saved in the previous step, then
                # we overwrite that previous step
                if 'step_id' in self.curr_step and 'step_id' in edit_event and self.curr_step['step_id'] == edit_event['step_id']:
                    # TODO: we should start sending the step_id in all the events we send to the backend!
                    previous_last_step = self.steps.pop()
                
                # Save some pre-execution state to make a potential roll-back easier
                previous_num_steps = len(self.steps)
                try:
                    # Actually execute this event
                    new_step['execute'](self, **params)

                    # We then check if a new step was created, and save some shit in the case that a new
                    # step was created. NOTE: this workaround is needed because filter, specifically, does
                    # not always create a new step; rather, it may just delete a step (e.g. if you remove
                    # all the filters
                    if previous_num_steps < len(self.steps):
                        # If we sucessfully execute this event, we save the params of the event in the step
                        # NOTE: this includes saturated items...
                        for key, value in params.items():
                            self.curr_step[key] = value
                        
                        # Furthermore, we save the step_id (if given). If not given, then we make one up
                        step_id = edit_event['step_id'] if 'step_id' in edit_event else str(uuid.uuid1())
                        self.curr_step['step_id'] = step_id
                except:
                    # If execution of this event fails, then we roll back to the state before the event was received. 
                    # Thus, if a new step was partially created, we delete it:
                    if len(self.steps) > previous_num_steps:
                        self.steps = self.steps[:previous_num_steps]
                    
                    # Furthermore, if the event was trying to overwrite a step, we undelete that step that was getting overwritten
                    if previous_last_step is not None:
                        self.steps.append(previous_last_step)

                    # Finially, we bubble the error up
                    # https://stackoverflow.com/questions/6593922/letting-an-exception-to-bubble-up
                    raise

                # Return if execution is sucessful
                return

        # If we didn't find anything, then we error!
        raise Exception(f'{edit_event} is not an edit event!')

    def handle_update_event(self, update_event):
        """
        Handles any event that isn't caused by an edit, but instead
        other types of new data coming from the frontend (e.g. the df names 
        or some existing steps).
        """
        for update in UPDATES:
            if update_event['type'] == update['event_type']:
                # Get the params for this event
                params = {key: value for key, value in update_event.items() if key in update['params']}
                # Actually execute this event
                update['execute'](self, **params)
                # And then return
                return

        raise Exception(f'{update_event} is not an update event!')        


    def _create_and_checkout_new_step(self, step_type):
        """
        Creates a new step with new_step_id and step_type that starts
        with the ending state of the previous step
        """
        new_step_idx = self.curr_step_idx + 1

        # the new step is a copy of the previous step, where we only take the data we need
        # (which is the formula content only)
        new_step = dict()

        new_step['step_type'] = step_type
        new_step['column_metatype'] = deepcopy(self.steps[new_step_idx - 1]['column_metatype'])
        new_step['column_type'] = deepcopy(self.steps[new_step_idx - 1]['column_type'])
        new_step['column_spreadsheet_code'] = deepcopy(self.steps[new_step_idx - 1]['column_spreadsheet_code'])
        new_step['added_columns'] = [[] for df in self.steps[new_step_idx - 1]['dfs']]
        new_step['column_python_code'] = deepcopy(self.steps[new_step_idx - 1]['column_python_code'])
        new_step['column_evaluation_graph'] = deepcopy(self.steps[new_step_idx - 1]['column_evaluation_graph'])
        new_step['column_filters'] = deepcopy(self.steps[new_step_idx - 1]['column_filters'])
        new_step['dfs'] = deepcopy(self.steps[new_step_idx - 1]['dfs'])
        new_step['df_names'] = deepcopy(self.steps[new_step_idx - 1]['df_names'])

        # add the new step to list of steps
        self.steps.append(new_step)

    def _delete_curr_step(self):
        """
        Deletes the current step and rolls back a step!
        """
        self.steps.pop()

    def add_df_to_curr_step(self, new_df, df_name=None):
        """
        Helper function for adding a new dataframe to the current step!
        """
        # update dfs by appending new df
        self.curr_step['dfs'].append(new_df)
        # Also update the dataframe name
        if df_name is None:
            self.curr_step['df_names'].append(f'df{len(self.curr_step["df_names"]) + 1}')
        else:
            self.curr_step['df_names'].append(df_name)
        
        # Update all the variables that depend on column_headers
        column_headers = new_df.keys()
        self.curr_step['column_metatype'].append({column_header: 'value' for column_header in column_headers})
        self.curr_step['column_type'].append({column_header: get_column_filter_type(new_df[column_header]) for column_header in column_headers})
        self.curr_step['column_spreadsheet_code'].append({column_header: '' for column_header in column_headers})
        self.curr_step['column_python_code'].append({column_header: '' for column_header in column_headers})
        self.curr_step['column_evaluation_graph'].append({column_header: set() for column_header in column_headers})
        self.curr_step['column_filters'].append({column_header: {'operator':'And', 'filters': []} for column_header in column_headers})

    def does_sheet_index_exist(self, index):
        return not (index < 0 or index >= self.num_sheets)
    