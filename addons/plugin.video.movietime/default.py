#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys, xpath, xbmc, os

if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"): # enigma2 KodiLite
    libs = sys.argv[0].replace("default.py", "resources/lib")
    if os.path.exists(libs):
       sys.path.append(libs)
    print "Here in default-py sys.argv =", sys.argv
    if ("?plugin%3A%2F%2F" in sys.argv[2]) or ("?plugin://" in sys.argv[2]):
        argtwo = sys.argv[2]
        n2 = argtwo.find("?", 0)
        n3 = argtwo.find("?", (n2+2))
        if n3<0:
            sys.argv[0] = argtwo
            sys.argv[2] = ""
        else:
            sys.argv[0] = argtwo[:n3]
            sys.argv[2] = argtwo[n3:]
        sys.argv[0] = sys.argv[0].replace("?", "")
    else:
        sys.argv[0] = sys.argv[0].replace('/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins/', 'plugin://')
        sys.argv[0] = sys.argv[0].replace('default.py', '')
    print "Here in default-py sys.argv B=", sys.argv


import xbmc,xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from os import path, system
import socket
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs
from urllib import unquote_plus

#import universalscrapers
THISPLUG = "/usr/lib/enigma2/python/Plugins/Extensions/Movietime"
thisPlugin = int(sys.argv[1])
addonId = "plugin.video.movietime"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

