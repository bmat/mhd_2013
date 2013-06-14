import os, web, json
import pyella
import re
import random
import datetime

import gdata.photos.service
from get_words import get_words, get_keywords
from get_lyrics import get_lyrics, get_image_lyrics

import os
import sys
import time
import urllib2
import simplejson

cache = dict()

def search_images(query, rand=False):
    # Define search term
    searchTerm = query
    # Replace spaces ' ' in search term for '%20' in order to comply with request
    searchTerm = searchTerm.replace(' ','%20')

    # Set count to 0
    images = []
    for i in range(0,1):
        if rand:
            start = random.randint(0,4)
        else:
            start = 0
        # Notice that the start changes for each iteration in order to request a new set of images for each loop
        url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 
               'v=1.0&q='+searchTerm+'&start='+ str(start) + '&userip=MyIP&imgtype=photo&imgsz=xxlarge')
        print url
        request = urllib2.Request(url, None, {'Referer': 'testing'})
        response = urllib2.urlopen(request)

        # Get results using JSON
        results = simplejson.load(response)
        data = results['responseData']
        dataInfo = data['results']
        print "Images for %s are %s"  %(searchTerm,  len(dataInfo))
        random.seed(datetime.datetime.now())
        image = random.randint(0, len(dataInfo) -1)

        # Iterate for each result and get unescaped url
        #for myUrl in dataInfo:
        myUrl = dataInfo[image]
        print myUrl['unescapedUrl']
        images = myUrl['unescapedUrl']
        #myopener.retrieve(myUrl['unescapedUrl'],str(count)+'.jpg')

        # Sleep for one second to prevent IP blocking from Google
        time.sleep(1)
        return images
    return images

#Google Photo Service
gd_client = gdata.photos.service.PhotosService()
gd_client.password = "mhdvideoclipr"
gd_client.email = "videoclipr@gmail.com"
gd_client.ProgrammaticLogin()

#
#
#for p in photos.entry:
#    print p.content.src

# render
render = web.template.render( os.path.dirname(__file__) + '/templates/')

# db connect

abspath = os.path.dirname(__file__)
os.chdir(abspath)

urls = (
    '/', 'init',
    '/search', 'search',
    '/player', 'player',
    )
app = web.application(urls, globals())

apikey = "905e7eec68193e3f0a81a75591b4a518"


class videclipr(object):

    def __init__(self):
        self.lyrics = None
        self.subtitles = None
        self.images = None
        self.title = None
        self.artist = None
        self.bpm = None
        self.moods = None
        self.audio = None
        self.isrc = None
        self.label = None
        self.duration = None
        self.cover = None

    def toJSON(self):
        j = dict()
        j['lyrics'] = self.lyrics
        j['subtitles'] = self.subtitles
        j['images'] = self.images
        j['title'] = self.title
        j['artist'] = self.artist
        if self.bpm:
            self.bpm = int(float(self.bpm))
        j['bpm'] = self.bpm
        j['moods'] = self.moods
        j['isrc'] = self.isrc
        j['label'] = self.label
        j['duration'] = self.duration
        j['cover'] = self.cover
        j['audio'] = self.audio.replace("/clips", "")
        return json.dumps(j)

    def setLyric(self, lyric):
        self.lyrics = get_lyrics(lyric)


    def set_photos(self, photos):
        print photos
        self.images = photos
        print self.images

def get_mbi_from_url(url):
    mbi = url.replace("http://musicbrainz.org/track/", "")
    mbi = mbi.replace(".html", "")
    return mbi

