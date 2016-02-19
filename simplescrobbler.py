#!/usr/bin/env python3
import hashlib
import urllib.request, urllib.parse
import time
import os
import os.path
import sys
import json
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

api_key = ''
secret = ''
base = 'http://ws.audioscrobbler.com/2.0/'
basehttps = 'https://ws.audioscrobbler.com/2.0/'


username = os.environ.get('LASTFM_USERNAME')
password = os.environ.get('LASTFM_PASSWORD')

def sign(text):
    m = hashlib.md5()
    texte = text.encode('utf-8')
    m.update(texte)
    md5 = m.hexdigest()
    return md5

def gettoken(baseuri, key, sig):
    try:
        gettokenuri = baseuri + '?method=auth.gettoken&api_key=' + key + '&api_sig=' + sig + '&format=json'
        token = urllib.request.urlopen(gettokenuri).read()
    except Exception as e:
        return 0

    t = token.decode("utf-8")
    return t

def getMobileSessionKey(usern, passwd, key, sig):
    if not os.path.isfile("storesession") or os.stat("storesession").st_size == 0:
        values = {'password' : passwd, 'username' : usern, 'api_key' : key, 'api_sig' : sig, 'format' : 'json'}

        resp = postRekt(basehttps, values, apiMethod='auth.getMobileSession')

        dresp = resp.decode("utf-8")
        jresp = json.loads(dresp)
        s = open('storesession', 'a')
        s.write(jresp['session']['key'])
        s.close()
        return jresp['session']['key']
    else:
        s = open('storesession', 'r')
        session = s.read()
        s.close()
        return session

def getApiSignature(key, passwd, usern, scrt):
    tsgn = 'api_key' + key + 'methodauth.getMobileSession' + 'password' + passwd + 'username' + usern + scrt
    if not os.path.isfile("storesignature") or os.stat("storesignature").st_size == 0:
        apisig = sign(tsgn)
        s = open('storesignature', 'a')
        s.write(apisig)
        s.close()
        return apisig
    else:
        s = open('storesignature', 'r')
        apisig = s.read()
        s.close()
        return apisig

def postRekt(uri, body, apiMethod):
    try:
        data = urllib.parse.urlencode(body)
        data = data.encode('utf-8') # data should be bytes
        req = urllib.request.Request(uri + '?method=' + apiMethod)
        req.add_header("User-Agent","Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0")
        resp = urllib.request.urlopen(req, data).read()
        return resp
    except Exception as e:
        print(e)
        print(e.read())
        return 0

def scrobbler(album, key, artist, duration, sk, timestamp, track, trackNum, scrt):
    tsgn = 'album' + album + 'api_key' + key + 'artist' + artist + 'duration' +  str(duration) + 'methodtrack.scrobble' + 'sk' + sk + 'timestamp' + str(timestamp) + 'track' + track + 'trackNumber' + str(trackNum) + scrt
    sgn = sign(tsgn)
    values = {'artist' : artist, 'track' : track, 'timestamp' : timestamp, 'album' : album, 'trackNumber' : trackNum, 'duration' : duration, 'api_key' : key, 'api_sig' : sgn, 'sk' : sk, 'format' : 'json'}
    resp = postRekt(base, values, apiMethod='track.scrobble')
    dresp = resp.decode("utf-8")
    jresp = json.loads(dresp)
    return jresp['scrobbles']['@attr']['accepted']


def main():
    if len(sys.argv) < 1 or len(sys.argv) > 2:
        print("You have to pass a path to a song as an argument to the program")
        return 0
    else:
        try:
            track = MP3(sys.argv[1])
        except Exception as e:
            print("Error opening the song:" + str(sys.argv[1]))
            return 0

        # Authentication
        apisig = getApiSignature(api_key, password, username, secret)
        session = getMobileSessionKey(username, password, api_key, apisig)

        # Scrobble track
        timestamp = int(time.time())
        scrobbler(track["TALB"].text[0], api_key, track["TPE1"].text[0], track.info.length, session, timestamp, track["TIT2"].text[0], track["TRCK"].text[0], secret)

        return 1

if __name__ == '__main__':
  main()
