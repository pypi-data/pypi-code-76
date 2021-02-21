"""Produces timesheets using activity data from GitLab.Com API calls.

The output is written to stdout in markdown. This can be viewed
in a browser using grip https://pypi.org/project/grip/ or other tools.
Please see: https://gitlab.com/oliversmart/timesheet_gitlab for information
about how to setup access to your account through GitLab API.

Example runs:
* produce a daily timesheet for today and view in your browser:
      timesheet_gitlab | grip -b -

* produce a monthly timesheet for January this year and saving the markdown
  to a file:
      timesheet_gitlab 1-1 31-1 > jan_timesheet.md

* produce a timesheet for project "tigger_watch" only for this month viewing
  directly in your browser:
      timesheet_gitlab --filter tigger_watch 1 today | grip -b -
"""
#    Copyright 2021 Oliver Smart
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import argparse
import datetime
import io
import logging
import os
import sys
from argparse import RawTextHelpFormatter
from typing import List, Optional, NamedTuple, TextIO

import gitlab

HOURS_PER_DAY = 7.5
DEFAULT_URL = 'https://GitLab.com/'


class TSEvent(NamedTuple):
    date: str
    time: str
    activity: str
    hyperlink: Optional[str]


class TimeSlot(NamedTuple):
    start: str
    finish: str
    activities: List[str]
    hyperlinks: List[Optional[str]]


class TimeSheet(NamedTuple):
    date: datetime.datetime
    hours: float
    text: str


