#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Replays an existing analysis onto the sheet
"""

from copy import copy
import uuid
from mitosheet.save_utils import read_and_upgrade_analysis

from mitosheet.steps import STEPS
from mitosheet.errors import make_execution_error


REPLAY_ANALYSIS_UPDATE_EVENT = 'replay_analysis_update'
REPLAY_ANALYSIS_UPDATE_PARAMS = [
    'analysis_name',
    'import_summaries',
    'clear_existing_analysis',
]

def execute_replay_analysis_update(
        wsc,
        analysis_name,
        import_summaries,
        clear_existing_analysis
    ):
    """
    This function reapplies all the steps summarized in the passed step summaries, 
    which come from a saved analysis. 

    If any of the step summaries fails, this function tries to roll back to before
    it applied any of the stems

    If clear_existing_analysis is set to true, then this will clear the entire widget
    state container (except the initalize step) before applying the saved analysis.
    """ 
    # We only keep the intialize step only
    if clear_existing_analysis:
        wsc.steps = wsc.steps[:1]

    # If we're getting an event telling us to update, we read in the steps from the file
    analysis = read_and_upgrade_analysis(analysis_name)

    # When replaying an analysis with import events, you can also send over
    # new params to the import events to replace them. We replace them in the steps here
    if import_summaries is not None:
        for step_idx, params in import_summaries.items():
            for key, value in params.items():
                analysis['steps'][step_idx][key] = value  

    # We make a shallow copy of the steps, as none of the objects
    # will be changed by the step summaries we apply   
    old_steps = copy(wsc.steps)  
    
    try:
        for _, step_summary in analysis['steps'].items():
            step_type = step_summary['step_type']

            found = False
            for new_step in STEPS:
                if step_type == new_step['step_type']:
                    found = True
                    # Get the params for this event
                    params = {key: value for key, value in step_summary.items() if key in new_step['params']}
                    # Actually execute this event
                    new_step['execute'](wsc, **params)
                    
                    # Save the params for this event
                    for key, value in params.items():
                        wsc.curr_step[key] = value

                    # Every step also needs an id, which we add
                    # TODO: in the future, we should functionalize (and unify) the running of
                    # steps, so we don't have to remember to do this everywhere
                    wsc.curr_step['step_id'] = str(uuid.uuid1())

            if not found:
                raise Exception('Trying to recreate invalid step:', step_summary)

    except Exception as e:
        print(e)
        # We remove all applied steps if there was an error
        wsc.steps = old_steps

        # And report a generic error to the user
        raise make_execution_error()


REPLAY_ANALYSIS_UPDATE = {
    'event_type': REPLAY_ANALYSIS_UPDATE_EVENT,
    'params': REPLAY_ANALYSIS_UPDATE_PARAMS,
    'execute': execute_replay_analysis_update
}