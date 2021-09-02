#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys, xpath, xbmc, os

if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"): # enigma2 KodiLite
    libs = sys.argv[0].replace("default.py", "resources/lib")
    if os.path.exists(libs):
       sys.path.append(libs)
    print("Here in default-py sys.argv =", sys.argv)
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
    print("Here in default-py sys.argv B=", sys.argv)


import xbmc,xbmcplugin,xbmcaddon
import xbmcgui
import six
# import vlc

PY3 = False

try:

     import sys
     import urllib
     import time
     import re
     import http.client
     from urllib.parse import urlparse
     from os import path, system
     import socket
     import urllib.request
     from urllib.parse import parse_qs
     PY3 = True; unicode = str; unichr = chr; long = int

except:
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


thisPlugin = int(sys.argv[1])
addonId = "plugin.video.worldcam"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

Addon = xbmcaddon.Addon(addonId)
__settings__ = xbmcaddon.Addon(addonId)
home = __settings__.getAddonInfo('path')
#addonDir = Addon.getAddonInfo('path').decode("utf-8")
addonDir = Addon.getAddonInfo('path')
print("Here in playlistloader addonDir =", addonDir)
playlistDir = path.join(addonDir, 'Playlists')
fanart = xbmc.translatePath(os.path.join(addonDir, 'fanart.jpg'))
# icon = xbmc.translatePath(os.path.join(addonDir, 'icon.png'))
pixx = xbmc.translatePath(os.path.join(home, 'pic.png'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

if PY3:
    def getUrl(url):
#        print(  "Here in getUrl url =", url)
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
               response = urllib.request.urlopen(req)
               link=response.read()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urllib.request.urlopen(req, context=gcontext)
               link=response.read()
               response.close()
               return link

    def getUrl2(url, referer):
#        print  "Here in  getUrl2 url =", url
#        print  "Here in  getUrl2 referer =", referer
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', referer)
        try:
               response = urllib.request.urlopen(req)
               link=response.read()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urllib.request.urlopen(req, context=gcontext)
               link=response.read()
               response.close()
               return link


    def getUrl3(url):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
               response = urllib.request.urlopen(req)
               link=response.geturl()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urllib.request.urlopen(req, context=gcontext)
               link=response.geturl()
               response.close()
               return link

else:
    def getUrl(url):
        pass#print "Here in getUrl url =", url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
               response = urllib2.urlopen(req)
               pass#print "Here in getUrl response =", response
               link=response.read()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urllib2.urlopen(req, context=gcontext)
               pass#print "Here in getUrl response 2=", response
               link=response.read()
               response.close()
               return link

    def getUrl2(url, referer):
        pass#print "Here in  getUrl2 url =", url
        pass#print "Here in  getUrl2 referer =", referer
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', referer)
        try:
               response = urllib2.urlopen(req)
               link=response.read()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urllib2.urlopen(req, context=gcontext)
               link=response.read()
               response.close()
               return link

    def getUrl3(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
               response = urllib2.urlopen(req)
               link=response.geturl()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urllib2.urlopen(req, context=gcontext)
               link=response.geturl()
               response.close()
               return link

def showContent():
        names = []
        urls = []
        modes = []
        names.append('skylinewebcams.com')
        urls.append('https://www.skylinewebcams.com/')
        modes.append('5')
        names.append('User Lists')
        urls.append('http://worldcam.eu/')
        modes.append('9')
        """
        names.append('earthcam.com')
        urls.append('https://www.earthcam.com')
        modes.append('8')
        names.append('livecameras.gr')
        urls.append('http://www.livecameras.gr/')
        modes.append('10')
        """
        i = 0
        pic = pixx
        for name in names:
            url = urls[i]
            mode = modes[i]
            i = i+1
            addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

#class="ln_css ln-de" alt="Deutsch"
def getVideos(name1, urlmain):
#        content = getUrl('https://www.skylinewebcams.com/en.html')
        content = getUrl(urlmain)
#        print( 'getVideos content =', content)
        n1 = content.find(b'span class="nav-header ">Countries<', 0)
        n2 = content.find(b'>All Cameras<', n1)
        content2 = content[n1:n2]
#        print( 'getVideos content2 =', content2)

        regexvideo = b'<a href=(.*?)>(.*?)<'
        match = re.compile(regexvideo, re.DOTALL).findall(content2)
        pass#print 'getVideos match =', match
        pic = " "

        items = []
        #https://www.webcamtaxi.com/en/andorra.html
        for url, name in match:
            url1 = b'https://www.webcamtaxi.com' + url
            url1 = url1.decode()
            name = name.decode()
            addDirectoryItem(name, {"name":name, "url":url1, "mode":"2"}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos2(name1, urlmain):

        content = getUrl(urlmain)
        print( 'getVideos2 content =', content)
        start = 0

        regexvideo = b'href=/en/' + name1.lower().encode("UTF-8") + b'/(.*?)html.*?self>(.*?)<'

        match = re.compile(regexvideo, re.DOTALL).findall(content)
        print( 'getVideos2 match =', match)
        pic = " "

        items = []

        for url, name in match:
            if b"/" in url:
                  continue
            if name in items:
                  continue
            items.append(name)

            url1 = 'https://www.webcamtaxi.com/en/' + name1.lower() +'/' + url.decode() + 'html'
#            url1 = url1.decode()
            name = name.decode()
            addDirectoryItem(name, {"name":name, "url":url1, "mode":"3"}, pic)

        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos3(name1, urlmain):
        pass#print 'getVideos3 urlmain =', urlmain
        content = getUrl(urlmain)
        print( 'getVideos3 content =', content)
        name = name1.lower()
        regexvideo = b'<div class="nspArt nspCol3".*?a href=(.*?).html'
#ok        regexvideo = 'en/webcam/united-kingdom/(.*?)".*?alt="(.*?)"'
#        regexvideo = "'" + stext + "(.*?)\".*?alt=\"(.*?)\"'"
        pass#print 'getVideos2 stext =', stext
#ok        regexvideo = stext + '(.*?)".*?alt="(.*?)"'
#        regexvideo = b'><a href="' + stext.encode("UTF-8") + b'(.*?)".*?alt="(.*?)"'
        print( 'getVideos3 regexvideo =', regexvideo)
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        print( 'getVideos3 match =', match)

        #https://www.webcamtaxi.com/en/spain/alava-province.html
        items = []
        pic = pixx
        items = []
        for url in match:
            url1 = 'https://www.webcamtaxi.com' + url.decode() + '.html'
            n1 = url.rfind(b"/")
            name = url[n1:].decode()
            print( "getVideos3 name 2 =", name)
            pass#print "getVideos4 url1 =", url1

            addDirectoryItem(name, {"name":name, "url":url1, "mode":"4"}, pic)

def getVideos4(name, url):
        print( "Here in getVideos4 url =", url)
        content = getUrl3(url)
        print( 'getVideos4 content =', content)
        regexvideo = b'<iframe src=(.*?) '
        pass#print 'getVideos3 regexvideo =', regexvideo
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        print( 'getVideos4 match =', match)
#        url = match[0].decode()
        url = match[0]
        url = url.replace(b'"', b'')
        print( 'getVideos4 url 2 =', url)
        if b"youtube" in url.lower():
               url = url.decode()
               print( 'getVideos4 url 3 =', url)
               content2 = getUrl(url)
               print( 'getVideos4 content2 =', content2)
               regexvideo = b'\?v(.*?)"'
               match2 = re.compile(regexvideo, re.DOTALL).findall(content2)
               print( 'getVideos4 match2 =', match2)
               s = match2[0]
               s = s.replace(b"\\", b"")
               s = s.replace(b"u003d", b"")
               print( 'getVideos4 s =', s)
               url2 = 'http://www.youtube.com/watch?v=' + s.decode()
               url2 = "http://127.0.0.1:8088/" + url2
               playVideo(name, url2)
        else:
               n1 = url.find(b"src", 0)
               url1 = url[(n1+4):]
               url1 = url1.decode()
               print( "getVideos4 url1 =", url1)
               playVideo(name, url1)

def getVideos5(name, url):
#        content = getUrl('https://www.skylinewebcams.com/en.html')
        content = getUrl(url)
        pass#print 'getVideos content =', content
        regexvideo = b'class="ln_css ln-(.*?)" alt="(.*?)"'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'getVideos match =', match
        pic = pixx

        items = []

        for url, name in match:
            url1 = b'https://www.skylinewebcams.com/' + url + b'.html'
            url1 = url1.decode()
            item = name.decode() + "###" + url1
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url1 = item.split("###")[1]

            addDirectoryItem(name, {"name":name, "url":url1, "mode":"6"}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos6(name1, urlmain):
#        content = getUrl('https://www.skylinewebcams.com/en.html')
        content = getUrl(urlmain)
        start = 0
        n1 = content.find(b'div class="dropdown-menu mega-dropdown-menu', start)
        n2 = content.find(b'div class="collapse navbar-collapse', n1)
        content2 = content[n1:n2]
        pass#print 'content2 =', content2
        ctry = urlmain.replace ("https://www.skylinewebcams.com/", "")
        ctry = ctry.replace (".html", "")
        #https://www.skylinewebcams.com/it/webcam/anguilla.html
#ok        regexvideo = '<a href="/en/webcam(.*?)">(.*?)</a>'
        regexvideo = b'<a href="/' + ctry.encode("UTF-8") + b'/webcam(.*?)">(.*?)</a>'
        match = re.compile(regexvideo, re.DOTALL).findall(content2)
        pass#print 'getVideos3 match =', match
        pic = pixx
        items = []
        for url, name in match:
            url1 = 'https://www.skylinewebcams.com/' + ctry + '/webcam' + url.decode()
            item = name.decode() + "###" + url1
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url1 = item.split("###")[1]
            addDirectoryItem(name, {"name":name, "url":url1, "mode":"7"}, pic)

        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos7(name1, urlmain):
        pass#print 'getVideos3 urlmain =', urlmain
        content = getUrl(urlmain)
        pass#print 'getVideos3 content =', content

        stext = urlmain.replace("https://www.skylinewebcams.com/", "")
        stext = stext.replace(".html", "")
        stext = stext + "/"
#ok        regexvideo = 'en/webcam/united-kingdom/(.*?)".*?alt="(.*?)"'
#        regexvideo = "'" + stext + "(.*?)\".*?alt=\"(.*?)\"'"
        pass#print 'getVideos2 stext =', stext
#ok        regexvideo = stext + '(.*?)".*?alt="(.*?)"'
        regexvideo = b'><a href="' + stext.encode("UTF-8") + b'(.*?)".*?alt="(.*?)"'
        pass#print 'getVideos3 regexvideo =', regexvideo
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'getVideos3 match =', match

        #https://www.skylinewebcams.com/en/webcam/united-kingdom/england/dover/dover-beach-kent.html
        items = []
        pic = pixx
        items = []
        for url, name in match:
            url1 = 'https://www.skylinewebcams.com/' + stext + url.decode()
            pass#print "getVideos4 name =", name
            pass#print "getVideos4 url1 =", url1

            item = name.decode() + "###" + url1
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url1 = item.split("###")[1]
            # url1 = "http://127.0.0.1:8088/" + item.split("###")[1]
            # addDirectoryItem(name, {"name":name, "url":url1, "mode":"11"}, pic)
            addDirectoryItem(name, {"name":name, "url":url1, "mode":"77"}, pic)


def getVid77(name, url):
    content = getUrl(url)
    if PY3:
        content = six.ensure_str(content)
    print('content ============================ ', content)
    regexvideo = "source:'livee.m3u8(.*?)'"
    match = re.compile(regexvideo, re.DOTALL).findall(content)
    print('id: ', match)
    id = match[0]
    id = id.replace('?a=','')
    url = "https://hd-auth.skylinewebcams.com/live.m3u8?a=" + id
    pic = pixx
    print( "Here in plugin.py getVid play with streamlink url =", url)
    url = url.replace(":", "%3a")
    url = url.replace("\\", "/")
    # ref = "http://127.0.0.1:8088/" + url
    ref = url
    desc = ' '
    # self.session.open(Playstream2, name, ref, desc)
    addDirectoryItem(name, {"name":name, "url":ref, "mode":"11"}, pic)

def getVideos9X(name, url):
                       print( "Here in plugin.py getVid play with streamlink url =", url)
                       url = url.replace(":", "%3a")
                       url = url.replace("\\", "/")
                       pass#pass#print "url final= ", url
                       ref = "http://127.0.0.1:8088/" + url
                       pass#pass#print "ref= ", ref
                       desc = ' '
                       self.session.open(Playstream2, name, ref, desc)
                       self.close()


def getVideos9(name, url):
                pass#print "In name 1=", name
                pass#print "In url 1=", url
                names = []
                pic = " "
                for root, dirs, files in os.walk(playlistDir):
                       for name in files:
                              print( "Playlist name =", name)
                              addDirectoryItem(name, {"name":name, "url":url, "mode":"10"}, pic)
                       xbmcplugin.endOfDirectory(thisPlugin)

def getVideos10(name, url):
        print( "getVideos10 name =", name)
        file1 = playlistDir + '/' + name
        names = []
        urls = []
        f1 = open(file1, 'r')

        pic = " "
        for line in f1.readlines():
            if '###' not in line:
                continue
            line = line.replace('\n', '')
            items = line.split('###')
            name = items[0]
            url = items[1]

            addDirectoryItem(name, {"name":name, "url":url, "mode":"11"}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)




def playVideo(name, url):
#           url = "https://videos3.earthcam.com/fecnetwork/AbbeyRoadHD1.flv/chunklist_w1096421812.m3u8"
#           url = "https://videos-3.earthcam.com/fecnetwork/16823.flv/playlist.m3u8"
           pass#print "Here in playVideo name =", name
           pass#print "Here in playVideo url =", url
           pic = "DefaultFolder.png"
           url = url
           li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
           player = xbmc.Player()
           player.play(url, li)


std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    try:
           url = sys.argv[0] + '?' + urllib.parse.urlencode(parameters)
    except:
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
try:
        url = urllib.parse.unquote(url)
except:
        url = urllib.unquote(url)
mode =  str(params.get("mode", ""))
iconimage = None
# def get_params():
	# param = []
	# paramstring = sys.argv[2]
	# if len(paramstring)>= 2:
		# params = sys.argv[2]
		# cleanedparams = params.replace('?', '')
		# if (params[len(params)-1] == '/'):
			# params = params[0:len(params)-2]
		# pairsofparams = cleanedparams.split('&')
		# param = {}
		# for i in range(len(pairsofparams)):
			# splitparams = {}
			# splitparams = pairsofparams[i].split('=')
			# if (len(splitparams)) == 2:
				# param[splitparams[0]] = splitparams[1]
	# return param
# params = get_params()
# url = None
# name = None
# mode = None
# iconimage = None

if not sys.argv[2]:
	ok = showContent()
else:
   if mode == str(1):
      ok = getVideos(name, url)
   elif mode == str(2):
      ok = getVideos2(name, url)
   elif mode == str(3):
      ok = getVideos3(name, url)
   elif mode == str(4):
      ok = getVideos4(name, url)
   elif mode == str(5):
      ok = getVideos5(name, url)
   elif mode == str(6):
      ok = getVideos6(name, url)
   elif mode == str(7):
      ok = getVideos7(name, url)
   elif mode == str(8):
      ok = getVideos8(name, url)
   elif mode == str(9):
      ok = getVideos9(name, url)
   elif mode == str(10):
      ok = getVideos10(name, url)
   elif mode == str(77):
      ok = getVid77(name, url)
   elif mode == str(11):
      ok = playVideo(name, url)

xbmcplugin.endOfDirectory(thisPlugin)





























































































