SOURCES = ["Filmxy", "Mkvhub", "Extramovies", "Coolmoviezone", "Gowatchseries", "Seriesonline"]
HOSTS = ["openload", "vidtodo", "streamango", "bestream", "vidzi", "streamcloud", "estream"]
hostDict  = ['example.com', 'teramixer.com', 'waaw.tv', 'hqq.watch', 'netu.tv', 'hqq.tv', 'flixtor.to', 'videoraj.ec', 'videoraj.eu', 'videoraj.sx', 'videoraj.ch', 'videoraj.com', 'videoraj.to', 'videoraj.co', 'videowood.tv', 'movdivx.com', 'divxme.com', 'streamflv.com', 'cloudy.ec', 'cloudy.eu', 'cloudy.sx', 'cloudy.ch', 'cloudy.com', 'openload.io', 'openload.co', 'oload.tv', 'oload.stream', 'amazon.com', 'everplay.watchpass.net', 'filepup.net', 'daclips.in', 'daclips.com', 'vimeo.com', 'toltsd-fel.tk', 'toltsd-fel.xyz', 'thevideobee.to', 'thevideo.me', 'tvad.me', 'uptobox.com', 'uptostream.com', 'nosvideo.com', 'noslocker.com', 'lolzor.com', 'mycollection.net', 'adhqmedia.com', 'gagomatic.com', 'funblr.com', 'favour.me', 'vidbaba.com', 'likeafool.com', 'googlevideo.com', 'googleusercontent.com', 'get.google.com', 'plus.google.com', 'googledrive.com', 'drive.google.com', 'docs.google.com', 'youtube.googleapis.com', 'movshare.net', 'wholecloud.net', 'vidgg.to', 'cloud.mail.ru', 'kingvid.tv', 'vidup.me', 'watchers.to', 'datemule.co', 'datemule.com', 'grifthost.com', 'vivo.sx', 'tvlogy.to', 'anyfiles.pl', 'streamable.com', 'rutube.ru', 'indavideo.hu', 'gorillavid.in', 'gorillavid.com', 'fastplay.sx', 'fastplay.cc', 'fastplay.to', 'vidics.tv', 'stream.moe', 'videoget.me', 'dailymotion.com', 'bitvid.sx', 'videoweed.es', 'videoweed.com', 'watchonline.to', 'novamov.com', 'auroravid.to', 'vidzella.me', 'dl.vidzella.me', 'facebook.com', 'byzoo.org', 'playpanda.net', 'videozoo.me', 'videowing.me', 'easyvideo.me', 'play44.net', 'playbb.me', 'video44.net', 'upload.af', 'upload.mn', 'adultswim.com', 'streamplay.to', 'streamplay.club', 'fileweed.net', 'mersalaayitten.com', 'mersalaayitten.co', 'mersalaayitten.us', 'ok.ru', 'odnoklassniki.ru', 'speedvid.net', 'videohut.to', 'uploadx.link', 'uploadx.org', 'uploadz.org', 'uploadz.co', 'clicknupload.com', 'clicknupload.me', 'clicknupload.link', 'clicknupload.org', 'mp4stream.com', 'tune.pk', 'tune.video', 'vk.com', 'trollvid.net', 'trollvid.io', 'mp4edge.com', 'mail.ru', 'my.mail.ru', 'm.my.mail.ru', 'videoapi.my.mail.ru', 'api.video.mail.ru', 'vidmad.net', 'tamildrive.com', 'oneload.co', 'oneload.com', 'apnasave.club', 'videa.hu', 'videakid.hu', 'vidlox.tv', 'powvideo.net', 'streamin.to', 'flashx.tv', 'flashx.to', 'streamcloud.eu', 'vid.me', 'veoh.com', 'vidstore.me', 'videohost2.com', 'trt.pl', 'vidzi.tv', 'cda.pl', 'www.cda.pl', 'ebd.cda.pl', 'videos.sapo.pt', 'myvi.ru', 'thevid.net', 'yourupload.com', 'yucache.net', 'vodlock.co', 'anime-portal.org', 'goflicker.com', 'movpod.net', 'movpod.in', 'embed8.ocloud.stream', 'ocloud.stream', 'earnvideos.com', 'ecostream.tv', 'mehlizmovies.com', 'vidtodo.com', 'gamovideo.com', 'tubitv.com', 'hugefiles.net', 'hdvid.tv', 'ustream.tv', 'xvidstage.com', 'faststream.ws', 'kingfiles.net', 'tudou.com', 'vshare.eu', 'playwire.com', 'streamango.com', 'streamcherry.com', 'castamp.com', 'promptfile.com', 'syfy.com', 'vidabc.com', 'blazefile.co', 'usersfiles.com', 'mystream.la', 'stagevu.com', 'playhd.video', 'playhd.fo', 'aliez.me', 'vidbom.com', 'speedvideo.net', 'playedto.me', 'myvidstream.net', 'speedplay.xyz', 'speedplay.us', 'speedplay1.site', 'speedplay.pw', 'speedplay1.pw', 'speedplay3.pw', 'speedplayy.site', 'streame.net', 'thevideos.tv', 'weshare.me', 'nowvideo.eu', 'nowvideo.ch', 'nowvideo.sx', 'nowvideo.co', 'nowvideo.li', 'nowvideo.fo', 'nowvideo.at', 'nowvideo.ec', 'divxstage.eu', 'divxstage.net', 'divxstage.to', 'cloudtime.to', 'mycloud.to', 'mcloud.to', 'watchvideo.us', 'watchvideo2.us', 'watchvideo3.us', 'watchvideo4.us', 'watchvideo5.us', 'watchvideo6.us', 'watchvideo7.us', 'watchvideo8.us', 'watchvideo9.us', 'watchvideo10.us', 'watchvideo11.us', 'watchvideo12.us', 'watchvideo13.us', 'watchvideo14.us', 'watchvideo15.us', 'watchvideo16.us', 'watchvideo17.us', 'watchvideo18.us', 'watchvideo19.us', 'watchvideo20.us', 'watchvideo21.us', 'bestream.tv', 'vidwatch3.me', 'vidwatch.me', 'vidfile.net', 'jetload.tv', 'vidhos.com', 'rapidvideo.ws', 'putload.tv', 'shitmovie.com', 'filez.tv', 'tusfiles.net', 'dbmovies.xyz', 'ani-stream.com', 'mp4engine.com', 'megamp4.net', 'megamp4.us', 'h265.se', 'vidstreaming.io', 'vidup.org', 'mp4upload.com', 'spruto.tv', '9xplay.net', 'estream.to', 'vshare.io', 'vidto.me', 'speedwatch.us', 'downace.com', 'vidcrazy.net', 'uploadcrazy.net', 'rapidvideo.com', 'raptu.com', 'goodvideohost.com', 'vidoza.net', 'entervideo.net', 'videocloud.co', 'zstream.to', 'userscloud.com', 'clipwatching.com']
hostprDict  = ['1fichier.com', 'oboom.com', 'rapidgator.net', 'rg.to', 'uploaded.net', 'uploaded.to', 'ul.to', 'filefactory.com', 'nitroflare.com', 'turbobit.net', 'uploadrocket.net']



std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}