def request_to_json(url):
    import urllib2
    req = urllib2.Request(url, None, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    json_dict = json.loads(response)
    f.close()
    return json_dict


def get_musixmatch_lyric(mbid, type_track="track_mbid"):
    url = ("http://api.musixmatch.com/ws/1.1/track.subtitle.get"
            "?%s=%s&"
           "apikey=%s&format=json" % (type_track, mbid, apikey))
    json = request_to_json(url)
    print json
    #TODO: Check if the message is correct
    if json['message']['header']['status_code'] in [404, 401]:
        return None
    return json['message']['body']['subtitle']['subtitle_body']


def get_musixmatch_lyric_by_query(query):
    url = ("http://api.musixmatch.com/ws/1.1/"
            "track.search?q=%s&f_has_lyrics=1&format=json&apikey=%s"
           % (query, apikey))
    json = request_to_json(url)
    if json['message']['header']['status_code'] in [404, 401]:
        return None
    track_id = json['message']['body']['track_list'][0]['track']['track_id']
    print track_id
    return get_musixmatch_lyric(track_id, "track_id")

def return_composite_parts(main):
    header = unicode(render.header())
    footer = unicode(render.footer())
    return render.layout(header, main, footer)


class init:
    def GET(self):
        main = unicode(render.start(self))
        return return_composite_parts(main)

class player:
    def GET(self):
        data = web.input()
        self.query = data.get("q")
        main = unicode(render.main(self))
        return return_composite_parts(main)


class search:
    def GET(self):
        self.cache_key = None
        self.lyric = ""
        self.words = None
        self.error = None
        self.photos = []
        obj = videclipr()
        data = web.input()
        query = data.get("q")
        next_song = int(data.get('next', 0))
        print "Finding track %s" % query
        results = pyella.search_tracks(query, "fulltracks").get_next_page()
        print results
        print len(results)
        if results:
            if next_song > len(results) - 1:
                next_song = 0
            print "Ela results " ,len(results), next_song
            track = results[next_song]
            self.cache_key = str(track.get_id())
            if self.cache_key in cache:
                    return cache[self.cache_key]
            print track.get_mbid(), track.get_title(), track.get_artist_name()
            print track.get_attribute("rhythm_bpm_value")
            print track.get_audio()
            obj.title = track.get_title()
            obj.artist = track.get_artist_name()
            obj.bpm = track.get_attribute("rhythm_bpm_value")[0][1:]
            obj.audio = track.get_audio()
            obj.isrc = track.get_attribute("track_isrc")
            obj.duration = track.get_attribute('track_duration')
            print obj.isrc
            obj.label = track.get_attribute("track_label")
            print obj.label
            obj.cover = track.get_image()
            links = track.get_links()
            mblink = links[3][1]
            if mblink:
                #Here we have the MusicBrainz ID
                mbid = get_mbi_from_url(mblink)
                self.lyric = get_musixmatch_lyric(mbid)
                #print self.lyric
                obj.setLyric(self.lyric)
            else:
                #print "No MusicBrainz ID found... trying with musixmatch"
                self.lyric = get_musixmatch_lyric_by_query(track.get_title())
                obj.setLyric(self.lyric)
        else:
            self.error = "Music not found in ELLA! Please try another song"
        if not self.lyric:
            self.error = "Can't found lyrics for this song. :("
        if self.lyric:
            self.time_lyrics = get_lyrics(self.lyric)
            self.keywords = get_keywords(self.lyric)
            self.image_lyrics = get_image_lyrics(self.keywords, self.time_lyrics)

            #self.words = get_words(self.lyric)
            #self.lyric = re.sub(r"\n", "<br/>", self.lyric)
            self.photos = []
            #self.lyrics = get_lyrics(self.lyric)
            #for count, key in enumerate(self.words):
            #    word = self.words[key][0][0]
            #    print "Finding photos for word %s" % word
            #    phs = gd_client.SearchCommunityPhotos(word, limit='20')
            #    photos_array = [p.content.src for p in phs.entry]
            #    #photos_array = search_images(word)
            for i, item in enumerate(self.image_lyrics):
                keyword = item[1]
                #print 'keyword:', keyword
                #phs = gd_client.SearchCommunityPhotos(keyword, limit='1')
                #self.photos.extend([p.content.src for p in phs.entry])
                rand = False
                if not keyword:
                    keyword = track.get_title() + ' ' + track.get_artist_name()
                    rand = True
                print "Searching for %s" % keyword
                if i > 25:
                    break
                photos = search_images(keyword, rand)
                #random.shuffle(photos_array)
                self.photos.append([item[0], photos])
            obj.set_photos(self.photos)
        #main = unicode(render.main(self))
        #return return_composite_parts(main)
        j = obj.toJSON()
        cache[self.cache_key] = j;
        return j

    def POST(self):
        main = unicode(render.main(self))
        data = web.input()
        query = data.get("q")
        print "Finding track %s" % query
        return return_composite_parts(main)


if __name__ == '__main__':
    app.run()
