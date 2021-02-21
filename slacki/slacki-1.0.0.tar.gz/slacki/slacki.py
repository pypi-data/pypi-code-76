#--------------------------------------------------------------------------
# Name        : slacki.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
#--------------------------------------------------------------------------

# Libraries
import slacki.utils.check_connection as check_connection
from datetime import datetime
from slacker import Slacker
from slackclient import SlackClient
import traceback
import numpy as np
import pandas as pd
import os

# %%
class slacki():
    """Python package slacki for reading and posting in slack groups."""

    def __init__(self, channel=None, token=None, response_time=60, legacy=False, verbose=3):
        """Initialize slacki with user-defined parameters.

        Parameters
        ----------
        channel : str, (default=None)
            Channel name.
        token : str
            Slack token..
        response_time : TYPE, optional
            DESCRIPTION. The default is 60.
        legacy : Bool (Default=False)
            When True, use the legacy version of slack-control.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        None.

        """
        if token is None: raise Exception('Token should be a valid id.')
        # Check internet connection
        check_connection._internet()
        # Check channel name
        channel = get_channel(channel)
        # Make slackclient object
        sc = self._connect(token, legacy, verbose=verbose)

        # Store in object
        self.legacy = legacy
        self.sc = sc
        self.channel = channel
        self.token = token
        self.response_time = response_time
        self.verbose = verbose
        self.channel_id = self.get_channels(channel_name=channel, create=True, verbose=self.verbose)[1]
    
    # Get channeld id
    def get_channels(self, channel_name=None, create=False, verbose=3):
        channels = None
        channel_id = None
        df = None
        
        if self.legacy:
            channel_id = self.sc.channels.get_channel_id(channel_name[1:])
        else:
            if verbose>=3: print('[slacki] >Gathering channel(s)..')
            df = pd.DataFrame(self.sc.api_call("conversations.list")['channels'])
            results = self.sc.api_call("conversations.list")
            if results.get('error', None)=='missing_scope':
                raise Exception('[slacki] >Error! Scope is missing. You need to add <%s> to your apps in OAuth.\n>More information about the scopes: https://api.slack.com/scopes\n>Adding scopes for your slack env. https://api.slack.com/apps/<YOUR_APPS_ID_HERE>/oauth?' %(results['needed']))
            else:
                channel_names = [m['name'] for m in self.sc.api_call("conversations.list")['channels']]
                channel_ids = [m['id'] for m in self.sc.api_call("conversations.list")['channels']]
                channels = {}
                channels.update(list(zip(channel_names, channel_ids)))

        # Get channel id
        if channel_name is not None:
            channel_id = channels.get(channel_name[1:], None)

        # Make channel if not exists
        if create and (channel_id is None):
            channel_id = make_channel(self.sc, channel_name, self.legacy, verbose=verbose)

        # Return
        return channels, channel_id, df

    # Retrieve posts
    def _connect(self, token, legacy, verbose=3):
        try:
            if legacy:
                sc = Slacker(token)
            else:
                sc = SlackClient(token)
            # Check connection
            check_connection._slack(sc, legacy)
        except Exception as e:
            if verbose>1: print(('[slacki] >ERROR: Could not import token: [%s]' % (str(e))))

        return sc

        # Retrieve posts
    def retrieve_posts(self, date_from=None, date_to=None, n=None, retrieve_names=False, verbose=3):
        """Retrieve posts

        Parameters
        ----------
        date_from : str: "%Y-%m-%d %H:%M:%S"
            Date From
        date_to : str: "%Y-%m-%d %H:%M:%S"
            Date To
        n : int, default: None
            Retrieve the n latest posts. If set to default=None, all is retrieved.
        retrieve_names : str, default: False
            Retrieve the real names for the posted messages. Note that this takes more time as the usersnames are retrieved at every run.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        list of dict containing posts.
        
        References
        ----------
        * https://api.slack.com/methods/conversations.history

        """
        # Check internet connection
        check_connection._internet()
        oldest = None
        latest = None
        get_posts = []
        out = {}

        # Set date
        if date_from is not None:
            oldest = (datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)).total_seconds()
        if date_to is not None:
            latest = (datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)).total_seconds()

        # Retrieve channel IDs of not present yet
        if self.channel_id is None:
            if self.legacy:
                self.channel_id = self.sc.channels.get_channel_id(self.channel[1:])
            else:
                self.channel_id = self.get_channels(channel_name=self.channel[1:], create=False, verbose=self.verbose)[1]

        # Try to retrieve posts
        try:
            if self.channel_id is None:
                if verbose>=3: print('[slacki] Could not retrieve ID for channel %s. If the channel is set on private, change it to normal and try again.' % (self.channel))
            else:
                # Retrieve History
                if self.legacy:
                    GEThistory = self.sc.channels.history(self.channel_id, oldest=oldest, latest=latest, count=n)
                    get_posts = GEThistory.body['messages']
                    out['posts'] = get_posts
                else:
                    # Get the resutls from the history
                    results = self.sc.api_call("conversations.history", channel=self.channel_id, oldest=oldest, latest=latest, count=n)
                    if results.get('error', None)=='missing_scope':
                        raise Exception('[slacki] >Error! Scope is missing. You need to add <%s> to your apps in OAuth.\n>More information about the scopes: https://api.slack.com/scopes\n>Adding scopes for your slack env. https://api.slack.com/apps/<YOUR_APPS_ID_HERE>/oauth?' %(results['needed']))
                    else:
                        out['posts'] = [m['text'] for m in results['messages']]
                        out['user_id'] = [m['user'] for m in results['messages']]

                        # Retrieve the names for hte user ids
                        if retrieve_names:
                            # Retrieve all user-names with ids
                            users = self.get_users(verbose=0)
                            GETnames = []
                            for GETid in out['user_id']:
                                GETnames.append(np.array(users['realname'])[np.isin(users['id'], GETid)][0])
                            out['realname'] = GETnames
        except:
            if verbose>=1: print(traceback.print_exc())

        return(out)

    # Snooze
    def snooze(self, minutes=None, return_status=False, verbose=3):
        """Snooze the slack messages for certain time.

        Parameters
        ----------
        minutes : int, default: None
            Number of minutes to snooze.
        return_status : bool, default: False
            Return the status of the snoozing action.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        status : bool

        """
        try:
            if minutes is not None:
                if self.legacy:
                    self.sc.dnd.set_snooze(num_minutes=minutes)
                    if verbose>=3: print('[slacki] >Snoozer for %s is set on %.d minutes' %(self.channel, minutes))
                    OK = True
                else:
                    if verbose>=3: print('[slacki] >Warning: Snoozer not implemented yet!')
                    OK = False
        except Exception as e:
            if verbose>=1: print(('[slacki] >ERROR: [%s]' % (str(e))))
            OK = False

        # Return
        if return_status:
            return(OK)

    # Post message in channel
    def post(self, queries, icon_url=None, return_status=False, verbose=3):
        """Post messages on slack.

        Parameters
        ----------
        queries : list
            list with strings containing messages to be posted.
        icon_url : str
            String with icon url.
        return_status : bool, default: False
            Return the status of the snoozing action.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        status : bool
        
        References
        * https://api.slack.com/scopes/chat:write
            * chat.delete - Deletes a message.
            * chat.deleteScheduledMessage - Deletes a pending scheduled message from the queue.
            * chat.postEphemeral - Sends an ephemeral message to a user in a channel.
            * chat.postMessage - Sends a message to a channel.
            * chat.scheduleMessage - Schedules a message to be sent to a channel.
            * chat.update - Updates a message.

        """
        if queries is None: raise Exception('Queries should be a string or list with strings.')
        # Check internet connection
        check_connection._internet()
        # Make list if required
        if isinstance(queries, str):
            queries=[queries]
        # Post messages
        try:
            for query in queries:
                if self.legacy:
                    self.sc.chat.post_message(self.channel, text=query, username=None, icon_url=None)
                    postOK = True
                else:
                    postOK = self.sc.api_call("chat.postMessage", channel=self.channel, text=query)['ok']
                if verbose>=5: print('[slacki] [%s] is posted' %(query))
        except Exception as e:
            if verbose>1: print(('[slacki] >ERROR: [%s]' % (str(e))))
            postOK = False
        # Return
        if return_status:
            return(postOK)

    # Post file in channel
    def post_file(self, file, query='File upload', title=None, return_status=False, verbose=3):
        """Post file in slack message.

        Parameters
        ----------
        file : str
            Pathname to the file to be posted in slack.
        query : str
            string containing messages to be posted with the file.
        title : str
            Title of the file to be posted with the file.
        return_status : bool, default: False
            Return the status of the snoozing action.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        status : bool
        
        References
        ----------
        * https://api.slack.com/scopes/files:write
            * https://api.slack.com/methods/files.upload#arg_content
            * files.comments.delete - Deletes an existing comment on a file.
            * files.delete - Deletes a file.
            * files.revokePublicURL - Revokes public/external sharing access for a file
            * files.sharedPublicURL - Enables a file for public/external sharing.
            * files.upload - Uploads or creates a file.

        """
        # Check file exists
        postOK = False
        if not os.path.isfile(file): raise Exception('[slacki] >Error: File does not exists! <%s>')

        # Check internet connection
        check_connection._internet()
        try:
            if self.legacy:
                self.sc.files.upload(file_=file, channels=self.channel, title=title, initial_comment=query)
                if verbose>=5: print('[slacki] File is posted')
                postOK = True
            else:
                results = self.sc.api_call("files.upload", file=file, channels=self.channel, title=title, initial_comment=query, filetype='auto')
                if results.get('error', None)=='missing_scope':
                    raise Exception('[slacki] >Error! Scope is missing. You need to add <%s> to your apps in OAuth.\n>More information about the scopes: https://api.slack.com/scopes\n>Adding scopes for your slack env. https://api.slack.com/apps/<YOUR_APPS_ID_HERE>/oauth?' %(results['needed']))

                if verbose>=5: print('[slacki] >File is posted')
                postOK = True
        except Exception as e:
            if verbose>=1: print(('[slacki] >ERROR: [%s]' % (str(e))))

        # Return
        if return_status:
            return(postOK)

    # Post message in channel
    def get_users(self, legacy=False, verbose=3):
        """Retrieve user information for the slack-group

        Parameters
        ----------
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        list with users.

        """
        # Check internet connection
        check_connection._internet()
        users = {}
        try:
            # Find all users
            if legacy:
                getusers = self.sc.users.list().body
                users['realname'] = list(map(lambda x:x['real_name'], getusers['members']))
                users['name'] = list(map(lambda x:x['name'], getusers['members']))
                for u in getusers['members']:
                    # print(f'User: {u["name"]}, Real Name: {u["real_name"]}, Time Zone: {u["tz_label"]}.')
                    if verbose>=3: print('User: %s, Real Name: %s, Time Zone: %s.' % (u['name'], u['real_name'], u['tz_label']))
                    # print(f'Current Status: {u["profile"]["status_text"]}')
                    # Get image data and show
                    # Image(user['profile']['image_192'])
                users['info']=pd.DataFrame(getusers)
            else:
                getusers = self.sc.api_call("users.list")
                if getusers.get('error', None)=='missing_scope':
                    raise Exception('[slacki] >Error! Scope is missing. You need to add <%s> to your apps in OAuth.\n>More information about the scopes: https://api.slack.com/scopes\n>Adding scopes for your slack env. https://api.slack.com/apps/<YOUR_APPS_ID_HERE>/oauth?' %(getusers['needed']))
                else:
                    getusers = self.sc.api_call("users.list")['members']
                    name = []
                    realname = []
                    ids = []
                    for m in getusers:
                        if m.get('name', None) is not None:
                            name.append(m['name'])
                            realname.append(m.get('real_name', None))
                            ids.append(m.get('id', None))
                    users['realname'] = realname
                    users['name'] = name
                    users['id'] = ids
                    users['info'] = pd.DataFrame(getusers)
                    if verbose>=3: print('[slacki] >Number of users detected: %s' %(len(name)))
        except Exception as ex:
            if verbose>=1: print(('[slacki] >ERROR: [%s]' % (str(ex))))
        return(users)


    # %% Listen
    def listen(self, date_from=None, date_to=None, n=None, response_time=None, verbose=3):
        if response_time is None: response_time = self.response_time
        # Retrieve posts
        results = self.retrieve_posts(date_from=date_from, date_to=date_to, n=n, verbose=verbose)

        # Setup questions
        tasks={}
        tasks['figure'] = False
        tasks['summary'] = False
        tasks['status'] = False
        tasks['advice'] = False

        # Run over all posts
        for message in results['posts']:
            if '@figure' in message:
                tasks['figure']=True
            elif '@summary' in message:
                tasks['summary']=True
            elif '@status' in message:
                tasks['status']=True
            elif '@advice' in message:
                tasks['advice']=True
            elif '@help' in message:
                if verbose>=4: print('[slacki] >My response time is within %d seconds. I listen to: @figure, @summary, @status, @advice, @help' % (response_time))
            else:
                if verbose>=4: print('[slacki] >I can not do <%s>' % (message))

        # Retrieve data or return
        if not np.any([*tasks.values()]):
            pass
        else:
            print('Do some stuff')
        return tasks

# %% Create channel
def make_channel(sc, channel, legacy=False, is_private=False, verbose=3):
    """Create channel."""
    try:
        if legacy:
            sc.channels.create(channel[1:])
        else:
            results = sc.api_call("conversations.create", name=channel[1:], is_private=is_private)
            if results.get('error', None)=='missing_scope':
                print('[slacki] >Error! Scope is missing. You need to add <%s> to your apps in OAuth.' %(results['needed']))
                print('[slacki] >More information about the scopes: https://api.slack.com/scopes')
                print('[slacki] >Adding scopes for your slack env. https://api.slack.com/apps/<YOUR_APPS_ID_HERE>/oauth?')

        if verbose>=3: print('[slacki] >Channel [%s] is succesfull created' % (channel))
    except Exception as e:
        if verbose>=3: print('[slacki] >Channel [%s] already exists.' % (channel))


# %% Post message in channel
def get_channel(channel):
    if (channel is None) or (channel=='') or (len(channel)<3): raise Exception('Channel should be a valid name; can not be None or "" or less then 3 chars.')
    if channel[0]!='#':
        channel = '#' + channel
    
    return(channel)