def getUrl(url):
    print "Here in getUrl url =", url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def showContent44():
                names = []
                urls = []
                modes = []
                names.append("Most Popular Movies by Year")
                names.append("Most Popular Movies by Genre")
                names.append("Most Popular Movies by Page")
                names.append("Most Popular TV shows")
                urls.append("https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&year=2020,2020&sort=moviemeter,asc&count=40&start=1")
                urls.append("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr_3")
                urls.append("http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=en&sort=moviemeter,asc&count=40&start=1&page=2&ref_=adv_nxt")
                urls.append("http://www.imdb.com/chart/tvmeter?ref_=nv_tvv_mptv_4")
                modes.append("81")
                modes.append("82")
                modes.append("83")
                modes.append("84")
                i = 0
                pic = " "
                for name in names:
                        url = urls[i]
                        mode = modes[i]
                        i = i+1
                        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)


def Movies1(name1, url):
            names = []
            urls = []
            iy = 2021
            ny = 0
            while ny < 10:
                  iy = iy-1
                  url = "https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&year=" + str(iy) + "," + str(iy) + "&sort=moviemeter,asc&count=40&start=1"
                  name = str(iy)
                  ny = ny+1
                  addDirectoryItem(name, {"name":name, "url":url, "mode":85}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)

def Movies2(name1, url):
            names = []
            urls = []
            content = getUrl(url)
            print "In Movies2 content =", content
            regexvideo = 'div class="table-cell primary".*?a href="(.*?)" >(.*?)<'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print "In Videos2 match =", match
            for url, name in match:
                  url = "http://www.imdb.com" + url
                  addDirectoryItem(name, {"name":name, "url":url, "mode":85}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)

def Movies3(name1, url):
            names = []
            urls = []
            np = 1
            while np < 6:
                  ns = np + (np-1)*40
#                  url = "https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&primary_language=en&production_status=released&count=40&start=" + str(ns) + "&ref_=adv_nxt"
                  url = "http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=en&sort=moviemeter,asc&count=40&start=1"
                  name = "Page-" + str(np)
                  np = np+1
                  addDirectoryItem(name, {"name":name, "url":url, "mode":85}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)


def getVideos2(name1, url):
        content = getUrl(url)
        print "content 1 =", content
        regexvideo = 'lister-item mode-advanced.*?<a href="(.*?)".*?img alt="(.*?)".*?loadlate="(.*?)".*?data-tconst="(.*?)".*?lister-item-year text-muted unbold">(.*?)<'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        print "In getVideos9 match =", match
        for url, name, pic, imdb, year in match:
                  poster = pic
                  print "Here in movies.py poster = ", poster
                  if '/nopicture/' in poster: poster = '0'
                  poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                  print "Here in movies.py poster 2= ", poster
#                  poster = client.replaceHTMLCodes(poster)
#                  print "Here in movies.py poster 3= ", poster
                  poster = poster.encode('utf-8')
                  print "Here in movies.py poster 4= ", poster
                  pic = poster
                  url1 = "https://www.imdb.com" + url
                  year = year.replace("(I)", "")
                  year = year.replace("(", "")
                  year = year.replace(")", "")
                  year = year.replace(" ", "")
                  name1 = name.replace(" ", "+")
                  url = name1 + "___" + year + "___" + imdb + "___"
                  name2 = name + "(" + year + ")"
                  addDirectoryItem(name2, {"name":name2, "url":url, "mode":86}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)


def getVideos3(name1, url):
#            sources = ["Putlocker", "Movie4uch", "Solarmovie", "Seriesonline", "Watchfree"]

            for name in SOURCES:
                  pic = " "
                  addDirectoryItem(name, {"name":name, "url":url, "mode":87}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)



#import resources
def findUrl(s, imdb, title, localtitle, aliases, year):
             url = s.movie(imdb, title, localtitle, aliases, year)
             print "Here in findUrl url =", url
             return url

def getVideos4(name1, url):
            print "Here in getVideos3 name1 =", name1
            print "Here in getVideos3 url =", url
            items = url.split("___")
            title = items[0]
            year = items[1]
            imdb = items[2]
