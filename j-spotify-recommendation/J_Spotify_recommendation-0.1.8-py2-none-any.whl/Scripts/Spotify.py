import base64
import platform
from urllib.parse import urlencode
import datetime
from datetime import timezone
import time
import geckodriver_autoinstaller
import requests
from selenium.webdriver import Safari,Chrome,Firefox
from selenium.webdriver.common.keys import Keys
import os, sys
import logging
import pandas as pd
import json
import sqlite3
import random
from statistics import quantiles
import tkinter as tk
from tkinter import messagebox
pd.set_option('display.max_rows', None)

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.disable()


new = os.environ
PATH = f'{new["HOME"]}/'

# Client ID and Secret and Redirect (WILL NOT CHANGE)
client_id = '62d46cea622741b1b6013c64688e2dfa'
client_secret = '1a863a23884b410c8b55d2b324eb7c84'
redirect_uri = 'http://song-in-playlist-finder/callback'


def zipf(l):
    """Create weights for randomly selecting genres"""
    ls = []
    w = []
    x = .05
    zipf = []
    for i,n in enumerate(l):
        if n == 0:
            n = 1
        ls.append(1/n)
        w.append(x)
        x+=.01
    for i,r in enumerate(ls):
        zipf.append(w[i]*r)

    return zipf


