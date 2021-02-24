from ics import Calendar, Event
from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, Configuration, EWSDateTime, CalendarItem
from getpass import getpass

import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description='Synchronize ICS to Exchange')
    parser.add_argument('ics', help="URL of the ICS")
    parser.add_argument('username', help="EWS username")
    parser.add_argument('--password', help="EWS password")
    parser.add_argument('mail', help="EWS primary SMTP mail address")
    parser.add_argument('--server', help="EWS server")

    args = parser.parse_args()

    if not args.password:
        args.password = getpass()

    c = Calendar(requests.get(args.ics).text)

    credentials = Credentials(username=args.username, password=args.password)

    config = None
    autodiscover = True
    if args.server:
        config = Configuration(server=args.server, credentials=credentials)
        autodiscover = False

    my_account = Account(primary_smtp_address=args.mail, credentials=credentials,
                    access_type=DELEGATE, config=config, autodiscover=autodiscover)

    for i in list(c.timeline):
        start=EWSDateTime.from_string(str(i.begin))
        end=EWSDateTime.from_string(str(i.end))
        found = False
        for calendar_item in my_account.calendar.filter(start__lt=end, end__gt=start):
            if args.ics in calendar_item.text_body and i.uid in calendar_item.text_body:
                found = True
                break
        if found:
            continue
        item = CalendarItem(
            account = my_account,
            folder = my_account.calendar,
            start = start,
            end = end,
            subject = i.name,
            body = "{}\nics2ews: {}\nuid: {}".format(i.description, args.ics, i.uid),
            location = i.location
        )
        item.save()