class GitLabTimeSheets:
    def __init__(self):
        self.args = None
        self.gl = None
        self.user = None
        self.start_date: datetime = None
        self.finish_date: datetime = None
        self.project_id2name = {}

    def _connect(self):
        """ connects to gitlab server & gets the user that will be analyzed """
        token = self.args.private_token
        if token is None:
            try:
                token = os.environ['PRIVATE_TOKEN']
            except KeyError:
                print('ERROR no private token - see help message.')
                sys.exit(1)
        self.gl = gitlab.Gitlab(self.args.url, private_token=token)
        self.gl.auth()
        current_user = self.gl.user
        my_id = current_user.id
        self.user = self.gl.users.get(my_id)
        logging.debug(f'current_user={self.user.name} id={my_id}')

    def _deal_with_command_line_args(self):
        parser = self._setup_command_line_options()
        self._parse_command_line_args(parser)

    @staticmethod
    def _setup_command_line_options():
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=RawTextHelpFormatter)
        p_add = parser.add_argument
        p_add('START', nargs='?', default='today',
              help='start date for timesheet as DD-MM-YY.\n'
                   'For instance 20-01-21 for 20 Jan 2021.\n'
                   'If the year or month is left out then current year/month'
                   ' will be used.\n'
                   'If not specified at all the timesheet for today will be'
                   ' produced')
        p_add('FINISH', nargs='?',
              help='finish date for timesheet as DD-MM-YY.\n'
                   'If not specified the timesheet for START day will'
                   ' be produced.')
        p_add('-p', '--private_token', metavar='TOKEN',
              help='private token to connect to the GitLab Server. This must\n'
                   'be specified unless the token is supplied using the shell\n'
                   'variable PRIVATE_TOKEN.'
                   ' The token must have read_api access.')
        p_add('-u', '--url', default=DEFAULT_URL,
              help=f'the url of the GitLab server, defaults to {DEFAULT_URL}')
        p_add('-f', '--filter',
              help='only include projects whose name includes FILTER')
        p_add('-s', '--summary', action='store_true',
              help='do not print daily time sheets. Only the initial summary.')
        p_add('-d', '--details', action='store_true',
              help='For each daily timesheet add a detailed list of each '
                   'individual activities. ')
        p_add('--debug', action='store_true',
              help='turn on debug message logging output\n'
                   '(only useful for the program developers).')
        return parser

    def _parse_command_line_args(self, parser):
        self.args = parser.parse_args()

    def _setup_dates(self) -> None:
        """ deals with self.args producing self.start_date and self.end_date """
        logging.debug(f'_setup_dates: self.args.START={self.args.START}'
                      f' self.args.FINISH={self.args.FINISH}')
        self.start_date = self._process_date(date_string=self.args.START)
        self.finish_date = self._process_date(date_string=self.args.FINISH)
        logging.debug(f'_setup_dates: self.start_date={self.start_date}'
                      f' self.finish_date={self.finish_date}')
        if self.finish_date is not None and self.start_date > self.finish_date:
            raise ValueError('start date cannot be after finish date')

    @staticmethod
    def _process_date(date_string: Optional[str]
                      ) -> Optional[datetime.datetime]:
        if date_string is None:
            return None
        today = datetime.datetime.now()
        day, month, year = today.day, today.month, today.year
        if date_string != 'today':
            try:
                date_split = date_string.split('-')
                day = int(date_split[0])
                month = int(date_split[1])
                year = int(date_split[2])
            except IndexError:
                pass
            if year < 2000:
                year = year + 2000
        logging.debug(f'_process_date: day={day} month={month} year={year}')
        return datetime.datetime(year, month, day)

    def _date_events(self, a_date: datetime.datetime) -> List[TSEvent]:
        """ returns the events for date a_date """
        prev_date = a_date + datetime.timedelta(days=-1)
        next_date = a_date + datetime.timedelta(days=1)
        prev_date = prev_date.strftime('%Y-%m-%d')
        next_date = next_date.strftime('%Y-%m-%d')
        logging.debug(f'prev_date={prev_date} next_date={next_date}')
        events = self.user.events.list(after=prev_date,
                                       before=next_date,
                                       all=True, sort='asc')
        ts_events = []
        for i_e, event in enumerate(events):
            str_event = str(event)
            str_event = str_event.replace('{', '\n{')
            str_event = str_event.replace(', ', ',\n')
            logging.debug(str_event)
            created_at = event.created_at
            date = created_at[:10]
            time = created_at[11:16]
            action = event.action_name
            target_type = event.target_type
            project_name = self._project_name(event.project_id)
            if self.args.filter and self.args.filter not in project_name:
                continue
            issue_number = None
            times = [time]
            if target_type is not None:
                if 'Note' in target_type:
                    issue_number = event.note['noteable_iid']
                    body = event.note['body']
                    if 'TSADD' in body:
                        splits = body.split('TSADD')
                        for word in splits:
                            word = word.replace('_', '')
                            if len(word) == 5:
                                logging.warning(f'inserting TSADD time {word}'
                                                f' before {time}')
                                times.insert(0, word)
                elif target_type == 'Issue':
                    issue_number = event.target_iid
            activity = self._activity(project_name=project_name,
                                      action=action,
                                      target_type=target_type,
                                      issue_number=issue_number)
            hyperlink = self._hyperlink(project_name=project_name,
                                        issue_number=issue_number,
                                        target_type=target_type,
                                        target_id=event.target_id)
            for t in times:
                ts_event = TSEvent(date=date, time=t,
                                   activity=activity,
                                   hyperlink=hyperlink)
                logging.debug(f'{i_e+1:3} {ts_event}')
                ts_events.append(ts_event)
        return ts_events

    @staticmethod
    def _activity(project_name: str,
                  action: str,
                  target_type: str,
                  issue_number: str) -> str:
        project_short = project_name.split('/')[1]
        activity = f'{project_short}: {action}'
        if target_type is not None and 'Wiki' in target_type:
            activity += ' wiki'
        if issue_number is not None:
            activity += f' issue #{issue_number}'
        activity = activity.replace('pushed to', 'pushed commit(s)')
        activity = activity.replace('deleted', 'deleted tag')
        activity = activity.replace('pushed new', 'created tag')
        return f'`{activity}`'

    def _hyperlink(self,
                   project_name: str,
                   issue_number: Optional[str],
                   target_type: str,
                   target_id: str) -> Optional[str]:
        hyperlink = None
        if issue_number is not None:
            hyperlink = (f'{self.args.url}{project_name}'
                         f'/-/issues/{issue_number}')
            if 'Note' in target_type:
                hyperlink += f'#note_{target_id}'
        return hyperlink

    @staticmethod
    def _print_detailed_list(a_date: datetime,
                             a_date_events: List[TSEvent],
                             file: TextIO):
        print('* Detailed list of activities for ' +
              a_date.strftime('%A %d %b %Y') + ':', file=file)
        for event in a_date_events:
            activity = event.activity
            if event.hyperlink is not None:
                activity = f'[{activity}]({event.hyperlink})'
            print(f'  * `{event.time}` {activity} ', file=file)

    @staticmethod
    def _bin_events(date_events: List[TSEvent]) -> List[TimeSlot]:
        """ bins events into 30-minute time slots"""
        timeslots = []
        for hour in range(24):
            hour24 = f'{hour:02d}'
            timeslots.append(TimeSlot(start=f'{hour24}:00',
                                      finish=f'{hour24}:29',
                                      activities=[], hyperlinks=[]))
            timeslots.append(TimeSlot(start=f'{hour24}:30',
                                      finish=f'{hour24}:59',
                                      activities=[], hyperlinks=[]))
        for event in date_events:
            for slot in timeslots:
                if slot.start <= event.time <= slot.finish:
                    if event.activity not in slot.activities:
                        slot.activities.append(event.activity)
                        slot.hyperlinks.append(event.hyperlink)
                    continue
        timeslots = [s for s in timeslots if len(s.activities)]
        logging.debug('\n'.join([str(t) for t in timeslots]))
        return timeslots

    @staticmethod
    def _print_timeslots(timeslots: List[TimeSlot], file: TextIO):
        """prints timeslots in markdown table"""
        print('>  | **time slot** | **activities** |', file=file)
        print('>  | ----------------- | -------------- |', file=file)
        for slot in timeslots:
            hyperlinked_activities = []
            for activity, hyperlink in zip(slot.activities, slot.hyperlinks):
                if hyperlink is None:
                    hyperlinked_activities.append(activity)
                else:
                    hyperlinked_activities.append(f'[{activity}]({hyperlink})')
            print(f'>  | {slot.start}&#8209;{slot.finish} '
                  f' | {", ".join(hyperlinked_activities)} |', file=file)

    def _print_heading(self):
        """ prints the headings """
        try:
            print(os.environ['TIMESHEET_HEADER'])
        except KeyError:
            pass
        projects = self.args.filter or ''
        simple_url = self.args.url.replace('https:', '').replace('/', '')
        print(f'# {projects} Projects hosted at {simple_url}')
        print(f'### Monthly Timesheet for '
              f'{self.start_date.strftime("%d %b %Y")} to '
              f'{self.finish_date.strftime("%d %b %Y")} (inclusive)')

    @staticmethod
    def _print_overall_table(time_sheets: List[TimeSheet]) -> None:
        """prints initial summary markdown table"""
        print('| **Date** | **Hours worked** |')
        print('| -------- | ---------------- |')
        for ts in time_sheets:
            print(f"| {ts.date.strftime('%A %d %b %Y')} | {ts.hours:.1f} |")
        total_hours = sum([ts.hours for ts in time_sheets])
        total_days = total_hours/HOURS_PER_DAY
        print(f'| **Total hours worked** | **{total_hours:.1f}** |')
        print(f'| **Total days worked** ({HOURS_PER_DAY} hours per day)'
              f'| **{total_days:.1f}** |')
        logging.info(f'Total hours={total_hours} Total days={total_days:.1f}')

    def _project_name(self, project_id):
        """ returns the project_name for a project_id """
        if project_id not in self.project_id2name:
            project_name = self.gl.projects.get(project_id).path_with_namespace
            self.project_id2name[project_id] = project_name
        return self.project_id2name[project_id]

    @staticmethod
    def _setup_logging(debug: bool) -> None:
        """ basic logging setup """
        if debug:
            level = logging.DEBUG
        else:
            level = logging.INFO
        logging.basicConfig(level=level, format='%(levelname)-8s %(message)s')

    def _timesheet_for_a_date(self, a_date: datetime.datetime) -> TimeSheet:
        capture = io.StringIO()
        print(f"### Daily time sheet for {a_date.strftime('%A %d %b %Y')}\n",
              file=capture)
        date_events = self._date_events(a_date)
        if date_events:
            timeslots = self._bin_events(date_events)
            self._print_timeslots(timeslots, file=capture)
            total_hours = 0.5 * len(timeslots)
            print(f'> \n> **Hours worked: {total_hours:.1f}**', file=capture)
            if self.args.details:
                self._print_detailed_list(a_date, date_events, file=capture)
            print('\n----', file=capture)
        else:
            total_hours = 0
            print('no activity', file=capture)
        markdown = capture.getvalue()
        capture.close()
        return TimeSheet(date=a_date, hours=total_hours, text=markdown)

    def run(self):
        self._deal_with_command_line_args()
        self._setup_logging(debug=self.args.debug)
        logging.debug(f'self.args={self.args}')
        self._setup_dates()
        self._connect()
        if self.finish_date is None:
            time_sheet = self._timesheet_for_a_date(self.start_date)
            print(time_sheet.text)
        else:
            time_sheets: List[TimeSheet] = []
            date = self.start_date
            while date <= min(self.finish_date, datetime.datetime.now()):
                time_sheet = self._timesheet_for_a_date(date)
                logging.info(f'{time_sheet.date.strftime("%Y-%m-%d")} '
                             f'hours: {time_sheet.hours}')
                if time_sheet.hours > 0:
                    time_sheets.append(time_sheet)
                date += datetime.timedelta(days=1)
            self._print_heading()
            self._print_overall_table(time_sheets)
            if not self.args.summary:
                [print(ts.text) for ts in time_sheets]
        print('_Timesheet produced using `timesheet_gitlab`'
              ' https://gitlab.com/oliversmart/timesheet_gitlab/_')