class Recommendation(object):
    """Set nonetype variables that will change for each user."""
    access_token = None
    access_token_expires = time.time()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'
    auth_url = 'https://accounts.spotify.com/authorize'
    refresh_token = None
    recomended_tracks = []  # Recomended tracks have ID and URI for adding to playlist


    def __init__(self,name, client_id, client_secret, redirect_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.name = name
        self.perform_cred_flow()

    def perform_cred_flow(self):
        """
        Use cred flow for this class to get song data without having to get user auth
        Used after we have put user data into DB
        """
        endpoint = 'https://accounts.spotify.com/api/token' #endpoint for getting credentials flow

        params = self.get_token_data() #parameters for requests
        headers = self.get_token_header() # header for requests

        # print(headers)
        # print(url)
        # print(params)

        r = requests.post(url= endpoint,data=params, headers= headers) #post to re
        if r.status_code not in range(200, 299):
            logging.error('error with getting client cred flow %s', r.status_code)
            print(r.status_code)
            print(r.text)
            print(r.json())
            return False

        data = r.json()
        self.access_token = data['access_token']
        self.access_token_expires = data['expires_in']

        return True

    def get_token_data(self):
        """
        token data for getting our access token
        """
        return {
            'grant_type': 'client_credentials',
        }

    def get_client_cred(self):
        """
        returns base64 str for client credentials
        """
        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == 0 or client_secret == 0:
            raise ValueError

        authorization = client_id + ':' + client_secret
        client_b64 = base64.b64encode(authorization.encode())
        return client_b64

    def get_token_header(self):
        """
        :return token header for url to get access token
        """

        client_b64 = self.get_client_cred()
        return {
            'Authorization': f'Basic {client_b64.decode()}'
        }

    def get_bearer_header(self):
        """
        When access token is received use it for the header to get user info
        """

        return {
            'Authorization': f'Bearer {self.access_token}'
        }

    def get_access_token(self):
        """return access token to use if it is expired"""
        token = self.access_token
        expires = self.access_token_expires
        now = time.time()
        print(type(now),'lolo',type(expires))
        if expires < now:
            self.perform_cred_flow()
            return self.get_access_token()
        elif token == None:
            self.perform_cred_flow()
            return self.get_access_token()
        return token

    def track_details(self, track_id):
        """return the genre to be used in creating user pref DF
        Mainly used in UserPref
        """
        headers = self.get_bearer_header()
        endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'

        r = requests.get(url=endpoint, headers=headers)
        if r.status_code not in range(199, 299):
            logging.error('error with retreiving track details for track id %s', track_id)
            print(r.status_code)
            print(r.json())
            return {}
        data = r.json()
        artist_id = data['artists'][0]['id']
        popularity = data['popularity']

        return artist_id, popularity

    def artist_genres(self, artist_id):
        """return the genres of a given artist
        Mainly used in UserPref
        """
        headers = self.get_bearer_header()
        endpoint = f'https://api.spotify.com/v1/artists/{artist_id}'

        r = requests.get(url=endpoint, headers=headers)
        if r.status_code not in range(199, 299):
            logging.error('error with retreiving track details for artist id %s', artist_id)
            print(r.status_code)
            print(r.json())
            return {}
        data = r.json()
        genres = data['genres']
        return genres

    def get_audio_features(self, tracks=[], routines=False, batch=None, recommendation=False):
        """
        Main program for returning features of users preferences
        """
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        # try:
        c.execute("SELECT top_tracks FROM userTop")
        top_tracks = c.fetchall()
        top_tracks = json.loads(top_tracks[0][0])
        user_top_tracks = list(top_tracks.keys())

        c.execute("SELECT playlist_tracks FROM userPlaylists")
        playlist_tracks = []
        placeholder = c.fetchall()


        for i in placeholder:
            for playlist in i:
                    play_tracks = json.loads(playlist)
                    for track in play_tracks:
                        playlist_tracks.append(track)

        headers = self.get_bearer_header()
        print('getting audio features')

        w = random.sample(range(1500), 1200) #Instead of returning all songs only get 1500 random songs
        x = -1
        q = 1


        if not recommendation:
            if type(tracks) == dict:
                logging.info("tracks are put in dict %s", tracks.keys())
                user_tracks_id = list(tracks.keys())


            elif type(tracks) == list:
                logging.info("tracks are put in list %s", tracks)
                user_tracks_id = tracks

                # use this to return the user tracks from SQL DB
                logging.info("Getting user tracks from DB userTracks")
                c.execute("SELECT track_id FROM userTracks")
                user_tracks = c.fetchall()
                print('user tracks',user_tracks)
                for track in user_tracks:
                    user_tracks_id.append(track[0])
                logging.info("user tracks are %s", user_tracks_id)
            else:
                raise ValueError


        else:
            logging.info(f'{len(tracks)} + tracks were input and are {tracks}')
            rec_tracks = []
            for track in tracks:
                if track not in playlist_tracks:
                    rec_tracks.append(track)
                    tracks = rec_tracks

        df_dict_list = []
        # print(user_tracks_id)
        for i in tracks:
            x +=1
            for ind,num in enumerate(w):
                if num == x:

                    q += 1
                    print('song id {}'.format(i))
                    print(f'{q} / {len(tracks)}')

                    endpoint = f'https://api.spotify.com/v1/audio-features/{i}'
                    r = requests.get(url=endpoint, headers=headers)
                    if r.status_code == 503:
                        print("ERROR WITH THE SERVER WAITING 30 SECONDS")
                        time.sleep(20)
                        continue
                    if r.status_code not in range(199, 299):
                        logging.error('Error with getting audio features %s', r.status_code)
                        print(r.status_code)
                        print(r.json())
                        continue


                    data = r.json()
                    try:
                        artist_id, popularity = self.track_details(track_id=i)
                        genres = self.artist_genres(artist_id)
                    except ValueError:
                        genres = ['None']
                        pass


                    user_TT = False
                    user_PT = False
                    if i in user_top_tracks:
                        logging.info("Found track in user_top_tracks %s",i)
                        user_TT = True
                    if i in playlist_tracks:
                        logging.info("Found track in playlist_tracks %s",i)
                        user_PT = True

                    if len(genres) == 0:
                        genres = ['NONE']
                    if routines:
                        now = time.time()
                        c.execute("CREATE TABLE IF NOT EXISTS playbackTracks (track_id TEXT,batch INTEGER, timestamp REAL, genre TEXT, danceability REAL, energy REAL, key REAL, loudness REAL, mode REAL, speechiness REAL,"
                            "acousticness REAL, instrumentalness REAL, liveness REAL, valence REAL, tempo REAL, popularity REAL, top_track BOOL, playlist_track BOOL, UNIQUE(track_id))")
                        c.execute("INSERT OR IGNORE INTO playbackTracks (track_id, batch, timestamp, genre, danceability, energy, key, loudness, mode, speechiness,"
                            "acousticness, instrumentalness, liveness, valence, tempo, popularity,top_track,playlist_track) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (i,batch,now, genres[0], data['danceability'], data['energy'], data['key'], data['loudness'],data['mode'], data['speechiness'],
                             data['acousticness'], data['instrumentalness'], data['liveness'], data['valence'],
                             data['tempo'], popularity,user_TT,user_PT))
                        conn.commit()

                    elif not routines and not recommendation:
                        c.execute("CREATE TABLE IF NOT EXISTS userTrackFeatures (track_id TEXT, genre TEXT, danceability REAL, energy REAL, key REAL, loudness REAL, mode REAL, speechiness REAL,"
                                  "acousticness REAL, instrumentalness REAL, liveness REAL, valence REAL, tempo REAL, popularity REAL, top_track BOOL, playlist_track BOOL, UNIQUE(track_id))")
                        c.execute("INSERT OR IGNORE INTO userTrackFeatures (track_id, genre, danceability, energy, key, loudness, mode, speechiness,acousticness, instrumentalness, liveness, valence, tempo, popularity,top_track,playlist_track) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                  (i,genres[0],data['danceability'],data['energy'],data['key'],data['loudness'],data['mode'],data['speechiness'],data['acousticness'],data['instrumentalness'],data['liveness'],data['valence'],data['tempo'],popularity, user_TT, user_PT))
                        conn.commit()

                    if recommendation:
                        if i not in playlist_tracks:
                            recomend_dict = {'Track ID': i,'genre': genres[0], 'danceability' :data['danceability'], 'energy' :data['energy'],'key' :data['key'],
                                             'loudness' : data['loudness'],'mode' :data['mode'],'speechiness' : data['speechiness'],
                                 'acousticness' : data['acousticness'],'instrumentalness' : data['instrumentalness'],
                                'liveness' :data['liveness'], 'valence' :data['valence'],'tempo' :data['tempo'], 'popularity' :popularity,'top_track' :user_TT,'playlist_track' :user_PT}

                            df_dict_list.append(recomend_dict)
        try:
            df_for_tree = pd.DataFrame(df_dict_list,index=[i for i in range(len(df_dict_list))])
        except:
            return
        return df_for_tree

    def get_recomendation(self, limit=20,decicion_tree= False):
        """Get recomendation to add to playlist"""

        def create_list(ls): #Create a list from calling user features
            m = []
            for i in range(len(ls)):
                m.append(ls[i][0])
            return m

        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        now = datetime.datetime.now()  # set the time for the update
        now = str(now)

        """
        Use Generate Recomendation in API to get a list of 20 songs
        that we read through to find the best ones for user
        """
        print("getting recomended songs")
        headers = self.get_bearer_header()

        c.execute("SELECT playlist_tracks FROM userPlaylists")
        playlist_tracks = []
        placeholder = c.fetchall()

        for i in placeholder:
            for playlist in i:
                tracks = json.loads(playlist)
                for track in tracks:
                    playlist_tracks.append(track)

        c.execute("SELECT top_artists FROM userTop")
        top_artists = c.fetchall()
        c.execute("SELECT top_genres FROM userTop")
        top_genres = c.fetchall()
        c.execute("SELECT top_tracks FROM userTop")
        top_tracks = c.fetchall()

        top_artists = json.loads(top_artists[0][0])
        top_genres = json.loads(top_genres[0][0])
        top_tracks = json.loads(top_tracks[0][0])

        c.execute("SELECT track_id FROM userTracks")
        user_tracks = c.fetchall()


        seed_artists_list = list(top_artists.keys())
        seed_genres_list = list(sorted(top_genres.keys()))
        seed_tracks_list = list(top_tracks.keys())
        seed_tracks_list.append(random.sample(user_tracks, 4))

        genre_recomended_seeds = []

        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        genre_file = os.path.join(os.getcwd() + '/xbox_one_vietnamese.txt')

        with open(genre_file,'r') as f:
            lines = f.readlines()
            for line in lines:
                genre_recomended_seeds.append(line.strip("\n"))
            f.close()

        seed_genres_pre = []
        weights = []
        for genre in seed_genres_list:
            if genre in genre_recomended_seeds:
                weights.append(top_genres[genre])
                seed_genres_pre.append(genre)

        seed_artists = random.sample(population=seed_artists_list, k=random.randint(1, 3))
        seed_genres = random.choices(population=seed_genres_pre, weights=zipf(weights),
                                     k=random.randint(0, 4 - len(seed_artists)))
        seed_tracks = random.sample(population=seed_tracks_list, k=1)

        seed_artists = str(seed_artists)
        seed_genres = str(seed_genres)
        seed_tracks = str(seed_tracks)
        seed_artists = seed_artists[1:-1].replace("'", "").replace(" ", "%2C").replace(",", "")
        seed_genres = seed_genres[1:-1].replace("'", "").replace(" ", "%2C").replace(",", "")
        seed_tracks = seed_tracks[1:-1].replace("'", "").replace(" ", "%2C").replace(",", "")


        ########## Call user track features to get recomendation #########
        c.execute("SELECT danceability FROM userTrackFeatures")
        danceability = c.fetchall()
        danceability_ls = create_list(danceability)
        danceability_quantiles = quantiles(danceability_ls)
        c.execute("SELECT energy FROM userTrackFeatures")
        energy = c.fetchall()
        energy_ls = create_list(energy)
        energy_quantiles = quantiles(energy_ls)
        c.execute("SELECT key FROM userTrackFeatures")
        key = c.fetchall()
        key_ls = create_list(key)
        key_quantiles = quantiles(key_ls)
        c.execute("SELECT loudness FROM userTrackFeatures")
        loudness = c.fetchall()
        loudness_ls = create_list(loudness)
        loudness_quantiles = quantiles(loudness_ls)
        c.execute("SELECT mode FROM userTrackFeatures")
        mode = c.fetchall()
        mode_ls = create_list(mode)
        mode_quantiles = quantiles(mode_ls)
        c.execute("SELECT speechiness FROM userTrackFeatures")
        speechiness = c.fetchall()
        speechiness_ls = create_list(speechiness)
        speechiness_quantiles = quantiles(speechiness_ls)
        c.execute("SELECT acousticness FROM userTrackFeatures")
        acousticness = c.fetchall()
        acousticness_ls = create_list(acousticness)
        acousticness_quantiles = quantiles(acousticness_ls)
        c.execute("SELECT instrumentalness FROM userTrackFeatures")
        instrumentalness = c.fetchall()
        instrumentalness_ls = create_list(instrumentalness)
        instrumentalness_quantiles = quantiles(instrumentalness_ls)
        c.execute("SELECT liveness FROM userTrackFeatures")
        liveness = c.fetchall()
        liveness_ls = create_list(liveness)
        liveness_quantiles = quantiles(liveness_ls)
        c.execute("SELECT valence FROM userTrackFeatures")
        valence = c.fetchall()
        valence_ls = create_list(valence)
        valence_quantiles = quantiles(valence_ls)
        c.execute("SELECT tempo FROM userTrackFeatures")
        tempo = c.fetchall()
        tempo_ls = create_list(tempo)
        tempo_quantiles = quantiles(tempo_ls)
        c.execute("SELECT popularity FROM userTrackFeatures")
        popularity = c.fetchall()
        popularity_ls = create_list(popularity)
        popularity_quantiles = quantiles(popularity_ls)
        conn.commit()

        endpoint = 'https://api.spotify.com/v1/recommendations'
        query_params = {'limit': f'{limit}', 'market': 'US',
                        'seed_artists': f'{seed_artists}',
                        'seed_genres': f'{seed_genres}',
                        'seed_tracks': f'{seed_tracks}',
                        'min_danceability': round(danceability_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_energy': round(energy_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_key': round(key_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_loudness': round(loudness_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_mode': round(mode_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_speechiness': round(speechiness_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_acousticness': round(acousticness_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_instrumentalness': round(instrumentalness_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_liveness': round(liveness_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_valence': round(valence_quantiles[0] + random.uniform(-.1,.2),2),
                        'min_tempo': round(tempo_quantiles[0] + random.uniform(-.1,.2),2),
                        # 'min_popularity': round(popularity_quantiles[0] + random.uniform(0,.2),2),
                        # 'min_duration': pdf['duration'].quantile(.3),
                        'max_danceability': round(danceability_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_energy': round(energy_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_key': round(key_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_loudness': round(loudness_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_mode': round(mode_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_speechiness': round(speechiness_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_acousticness': round(acousticness_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_instrumentalness': round(instrumentalness_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_liveness': round(liveness_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_valence': round(valence_quantiles[2] + random.uniform(-.1,.3),2),
                        'max_tempo': round(tempo_quantiles[2] + random.uniform(-.1,.3),2),
                        # 'max_popularity': round(popularity_quantiles[2] + random.uniform(0,.3),2),
                        # 'max_duration': pdf['duration'].quantile(.769),2),
                        'target_danceability': round(danceability_quantiles[1],2),
                        'target_energy': round(energy_quantiles[1],2),
                        'target_key': round(key_quantiles[1],2),
                        'target_loudness': round(loudness_quantiles[1],2),
                        'target_mode': round(mode_quantiles[1],2),
                        'target_speechiness': round(speechiness_quantiles[1],2),
                        'target_acousticness': round(acousticness_quantiles[1],2),
                        'target_instrumentalness': round(instrumentalness_quantiles[1],2),
                        'target_liveness': round(liveness_quantiles[1],2),
                        'target_valence': round(valence_quantiles[1],2),
                        'target_tempo': round(tempo_quantiles[1],2)}
                        # 'target_popularity' : round(danceability_quantiles[1],2)}
        w = []
        z = []
        for k, v in list(query_params.items()):
            w.append(k)
            z.append(v)

        """
        This is non compatible don't use it until it is fixed

        # print(w)
        # print('-'*55)
        # print(z)
        # print('-'*55)
        # print(w[7],w[8],w[9],w[10],w[17],w[18],w[20],w[29],w[31])
        # print('-'*55)
        # print(z[7], z[8], z[9], z[10], z[17], z[18], z[20], z[29], z[31])
        #&{w[7]}={z[7]}&{w[9]}={z[9]}&{w[10]}={z[10]}&{w[17]}={z[17]}&{w[18]}={z[18]}&{w[20]}={z[20]}&{w[29]}={z[29]}&{w[31]}={z[31]}'
        """

        search_url = f'{endpoint}?{w[0]}={z[0]}&{w[1]}={z[1]}&{w[2]}={z[2]}&{w[3]}={z[3]}&{w[4]}={z[4]}&{w[5]}={z[5]}&{w[6]}={z[6]}&{w[11]}={z[11]}&{w[12]}={z[12]}&{w[13]}={z[13]}&{w[14]}={z[14]}&{w[15]}={z[15]}&{w[16]}={z[16]}&{w[19]}={z[19]}&{w[21]}={z[21]}&{w[22]}={z[22]}&{w[23]}={z[23]}&{w[24]}={z[24]}&{w[25]}={z[25]}&{w[26]}={z[26]}&{w[27]}={z[27]}&{w[28]}={z[28]}&{w[30]}={z[30]}&{w[32]}={z[32]}&{w[33]}={z[33]}&{w[34]}={z[34]}&{w[35]}={z[35]}&{w[36]}={z[36]}&{w[37]}={z[37]}'

        r = requests.get(url=search_url, headers=headers)

        if r.status_code not in range(199, 299):
            logging.error("error with requests for getting recomended songs %s" % r.status_code)
            print(r.status_code)
            print(r.json())
            self.get_recomendation()
        data = r.json()

        try:
            tracks = data['tracks']
        except:
            tracks = []

        if len(tracks) == 0:
            logging.info('recommendation search had 0 tracks, rerunning')
            self.get_recomendation()

        sufficient = False

        for track in tracks:
            logging.info("RECOMMENDED TRACK %s", track['uri'][14:])
            if track['uri'][14:] not in playlist_tracks:
                print(f'adding {track["uri"]} to recommendations')
                c.execute("CREATE TABLE IF NOT EXISTS recommendedSongs (track_id TEXT, UNIQUE(track_id))")
                c.execute("INSERT OR IGNORE INTO recommendedSongs (track_id) VALUES (?)",(track['uri'],))
        conn.commit()

        c.execute("SELECT * FROM recommendedSongs")
        length = c.fetchall()
        if len(length) > 500:
            sufficient = True


        logging.info("tracks in self.recomended tracks %s" % self.recomended_tracks)

        if not sufficient:
            logging.info("Not enough tracks to run recommendation")
            self.get_recomendation()

        if decicion_tree:
            self.decision_tree_recommendation()

        return

    def recomend_seeds(self):
        """Is not used, file has since been saved and will ship with final builds"""

        endpoint = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
        headers = self.get_bearer_header()

        r = requests.get(url=endpoint, headers=headers)
        data = r.json()
        self.genre_recomended_seeds = data['genres']
        with open('/Users/jonnymurillo/untitled folder/xbox_one_vietnamese.txt', 'w') as f:
            for genre in data['genres']:
                f.write(f'{genre}\n')
            f.close()

    def decision_tree_recommendation(self,df_for_tree=None,samples_split=25):
        """Run decision tree with recommended songs before adding them
        :returns list for adding to playlist
        """
        conn = sqlite3.connect('test.db')
        c = conn.cursor()


        from sklearn import tree
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import OrdinalEncoder

        recommended_songs = []

        if df_for_tree is None:


            c.execute("SELECT * FROM recommendedSongs ORDER BY RANDOM() LIMIT 250")
            recommended_songs_db = c.fetchall()

            for song in recommended_songs_db:
                recommended_songs.append(song[0][14:])
            try:
                c.execute("SELECT * FROM sufficientAddToPlaylist ORDER BY RANDOM() LIMIT 50")
                sufficient_to_add = c.fetchall()
                for track in sufficient_to_add:
                    recommended_songs.append(track)
            except sqlite3.OperationalError:
                logging.info("NO SUFFICIENT TRACKS YET")
                pass
            df_for_tree = self.get_audio_features([j for j in recommended_songs],recommendation=True) #get audio features for list of songs

        conn = sqlite3.connect('test.db')
        c = conn.cursor()



        c.execute("SELECT * FROM userTrackFeatures")
        track_feat_raw = c.fetchall()
        user_feat_df = pd.DataFrame(track_feat_raw,columns=['Track ID','genre','danceability','energy','key','loudness','mode','speechiness',
                      'acousticness','instrumentalness','liveness','valence','tempo','popularity','playlist_track','top_track'])

        enc = OrdinalEncoder()

        tempo = user_feat_df['tempo']
        try:
            user_feat_df['tempo_0_1'] = (tempo - tempo.min()) / (tempo.max() - tempo.min())

            loudness = user_feat_df['loudness']
            user_feat_df['loudness_0_1'] = (loudness - loudness.min()) / (loudness.max() - loudness.min())

            tempo = df_for_tree['tempo']
            df_for_tree['tempo_0_1'] = (tempo - tempo.min()) / (tempo.max() - tempo.min())

            loudness = df_for_tree['loudness']
            df_for_tree['loudness_0_1'] = (loudness - loudness.min()) / (loudness.max() - loudness.min())

        except TypeError:
            pass

        user_feat_df['genre_code'] = enc.fit_transform(user_feat_df[['genre']])
        feat_df_no_none = user_feat_df.loc[user_feat_df['genre_code'] != 0]
        df_for_tree['genre_code'] = enc.fit_transform(df_for_tree[['genre']])



        clf = tree.DecisionTreeClassifier(min_samples_split=samples_split)
        X = feat_df_no_none[['genre_code', 'danceability', 'energy', 'key', 'loudness',
                             'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                             'valence', 'tempo', 'popularity']]
        y = feat_df_no_none[['playlist_track']]

        P = df_for_tree[['genre_code', 'danceability', 'energy', 'key', 'loudness',
                             'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                             'valence', 'tempo', 'popularity']]
        q = df_for_tree[['playlist_track']]

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=84, test_size=.25)

        clf.fit(X, y)
        y_pred_test = clf.predict(X_train)

        score = accuracy_score(y_pred_test,y_train)
        logging.info(f'SCORE + {score}')
        if score < .85:
            self.decision_tree_recommendation(df_for_tree, samples_split=random.randint(10,100))


        # clf.fit(P,q)
        pred = clf.predict(P)

        df_for_tree['pred'] = pred


        transfer_ls = []
        pred_like = df_for_tree.loc[df_for_tree['pred'] == 1]
        for i in pred_like['Track ID']:
            transfer_ls.append(i)

        conn.commit()

        print(f'adding transfer to playlist {transfer_ls}')
        if len(transfer_ls) < 4:
            for track in transfer_ls:
                c.execute("CREATE TABLE IF NOT EXISTS sufficientAddToPlaylist (track_id TEXT,UNIQUE(track_id))")
                c.execute("INSERT OR IGNORE INTO sufficientAddToPlaylist (track_id) VALUES (?)", [track])
            conn.commit()
            self.decision_tree_recommendation(df_for_tree, samples_split=random.randint(10,100))


        for track in transfer_ls:
            c.execute("CREATE TABLE IF NOT EXISTS sufficientAddToPlaylist (track_id TEXT,UNIQUE(track_id))")
            c.execute("INSERT OR IGNORE INTO sufficientAddToPlaylist (track_id) VALUES (?)",[track])
        conn.commit()
        return transfer_ls


"""
    def get_audio_analysis(self, songs_dict):
        
        Only use for small list of songs to test user preferences
        based on saved through my recomended playlist
        
        headers = self.get_bearer_header()
        print(headers)
        print('Getting audio analysis')
        w = 1
        for i, name in songs_dict.items():
            print(name)
            l = len(songs_dict) + 1
            print(f'{w} / {l}')
            w += 1
            endpoint = f'https://api.spotify.com/v1/audio-analysis/{i}'
            r = requests.get(url=endpoint, headers=headers)
            if r.status_code not in range(199, 299):
                print(r.status_code)
                print(r.json())
            data = r.json()
            sections = data['sections']
            self.audio_analysis[name] = []
            for sect in sections:
                analysis_dict = {"start": sect['start'], "duration": sect['duration'], "confidence": sect['confidence'],
                                 "loudness": sect['loudness'], "tempo": sect['tempo'],
                                 "tempo_confidence": sect['tempo_confidence'],
                                 "key": sect['key'], "key_confidence": sect['key_confidence'], "mode": sect['mode'],
                                 "mode_confidence": sect['mode_confidence'], "time_signature": sect['time_signature'],
                                 "time_signature_confidence": sect['time_signature_confidence']}
                self.audio_analysis[name].append(analysis_dict)
            time.sleep(1)

        keys = [k for k in self.audio_analysis.keys() for v in self.audio_analysis[k]]
        temp = list(songs_dict.values())
        if len(temp) == 0:
            return
        print('temp: {}'.format(temp))
        audio_analysis_df = pd.DataFrame(index=keys, columns=[x for x in self.audio_analysis[temp[0]][0].keys()],
                                         data=[v.values() for i, k in enumerate(self.audio_analysis.keys()) for v in
                                               self.audio_analysis[k]])
        return audio_analysis_df

"""


def click_accept(url, name, driver=None):
    """Opens up web browser to log in and authorize and get CODE for access/refresh Token

       # Eventually change to be used by any member with redirects for the app
    """
    success = True
    with open(PATH + f'Spotify_by_Jonny/{name}/Username_password.txt', 'r') as f:
        info = f.readlines()
        login_username = info[0]
        login_password = info[1]

    if browser[0] == 'safari':
        try:
            driver = Safari()
            driver.get(url)
        except:
            driver = Firefox()
            driver.get(url)


    elif browser[0] == 'Chrome':
        try:
            driver = Firefox()
            driver.get(url)
        except:
            driver = Chrome()
            driver.get(url)

    if driver == None:
        raise Exception ('ERROR GETTING DEFAULT BROWSER')


    auth_url = 'https://accounts.spotify.com/en/authorize?scope=user-read-private%20user-read-email%20user-top-read&response_type=code&redirect_uri=http:%2F%2Fsong-in-playlist-finder%2Fcallback&client_id=62d46cea622741b1b6013c64688e2dfa'
    login_url = 'https://accounts.spotify.com/en/login?continue=https:%2F%2Faccounts.spotify.com%2Fauthorize%3Fscope%3Duser-read-private%2Buser-read-email%2Buser-top-read%2Buser-library-read%2Bplaylist-modify-private%2Bplaylist-modify-public%2Buser-read-recently-played%2Bugc-image-upload%26response_type%3Dcode%26redirect_uri%3Dhttp%253A%252F%252Fsong-in-playlist-finder%252Fcallback%26client_id%3D62d46cea622741b1b6013c64688e2dfa'
    username_input = driver.find_element_by_xpath('//*[@id="login-username"]')
    username_input.send_keys(login_username)
    password_input = driver.find_element_by_xpath('//*[@id="login-password"]')
    password_input.send_keys(login_password)
    login_button = driver.find_element_by_xpath('//*[@id="login-button"]')
    login_button.send_keys(Keys.ENTER)
    time.sleep(2)
    if driver.current_url == login_url:
        success = False
    if driver.current_url == auth_url:
        driver.find_element_by_xpath('//*[@id="auth-accept"]').click()
    try:
        auth = driver.find_element_by_xpath('//*[@id="auth-accept"]')
        auth.click()
    except:
        pass
    final_url = driver.current_url
    print('Final Url: ')
    print(final_url)
    driver.close()
    return final_url, success


class SpotifyAPI(object):
    """Set nonetype variables that will change for each user."""
    success_auth = None
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'
    auth_url = 'https://accounts.spotify.com/authorize'
    refresh_token = None
    user_email = None
    user_id = None
    user_top_artists = {}
    user_top_genres = {}
    user_top_tracks = {}
    user_playlists = {}
    user_playlist_tracks = {}
    user_library_tracks = {}
    user_tracks = []
    user_playback = {}
    recomended_tracks = []  # Recomended tracks have ID and URI for adding to playlist


    def __init__(self,name, client_id, client_secret, redirect_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.name = name
        self.perform_auth()


    def get_client_cred(self):
        """
        returns base64 str for client credentials
        """
        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == 0 or client_secret == 0:
            raise ValueError

        authorization = client_id + ':' + client_secret
        client_b64 = base64.b64encode(authorization.encode())
        return client_b64

    def get_token_header(self):
        """
        :return token header for url to get access token
        """

        client_b64 = self.get_client_cred()
        return {
            'Authorization': f'Basic {client_b64.decode()}'
        }

    def get_token_data(self):
        """
        token data for getting our access token
        """
        return {
            'response_type': 'code',
            'client_id': f'{self.client_id}',
            'scope': 'user-read-private user-read-email user-top-read user-library-read playlist-modify-private playlist-modify-public user-read-recently-played ugc-image-upload',
            'redirect_uri': f'{self.redirect_uri}'
        }

    def get_bearer_header(self):
        """
        When access token is received use it for the header to get user info
        """

        return {
            'Authorization': f'Bearer {self.access_token}'
        }

    def perform_auth(self,first_run=False):
        """
        Returns the access token if the status code is valid

        Run this daily, otherwise run get token first. If it is expired it will automatically run this
        """

        token_data = self.get_token_data()
        token_headers = self.get_token_header()

        a = requests.get(url=self.auth_url, params=token_data)
        print('perform auth URL')
        print(a.url)
        if first_run:
            os.system(f'open {a.url}')
            return
        auth_url, self.success_auth = click_accept(url=a.url,name=self.name)  # auto opens for the user to retreive code

        if self.success_auth == False:
            root = tk.Tk()
            app = LoginInfo(root,wrong_info=True)
            app.mainloop()

            while app.running:
                time.sleep(2)

        auth_url = str(auth_url.split())
        code = auth_url
        code = code[47:-2]  # code from the url

        code_payload = {
            'grant_type': 'authorization_code',
            'code': f'{code}',
            'redirect_uri': f'{self.redirect_uri}',
        }

        r = requests.post(self.token_url, data=code_payload, headers=token_headers)
        if r.status_code not in range(200, 299):
            logging.error('error with performing auth %s', r.status_code)
            print(r.status_code)
            raise Exception("Couldn't authenticate client")

        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
        refresh_token = data['refresh_token']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        print("expiration: ")
        print(expires)
        self.refresh_token = refresh_token

        return True

    def get_access_token(self):
        """return access token to use if it is expired"""
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_user_profile(self):
        """
        Get the users profile and assign the user ID to be used to keep users data interally
        """
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()  # ALWAYS RUN THIS WHEN RETREIVING DATA
        elif self.refresh_token == None or self.access_token == None:
            self.perform_auth()
        headers = self.get_bearer_header()
        endpoint = 'https://api.spotify.com/v1/me'
        r = requests.get(url=endpoint, headers=headers)
        data = r.json()
        if r.status_code not in range(200, 299):
            print(r.status_code)
            print(r.json())
            return {}
        self.user_email = data['email']
        print('User ID: ')
        self.user_id = data['id']
        with open(PATH + f'Spotify_by_Jonny/{self.name}/User_Info.txt', 'w') as user_f:
            user_f.write(str(self.user_id))
            user_f.close()
        print(self.user_id)

        return data

    def search(self, query, search_type='artist'):
        """
        Search for anything in Spotify Library
        """
        headers = self.get_bearer_header()
        endpoint = 'https://api.spotify.com/v1/search'
        params = urlencode({'q': query, 'type': search_type.lower()})
        # EX: "href": "https://api.spotify.com/v1/search?query=tania+bowra&offset=0&limit=20&type=artist"
        search_url = f'{endpoint}?{params}'
        r = requests.get(url=search_url, headers=headers)
        if r.status_code not in range(199, 299):
            print(r.status_code)
            print(r.json())
            return {}
        return r.json()

    def artist_genres(self ,artist_id):
        """return the genres of a given artist
        Mainly used in UserPref
        """
        headers = self.get_bearer_header()
        endpoint = f'https://api.spotify.com/v1/artists/{artist_id}'

        r = requests.get(url=endpoint ,headers=headers)
        if r.status_code not in range(199, 299):
            logging.error('error with retreiving track details for artist id %s', artist_id)
            print(r.status_code)
            print(r.json())
            return {}
        data = r.json()
        genres = data['genres']
        return genres

    def track_details(self ,track_id):
        """return the genre to be used in creating user pref DF
        Mainly used in UserPref
        """
        headers = self.get_bearer_header()
        endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'

        r = requests.get(url=endpoint, headers=headers)
        if r.status_code not in range(199, 299):
            logging.error('error with retreiving track details for track id %s', track_id)
            print(r.status_code)
            print(r.json())
            return {}
        data = r.json()
        artist_id = data['artists'][0]['id']
        popularity = data['popularity']

        return artist_id, popularity

    def get_user_top_artists_and_tracks(self, type='artists', time_range='long_term', limit=50):
        """
        Find the users top artists and tracks and add them to Class dictionary for user
        """

        print('getting user tracks')
        headers = self.get_bearer_header()
        endpoint = f'https://api.spotify.com/v1/me/top/{type.lower()}'
        query_params = urlencode({'time_range': f'{time_range}', 'limit': f'{limit}'})

        search_url = f'{endpoint}?{query_params}'
        r = requests.get(url=search_url, headers=headers)
        if r.status_code not in range(199, 299):
            print(r.status_code)
            print(r.json())
            return {}
        data = r.json()
        items = data['items']

        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS userTracks (track_id TEXT,UNIQUE(track_id))")

        if type == 'artists':
            for i in range(len(items)):
                name = items[i]['name']
                artist_genres = items[i]['genres']
                for genre in artist_genres:
                    if genre not in self.user_top_genres:
                        self.user_top_genres[genre] = 0
                    elif genre in self.user_top_genres:
                        self.user_top_genres[genre] += 1
                artist_id = items[i]['id']
                self.user_top_artists[artist_id] = name
        if type == 'tracks':
            for i in range(len(items)):
                i = int(i)
                track_name = items[i]['name']
                track_id = items[i]['id']
                self.user_top_tracks[track_id] = track_name
                c.execute("INSERT OR IGNORE INTO userTracks (track_id) VALUES (?)", [track_id])
        conn.commit()
        return data

    def get_user_playlists(self):
        """
        Get users play lists with id, name, and URL
        """
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        headers = self.get_bearer_header()
        endpoint = 'https://api.spotify.com/v1/me/playlists'

        search_url = f'{endpoint}'
        r = requests.get(url=search_url, headers=headers)
        if r.status_code not in range(199, 299):
            print(r.status_code)
            print(r.json())
            return {}
        data = r.json()
        items = data['items']


        c.execute("CREATE TABLE IF NOT EXISTS userPlaylists (playlist_id TEXT, playlist_name TEXT, playlist_tracks TEXT,UNIQUE(playlist_id))")
        for i in range(len(items)):
            playlist_id = items[i]['id']
            playlist_name = items[i]['name']
            tracks_in_playlist = self.user_tracks_in_playlist(playlist_id)
            dump = [json.dumps(tracks_in_playlist)]
            c.execute("INSERT OR IGNORE INTO userPlaylists (playlist_id, playlist_name,playlist_tracks) VALUES (?, ?, ?)"
                      ,(playlist_id, playlist_name,json.dumps(tracks_in_playlist)))
        conn.commit()
        return data


    def get_user_library(self):
        headers = self.get_bearer_header()
        endpoint = 'https://api.spotify.com/v1/me/tracks'

        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS userTracks (track_id TEXT,UNIQUE(track_id))")

        limit = 50
        offset = 0
        while offset < 450:
            query_params = urlencode({'limit': f'{limit}', 'offset': f'{offset}'})
            search_url = f'{endpoint}?{query_params}'

            r = requests.get(url=search_url, headers=headers)
            if r.status_code not in range(199, 299):
                print(r.status_code)
                print(r.json())
                return {}
            data = r.json()
            items = data['items']
            for i in range(len(items)):
                lib_track_id = items[i]['track']['id']
                lib_track_name = items[i]['track']['name']
                # lib_track_added_at = items[i]['added_at']
                c.execute("INSERT OR IGNORE INTO userTracks (track_id) VALUES (?)",[lib_track_id])
            offset += limit - 1
        conn.commit()
        return


    def find_user_routines(self):
        """find playback for user time frame throughout the day
        Batch1: before noon
        Batch2: noon to six
        Batch3: after six
        """
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        # Get the user timestamp. UNIX MILISECONDS
        date = datetime.datetime.now().date()
        date = str(date)
        year = int(date[0:4])
        month = date[5:7]
        if month[0] == '0':
            month = int(month[-1])
        else:
            month = int(month)
        day = date[-2:len(date)]
        if day[0] == '0':
            day = int(day[-1])
        else:
            day = int(day)

        nine = datetime.datetime(year, month, day, hour=5, minute=0)
        noon = datetime.datetime(year, month, day, hour=6, minute=0)
        six = datetime.datetime(year, month, day, hour=10, minute=0)
        batch1_time = nine.replace(tzinfo=timezone.utc).timestamp()
        batch2_time = noon.replace(tzinfo=timezone.utc).timestamp()
        batch3_time = six.replace(tzinfo=timezone.utc).timestamp()

        batch1_time = int(batch1_time)
        batch2_time = int(batch2_time)
        batch3_time = int(batch3_time)

        print(f'batch1 time: {batch1_time}')
        batch_1_list = self.get_user_playback(batch=1, before=batch1_time)
        print(f'batch2 time: {batch2_time}')
        batch_2_list = self.get_user_playback(batch=2, after=batch1_time)
        # print(f'batch3 time: {batch3_time}')
        # self.get_user_playback(batch=3,after= batch3_time)

        print('running audio analysis on batch 1')
        Recommendation.get_audio_features(batch_1_list, routines=True, batch=1)
        print('running audio analysis on batch 2')
        Recommendation.get_audio_features(batch_2_list, routines=True, batch=2)

        conn.commit()


    def user_tracks_in_playlist(self,playlist_id):
        """parse through playlist and find songs"""

        headers = self.get_bearer_header()
        print('User Playlists ID')
        print(playlist_id)
        query_params = urlencode({'fields': 'items.track(id, name)'})
        # print(f'QUERY PARAMS FOR TRACKS IN PLAYLIST {query_params}')
        # print('COMPARARISON:                        fields=items(added_by.id%2Ctrack(name%2Chref%2Calbum(name%2Chref)))')

        user_playlist_tracks = []


        endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?{query_params}'
        r = requests.get(url=endpoint, headers=headers)
        if r.status_code not in range(199, 299):
            print(r.status_code)
            print(r.json())
            return {}
        data = r.json()
        items = data['items']
        for i in range(len(items)):
            track_id = items[i]['track']['id']
            user_playlist_tracks.append(track_id)
        return user_playlist_tracks


    def get_playlist_songs(self):
        """ONLY USE FOR V1 RELEASE TO GET USERS DATA"""
        """Get list of uri from hourly playlist"""
        with open(PATH + f'Spotify_by_Jonny/{self.name}/Playlist_File.txt', 'r') as file:
            playlist_id = file.readlines()
            playlist_id = playlist_id[0]
            file.close()

        list_of_uri = []
        headers = self.get_bearer_header()
        print(playlist_id)
        endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

        r = requests.get(url=endpoint, headers=headers)
        print("getting playlist songs")
        if r.status_code not in range(199, 299):
            logging.error("error with requests for getting playlist songs %s" % r.status_code)
            print(r.status_code)
            print(r.json())
        data = r.json()
        items = data['items']
        for i in range(len(items)):
            track = items[i]['track']
            uri = track['uri']
            list_of_uri.append(uri)

        return list_of_uri


    def sort_user_tracks(self):
        """loop through all saved user tracks. Put them all into one dictionary"""
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS userTracks (track_id TEXT,UNIQUE(track_id))")
        c.execute("CREATE TABLE IF NOT EXISTS userTop (top_genres TEXT, top_artists TEXT, top_tracks TEXT, UNIQUE(top_genres))")

        c.execute("SELECT playlist_tracks FROM userPlaylists")
        playlist_tracks = {}
        placeholder = c.fetchall()
        print(placeholder)


        for i in placeholder:
            for playlist in i:
                tracks = json.loads(playlist)
                for track in tracks:
                    playlist_tracks[track] = 0

        top_tracks = self.user_top_tracks
        lib_tracks = self.user_library_tracks
        playlist_tracks = playlist_tracks
        for list in [top_tracks, lib_tracks, playlist_tracks]:
            for track_id, name in list.items():
                if list[track_id] not in self.user_tracks:
                    c.execute("INSERT OR IGNORE INTO userTracks (track_id) VALUES (?)", ([track_id]))

        c.execute("INSERT OR IGNORE INTO userTop (top_genres,top_artists,top_tracks) VALUES (?, ?, ?)", (
        json.dumps(self.user_top_genres), (json.dumps(self.user_top_artists)), (json.dumps(self.user_top_tracks))))
        conn.commit()


    def get_user_playback(self, batch, before=None, after=None, limit=50):
        """Get user playback based on the time of day"""
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        now = datetime.datetime.now()
        thirty_days_ago = now - datetime.timedelta(days=30)
        thirty_days_ago = float(thirty_days_ago.timestamp())
        now = time.time()
        try:
            c.execute("SELECT track_id FROM playbackTracks")
            playback_len = c.fetchall()
            if len(playback_len) > 7000:
                c.execute("DELETE FROM playbackTracks WHERE timestamp>?", (thirty_days_ago,))
                conn.commit()
        except sqlite3.OperationalError:
            pass

        if before == after:
            raise ValueError('cant have begin and end time frame the same')

        headers = self.get_bearer_header()
        endpoint = 'https://api.spotify.com/v1/me/player/recently-played'

        if before:
            search_url = f'{endpoint}?limit={limit}&before={before}'
        elif after:
            search_url = f'{endpoint}?limit={limit}&after={after}'

        r = requests.get(url=search_url, headers=headers)
        if r.status_code not in range(199, 299):
            logging.debug('error with getting user playback %s', r.status_code)
            print(r.status_code)
            print(r.json())
            return {}

        data = r.json()
        items = data['items']
        track_id_list = []
        for item in items:
            track_id_list.append(item['track']['id'])

        return track_id_list


    def playlist_picture(self):
        """Change photo of playlist"""

        with open("/Users/jonnymurillo/Desktop/Python_Code/Spotify_Cover.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            image_file.close()

        headers = self.get_bearer_header()
        headers['Content-Type'] = 'image/jpeg'
        data = {'data': encoded_string}
        with open(PATH + f'Spotify_by_Jonny/{self.name}/Playlist_File.txt', 'r') as f:
            playlist_id = f.readlines()
            playlist_id = playlist_id[0]

        endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/images'
        try:
            r = requests.put(url=endpoint, data=data, headers=headers)
            if r.status_code not in range(199, 299):
                logging.debug('error with uploading photo %s', r.status_code)
                print(r.status_code)
                print(r.json())
                return {}
            if r.status_code == 413:
                return False
        except:
            return False


    def return_user_tracks(self):
        """Run all programs to populate self. items"""
        print('returning user tracks')
        self.get_access_token()
        self.get_user_top_artists_and_tracks(type='artists')
        self.get_user_top_artists_and_tracks(type='tracks')
        self.get_user_library()
        self.get_user_playlists()
        self.sort_user_tracks()

        return "Successfully populated user tracks"


    def add_to_playlist(self):
        """
           :param batch which batch to add to
                    default = 0
        """
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        c.execute("SELECT * FROM sufficientAddToPlaylist")
        recomended_songs = c.fetchall()

        logging.info("Removing from playlist")
        self.remove_from_playlist()

        with open(PATH + f'Spotify_by_Jonny/{self.name}/Playlist_File.txt', 'r') as f:
            playlists = f.readlines()
            hourly_playlist_id = playlists[0]
            f.close()
        """
        Return song uri for removal and adding to combined playlist
        """
        headers = self.get_bearer_header()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'

        print('adding to hourly playlist')
        logging.info("recommended songs are %s", recomended_songs)
        for uri in recomended_songs:
            logging.info('songs to be added to hourly %s' % uri)
            endpoint = f'https://api.spotify.com/v1/playlists/{hourly_playlist_id}/tracks'
            add_url = f'{endpoint}'
            data = {'uris': f'spotify:track:{uri[0]}'}

            r = requests.post(url=add_url, params=data, headers=headers)

            if r.status_code not in range(199, 299):
                logging.error("error with adding songs to hourly playlist %s" % r.status_code)
                print(r.status_code)
                print(r.json())
                return {}
            print(f'added songs with uri: {uri}')
        return datetime.datetime.now()

    def remove_from_playlist(self):
        """No need to call this. When add_to_playlist(saved) runs it will remove from playlist"""
        songs_uri = self.get_playlist_songs()
        headers = self.get_bearer_header()
        print(f'Removing: {[x[0:-1] for x in songs_uri]}')

        with open(PATH + f'Spotify_by_Jonny/{self.name}/Playlist_File.txt', 'r') as f:
            playlists = f.readlines()
            hourly_playlist_id = playlists[0]
            f.close()
        for uri in songs_uri:
            endpoint = f'https://api.spotify.com/v1/playlists/{hourly_playlist_id}/tracks'
            data = {'tracks': [{'uri': f'{str(uri)}'}]}

            remove_url = f'{endpoint}'
            print(f'data for dumps: {data}')
            print(f'removed {str(uri)} from hourly playlist')

            r = requests.delete(url=remove_url, data=json.dumps(data), headers=headers)
            if r.status_code not in range(199, 299) and range(499, 599):
                logging.error("error with removing %s" % uri, "songs from playlist songs %s" % r.status_code)
                print(r.status_code)
                print(r.json())
                print(r.content)
                self.remove_from_playlist()
            if r.status_code in range(499, 599):
                print('server error try again later')
                print('waiting for 1 minutes')
                time.sleep(30)
                self.remove_from_playlist()
        return

    def create_playlist(self, playlist_name1, playlist_name2=None, multiple=False):
        """
        Create Empty Playlist
        DOES NOT ADD SONGS TO PLAYLIST
        ONLY RUN TO INITIALIZE
        ADD PLAYLIST ID TO FILE
        """
        created_playlist = False
        headers = self.get_bearer_header()
        print(headers)
        with open(PATH + f'Spotify_by_Jonny/{self.name}/User_Info.txt', 'r') as user_f:
            lines = user_f.readlines()
            user_id = lines[0]
            user_f.close()

        print(f'user id for creating playlist: {user_id}')
        endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        data1 = {
            'name': f'{playlist_name1}'
        }
        jdata1 = json.dumps(data1)


        r = requests.post(url=endpoint, data=jdata1, headers=headers)
        if r.status_code not in range(199, 299):
            logging.error("error with requests for creating %s" % r.status_code)
            print(r.status_code)
            print(r.json())
            return {}
        data1 = r.json()
        id_1 = data1['id']

        if not multiple:
            try:
                with open(PATH + f'/Spotify_by_Jonny/{self.name}/Playlist_File.txt', 'w') as f:
                    f.write(id_1)
                    f.close()
                    created_playlist = True
            except:
                raise ValueError

class CreateFiles:

    def __init__(self, name):
        self.name = name

    def create_begin_files(self):
        """Only run this when first creating program"""
        FileExists = False
        spotify_path = (PATH + '/Spotify_by_Jonny/')
        try:
            new_file = os.makedirs(PATH + f'Spotify_by_Jonny/{self.name}/')
            print(f'/Spotify_by_Jonny has been created in {PATH} :)')
        except FileExistsError or UnboundLocalError:
            FileExists = True
            print('file already exists')
            pass

        return FileExists

    def create_sub_starter_files(self, begin=False, additional_files=False, file_to_create=None):
        """
        :param begin: is this the first time the program is running?
        :param additional_files: is this an aditional file being stored?
        :param file_to_create: str, do not add .txt
        """
        user_dir = PATH + f'Spotify_by_Jonny/{self.name}/'
        created_files = False
        DATA = ['User_Info', 'Playlist_File', 'Username_password']
        if begin:
            for f in DATA:
                if f not in user_dir:
                    file = os.path.join(user_dir, f + ".txt")
                    with open(file, 'w') as file1:
                        time.sleep(.2)
                        file1.close()
        if additional_files:
            file = os.path.join(user_dir, file_to_create + '.txt')
            with open(file, 'w') as file1:
                time.sleep(.2)
                file1.close()
        try:
            for f in DATA:
                open(user_dir + f + ".txt")
                created_files = True
        except:
            raise FileNotFoundError

        return created_files



class LoginInfo(tk.Frame):
    pw = None
    un = None
    running = True

    def __init__(self,master,wrong_info=False):
        super().__init__(master)
        self.pack()

        if wrong_info:
            self.login_label = tk.Label(master, text="Your info was incorrect, please enter again")
        else:
            self.login_label = tk.Label(master, text="Enter your Spotify Username and Password")
        self.login_label.pack(side='top', expand=True)
        self.username_lbl = tk.Label(master,text='Username')
        self.password_lbl = tk.Label(master, text='Password')

        self.B = tk.Button(master, text="Enter ;)", command=self.store_info)
        self.B.pack(side='bottom')


        self.USERNAME = tk.Entry(master)
        self.USERNAME.pack(side='top')


        self.PASSWORD = tk.Entry(master)
        self.PASSWORD.pack(side='bottom')


        self.login_username = tk.StringVar()
        self.login_username.get()
        self.login_username.set('username')
        self.login_password = tk.StringVar()
        self.login_password.set('password')
        self.login_password.get()


        self.USERNAME['textvariable'] = self.login_username
        self.PASSWORD['textvariable'] = self.login_password

        master.protocol("WM_DELETE_WINDOW", func=self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()


    def store_info(self):

        self.un = self.login_username.get()
        self.pw = self.login_password.get()
        self.running = False
        self.master.destroy()






if __name__ == '__main__':
    global browser
    browser = []
    if platform.system() == 'Darwin':  # macOS
        browser.append('safari')
    elif platform.system() == 'Windows':  # Windows
        browser.append('chrome')
        browser.append('firefox')
    else:  # linux variants
        browser.append('chrome')
        browser.append('firefox')

    feature = input('What do you want to do?\n-s to set up your account\n\n-r to run run recommendation\n\n')

    if feature == '-s':
        rec = CreateFiles('hehe')
        file = rec.create_begin_files()
        if file:
            sp = SpotifyAPI('hehe', client_id, client_secret, redirect_uri)
            sp.return_user_tracks()
            rec = Recommendation('hehe', client_id, client_secret, redirect_uri)
            rec.get_audio_features()
        else:
            os.system(
                f'open "https://accounts.spotify.com/en/authorize?scope=user-read-private%20user-read-email%20user-top-read&response_type=code&redirect_uri=http:%2F%2Fsong-in-playlist-finder%2Fcallback&client_id=62d46cea622741b1b6013c64688e2dfa"')
            time.sleep(25)
            root = tk.Tk()
            app = LoginInfo(root)
            app.mainloop()
            while app.running:
                time.sleep(1)

            rec.create_sub_starter_files(begin=True)
            login_username = app.un
            login_password = app.pw
            with open(PATH + f'Spotify_by_Jonny/{rec.name}/Username_password.txt', 'w') as f:
                f.write(f'{login_username}\n')
                f.write(login_password)
                f.close()
            sp = SpotifyAPI('hehe', client_id, client_secret, redirect_uri)
            sp.get_user_profile()
            sp.create_playlist('LITLITLIT')
            sp.return_user_tracks()
            rec = Recommendation('hehe', client_id, client_secret, redirect_uri)
            rec.get_audio_features()



    elif feature == '-r':
        rec = Recommendation('hehe',client_id,client_secret,redirect_uri)
        rec.get_recomendation(decicion_tree=True)
        s = SpotifyAPI('hehe',client_id,client_secret,redirect_uri)
        s.add_to_playlist()
    else:
        print("invalid input\n\n use '-s' or '-r' after rerunning program")
        sys.exit()