#Here in getVideos3 year = %282017%29
#Here in getVideos3 title = Baby%24Driver
            year = year.replace("%28", "")
            year = year.replace("%29", "")
            title = title.replace("+", " ")
            print "Here in getVideos3 year =", year
            print "Here in getVideos3 title =", title
            print "Here in getVideos3 imdb =", imdb
            localtitle = title
            aliases= []
            #"Filmxy", "Mkhub", "Extramovies", "Coolmoviezone", "Gowatchseries", "Seriesonline"
            if "Filmxy" in name1:
                       from exoscrapers.sources_exoscrapers.en.filmxy import source
                       s = source()
                       sources = s.sources(findUrl(s, imdb, title, localtitle, aliases, year), hostDict, hostprDict)
                       print "Here in getVideos3 sources =", sources
            #watch32
            elif "Mkvhub" in name1:
                       from exoscrapers.sources_exoscrapers.en.mkvhub import source
                       s = source()
                       sources = s.sources(findUrl(s, imdb, title, localtitle, aliases, year), hostDict, hostprDict)
                       print "Here in getVideos3 sources =", sources

            elif "Extramovies" in name1:
                       from exoscrapers.sources_exoscrapers.en.extramovies import source
                       s = source()
                       sources = s.sources(findUrl(s, imdb, title, localtitle, aliases, year), hostDict, hostprDict)
                       print "Here in getVideos3 sources =", sources            #watchfrees

            elif "Coolmoviezone" in name1:
                       from exoscrapers.sources_exoscrapers.en.coolmoviezone import source
                       s = source() # def movie(self, imdb, title, localtitle, aliases, year):
                       sources = s.sources(findUrl(s, imdb, title, localtitle, aliases, year), hostDict, hostprDict)
                       print "Here in getVideos3 sources =", sources            #watchfrees
            #watchstream
            elif "Gowatchseries" in name1:
                       from exoscrapers.sources_exoscrapers.en.gowatchseries import source
                       s = source()
                       sources = s.sources(findUrl(s, imdb, title, localtitle, aliases, year), hostDict, hostprDict)
                       print "Here in getVideos3 sources =", sources

            elif "Seriesonline" in name1:
                       from exoscrapers.sources_exoscrapers.en.seriesonline import source
                       s = source()
                       sources = s.sources(findUrl(s, imdb, title, localtitle, aliases, year), hostDict, hostprDict)
                       print "Here in getVideos3 sources =", sources

            for source in sources:
                         url = source['url']
##                         url = s.resolve(url1)
                         print "Here in getVideos3 url 3=", url
                         name = title + "_" + source['source']
#                         if (not "googlelink" in name.lower()) and (not "dl" in name.lower()) and (not "cdn" in name.lower()) and(not "openload" in name.lower()) and (not "vidtodo" in name.lower()) and (not "streamango" in name.lower()) and (not "bestream" in name.lower()) and (not "vidzi" in name.lower()) and (not "streamcloud" in name.lower()):
#                                continue
                         quality = source['quality']
                         name2 = name + "_" + quality
                         pic = " "
                         addDirectoryItem(name2, {"name":name2, "url":url, "mode":88}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)


def playVideoThumb(name, url):
           print "Here in playVideoThumb url =", url
           if ("vidcloud" in name.lower()) or ("googlelink" in name.lower()) or ("dl" in name.lower()) or ("cdn" in name.lower()) or ("gvideo" in name.lower()):
                    url = url
           else:
                    import urlresolver
                    url = urlresolver.HostedMediaFile(url=url).resolve()
           pic = "DefaultFolder.png"
           print "Here in playVideoThumb url B=", url
           li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
           player = xbmc.Player()
           player.play(url, li)


def Videos5(name1, url):
            names = []
            urls = []
            pics = []

            content = getUrl(url)
            print "In TV1 content =", content

            regexvideo = '<td class="posterColumn.*?a href="(.*?)".*?title=".*?>(.*?)<.*?secondaryInfo">(.*?)<'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print "In TV1 match =", match
            for url, name, year in match:
                  pic = " "
                  url = "http://www.imdb.com" + url
#                  name = name + year
                  print "In TV1 name =", name
                  print "In TV1 url =", url
                  addDirectoryItem(name, {"name":name, "url":url, "mode":9}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)

def Videos6(name1, url):
            names = []
            urls = []
            pics = []
            content = getUrl(url)
            print "In Videos6 content =", content
            n1 = content.find('div class="seasons-and-year-nav', 0)
            n2 = content.find('br class="clear', n1)
            n3 = content.find('</div>', n2)
            content = content[n2:n3]
            print "In Videos6 n1, n2, n3, content 2 =", n1, n2, n3, content
            regexvideo = '<a href="(.*?)season=(.*?)&(.*?)"'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print "In Videos6 match =", match
            for url1, name, url2 in match:
                  pic = " "
                  url = "http://www.imdb.com" + url1 + "season=" + name + "&" + url2
                  name = name1 + "__" + "Season " + name
                  print "In TV2 name =", name
                  print "In TV2 url =", url
                  addDirectoryItem(name, {"name":name, "url":url, "mode":10}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)

