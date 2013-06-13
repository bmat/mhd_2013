import os, web, json
import pyella
import re

import gdata.photos.service
from get_words import get_words

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
    '/', 'search',
    )
app = web.application(urls, globals())

apikey = "905e7eec68193e3f0a81a75591b4a518"

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


class search:
    def GET(self):
        self.lyric = ""
        self.error = None
        data = web.input()
        query = data.get("q")
        print "Finding track %s" % query
        results = pyella.search_tracks(query, "fulltracks").get_next_page()
        if results:
            track = results[0]
            print track.get_mbid(), track.get_title(), track.get_artist_name()
            print track.get_attribute("rhythm_bpm_value")
            links = track.get_links()
            mblink = links[3][1]
            if mblink:
                #Here we have the MusicBrainz ID
                mbid = get_mbi_from_url(mblink)
                self.lyric = get_musixmatch_lyric(mbid)
                print self.lyric
            else:
                print "No MusicBrainz ID found... trying with musixmatch"
                self.lyric = get_musixmatch_lyric_by_query(track.get_title())
        else:
            self.error = "Music not found in ELLA! Please try another song"
        if not self.lyric:
            self.error = "Can't found lyrics for this song. :("
        if self.lyric:
            self.words = get_words(self.lyric)
            self.lyric = re.sub(r"\n", "<br/>", self.lyric)
            self.photos = []
            for key in self.words:
                word = self.words[key][0][0]
                phs = gd_client.SearchCommunityPhotos(word, limit='2')
                self.photos.extend([p.content.src for p in phs.entry])
        main = unicode(render.main(self))
        return return_composite_parts(main)

    def POST(self):
        main = unicode(render.main(self))
        data = web.input()
        query = data.get("q")
        print "Finding track %s" % query
        return return_composite_parts(main)


if __name__ == '__main__':
    app.run()
