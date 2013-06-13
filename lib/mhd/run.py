import os, web, socket, json, pprint, time
import pyella
import re

# render
render = web.template.render( os.path.dirname(__file__) + '/templates/')

# db connect

abspath = os.path.dirname(__file__)
os.chdir(abspath)

urls = (
    '/', 'search',
    )
app = web.application(urls, globals())


def get_musixmatch_lyric(url, apikey):
    import urllib2
    req = urllib2.Request(url, None, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    json_dict = json.loads(response)
    print json_dict
    f.close()
    return json_dict['message']['body']['lyrics']['lyrics_body']

def return_composite_parts(main):
    header = unicode(render.header())
    footer = unicode(render.footer())
    return render.layout(header, main, footer)


class search:
    def GET(self):
        data = web.input()
        query = data.get("q")
        print "Finding track %s" % query
        results = pyella.search_tracks(query, "fulltracks")
        track = results.get_next_page()[0]
        print track.get_mbid(), track.get_title(), track.get_artist_name()
        print track.get_attribute("rhythm_bpm_value")
        #mbid = track.get_attribute("musicbrainz_track_url")#[29:-5]
        links = track.get_links()
        mblink = links[3][1]
        mbid = mblink[29:-5]
        self.lyric = get_musixmatch_lyric("http://api.musixmatch.com/ws/1.1/track.lyrics.get?track_mbid=%s&apikey=905e7eec68193e3f0a81a75591b4a518&format=json" % mbid, None)
        self.lyric = re.sub(r"\r\n", "<br/>", self.lyric)
        print self.lyric
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