def gettvdb(imdb):
                imurl = "http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=" + str(imdb)
                fpage = getUrl(imurl)
                print "In Videos9 fpage =", fpage
                n1 = fpage.find("<seriesid", 0)
                n2 = fpage.find(">", n1)
                n3 = fpage.find("<", n2)
                tvdb = fpage[(n2+1):n3]
                print "In gettvdb tvdb =", tvdb
                return tvdb

def Videos7(name1, url):
            names = []
            imdbs = []
            urls = []
            pics = []
            epids = []
            airds = []
            content = getUrl(url)
            print "In Videos7 content =", content
            n1 = content.find("imdb:///title/", 0)
            n2 = content.find("/", (n1+10))
            n3 = content.find("?", n2)
            imdb = content[(n2+1):n3]
            print "In Videos7 imdb =", imdb
            tvdb = gettvdb(imdb)
            print "In Videos7 tvdb =", tvdb
#            regexvideo = 'datePublished".*?"(*?)".?"div class="titleParentWrapper.*?a href="/title/(.*?)\?.*?title="(.*?)".*?parentDate">\((.*?)-.*?data-title="(.*?)"'
            regexvideo = '<div class="image".*?<a href="(.*?)".*?itle="(.*?)".*? data-const="(.*?)".*?<div>(.*?)<.*?<div class="airdate">(.*?)<'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print "In Videos7 match =", match
            for url, name, imdb, epid, aird in match:
                  pic = " "
                  items = epid.split(",")
#                  name = name1 + "-" + name
                  url = url + "__" + name1 + "__" + imdb + "__" + epid + "__" + aird
                  print "In TV3 name =", name
                  print "In TV3 url =", url
                  addDirectoryItem(name, {"name":name, "url":url, "mode":11}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)


def Videos8(name1, url):
#            sources = ["Putlocker", "Movie4uch", "Solarmovie", "Seriesonline", "Watchfree"]
            items = name1.split("__")
            name1 = items[0]
            for name in SOURCES:
                  pic = " "
                  name = name1 + "-" + name
                  print "In TV4 name =", name
                  print "In TV4 url =", url
                  addDirectoryItem(name, {"name":name, "url":url, "mode":12}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)

def TV5(name, url):
            names = []
            imdbs = []
            urls = []
            pics = []
            epids = []
            airds = []
            content = getUrl(url)
            print "In tv5 content =", content
            n1 = content.find("imdb:///title/", 0)
            n2 = content.find("/", (n1+10))
            n3 = content.find("?", n2)
            imdb = content[(n2+1):n3]
            print "In tv5 imdb =", imdb
            regexvideo = '<div class="image".*?<a href="(.*?)".*?itle="(.*?)".*? data-const="(.*?)".*?<div>(.*?)<.*?<div class="airdate">(.*?)<'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print "In tv5 match =", match
            for url, name, imdb, epid, aird in match:
                  pic = " "
                  items = epid.split(",")
                  name = items[0] + "-" + items[1] + "-" + name
                  url = url + "__" + imdb + "__" + epid + "__" + aird
                  addDirectoryItem(name, {"name":name, "url":url, "mode":12}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)


def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
name =  str(params.get("name", ""))
url =  str(params.get("url", ""))
url = urllib.unquote(url)
mode =  str(params.get("mode", ""))
pic =  str(params.get("pic", ""))

if not sys.argv[2]:
    ok = showContent44()
else:
    if mode == str(81):
        ok = Movies1(name, url)
#       ok = getVideos1(name, url)
    elif mode == str(85):
        ok = getVideos2(name, url)
    elif mode == str(86):
        ok = getVideos3(name, url)
    elif mode == str(87):
        ok = getVideos4(name, url)
    elif mode == str(88):
        ok = playVideoThumb(name, url)
    elif mode == str(82):
        ok = Movies2(name, url)
    elif mode == str(83):
        ok = Movies3(name, url)
    elif mode == str(84):
        ok = Videos5(name, url)
    elif mode == str(9):
        ok = Videos6(name, url)
    elif mode == str(10):
        ok = Videos7(name, url)
    elif mode == str(11):
        ok = Videos8(name, url)
    elif mode == str(12):
        ok = TV5(name, url)

