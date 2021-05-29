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

import xbmcplugin, xbmcaddon
import xbmcgui
import time
import re
import six
from sys import version_info

PY3 = version_info[0] == 3
if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import quote, unquote_plus, unquote, urlencode
    from urllib.request import urlretrieve
    from urllib.parse import urlparse
    from html.entities import name2codepoint as n2cp
    import http.client
else:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urllib import quote, unquote_plus, unquote, urlencode
    from urllib import urlretrieve
    from urlparse import urlparse
    from htmlentitydefs import name2codepoint as n2cp
    import httplib
try:
       import urlparse
except:       
       from urllib.parse import urlparse
from os import path, system
import socket
try:
       import urllib2
       from urllib2 import Request, URLError, urlopen
except:
       import urllib.request
try:       
       from urlparse import parse_qs
except:
       from urllib.parse import parse_qs

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

def getUrl(url):
        print( "Here in getUrl url =", url)
        req = Request(url)    
        # try:
               # req = urllib.request.Request(url)
        # except:
               # req = urllib2.Request(url)                  
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
               # try:
                      # response = urllib.request.urlopen(req)
               # except:       
                      # response = urllib2.urlopen(req)
               urlopen(req)       
               link=response.read()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               try:
                      response = urllib.request.urlopen(req)
               except:       
                      response = urllib2.urlopen(req)
               link=response.read()
               response.close()
               return link
                
def getUrl2(url, referer):
#        pass#pass#print "Here in  getUrl2 url =", url
#        pass#pass#print "Here in  getUrl2 referer =", referer
        try:
               req = urllib.request.Request(url)
        except:
               req = urllib2.Request(url)       
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', referer)
        try:
               # try:
                      # response = urllib.request.urlopen(req)
               # except:       
                      # response = urllib2.urlopen(req)
               urlopen(req)        
               link=response.read()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               # try:
                      # response = urllib.request.urlopen(req)
               # except:       
                      # response = urllib2.urlopen(req)
                      
               urlopen(req)       
               link=response.read()
               response.close()
               return link

def getUrl3(url):
#        pass#print"Here in getUrl url =", url
        # try:
               # req = urllib.request.Request(url)
        # except:
               # req = urllib2.Request(url)   
        req = Request(url)        
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.geturl()
        response.close()
        return link

def showContent():
        names = []
        urls = []
        modes = []
        names.append('skylinewebcams.com')
        urls.append('https://www.skylinewebcams.com/')
        modes.append('1')
        names.append('User Lists')
        urls.append('http://worldcam.eu/')
        modes.append('5')
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

            addDirectoryItem(name, {"name":name, "url":url1, "mode":"2"}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)
        
def getVideos2(name1, urlmain):
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
            addDirectoryItem(name, {"name":name, "url":url1, "mode":"3"}, pic)

        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos3(name1, urlmain):
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
            
            addDirectoryItem(name, {"name":name, "url":url1, "mode":"4"}, pic)

def getVideos4(name, url):
        pass#print "Here in getVideos4 url =", url
        content = getUrl(url)
        pass#print 'getVideos4 content =', content
        regexvideo = b'source\:\'(.*?)\''
        pass#print 'getVideos3 regexvideo =', regexvideo
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'getVideos3 match =', match
        url = "https://hd-auth.skylinewebcams.com/" + match[0].decode()
        pass#print "Here in Test url =", url
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
        player = xbmc.Player()
        player.play(url, li)




def getVideos4X(name, url):
        import youtube_dl
        pass#print "Here in getVideos4 url 1=", url
        from youtube_dl import YoutubeDL
        pass#print "Here in getVideos4 url 2", url
        ydl_opts = {'format': 'best'}
        ydl = YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
       # url = "https://www.youtube.com/watch?v=CSYCEyMQWQA"
        result = ydl.extract_info(url, download=False)
        pass#print "result =", result
        url = result["url"]
        pass#print "Here in Test url =", url
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
        player = xbmc.Player()
        player.play(url, li)

def getVideos5(name, url):
                pass#print "In name 1=", name
                pass#print "In url 1=", url
                names = []
                pic = pixx
                for root, dirs, files in os.walk(playlistDir):
                       for name in files:
                              url = "uuu"
                              names.append(name)
                              addDirectoryItem(name, {"name":name, "url":url, "mode":"6"}, pic)
                       xbmcplugin.endOfDirectory(thisPlugin)

def getVideos6(name, url):
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
    
            addDirectoryItem(name, {"name":name, "url":url, "mode":"7"}, pic)
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

def getVideos8(name1, urlmain):
        content = getUrl(urlmain)
        pass#print "content B =", content
        regexvideo = b'<a class="noDec" href="(.*?)".*?alt="(.*?)"'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'match =', match
        pic = " "       
        for url, name in match:
            if not b"https://www.earthcam.com" in url:
                   continue
            url1 = url.decode()
            name1 = name.decode() 
            addDirectoryItem(name1, {"name":name1, "url":url1, "mode":"9"}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)
        
def getVideos9(name, urlmain):
        content = getUrl(urlmain)
        print( "getVideos9 content C =", content)
#        regexvideo = '"livestreamingpath"\:"(.*?)m3u8'
        regexvideo = b'html5_streamingdomain"\:"(.*?)".*?html5_streampath"\:"(.*?)"'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        print( 'getVideos9  match =', match)

        url = match[0][0] + match[0][1]
        url = url.replace(b"\\", b"")
        url = url.replace(b"%2F", b"/")
        url = url.replace(b"%2B", b"+")
        print( "In Webcam7 url =", url)
        playVideo(name, url)
        
def getVideos10(name, urlmain):
        content = getUrl('http://www.livecameras.gr/')
        pass#print 'getVideos10 content A =', content#pass#
        
        # regexvideo = 'item1".*?href="(.*?)".*?data-title="(.*?)".*?<img src=""(.*?)"/>'        
        
        regexvideo = 'a class="item1" href="(.*?)".*?data-title="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pic = " "
        pass#print 'getVideos10 match =', match#pass#
        for url, name in match:
            url1 = 'https:' + url
            addDirectoryItem(name, {"name":name, "url":url1, "mode":"7"}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

        
std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    try:
           url = sys.argv[0] + '?' + urlencode(parameters)
    except:
           url = sys.argv[0] + '?' + urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)
    

def addDirectoryItemXX(name, url, mode, iconimage, fanart):

        u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name) + "&iconimage=" + quote_plus(iconimage)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
        liz.setInfo( type = "Video", infoLabels = { "Title": name } )
        liz.setProperty('fanart_image', fanart)
        if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
                u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
                ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
                return ok
        ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
        return ok

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
        url = unquote(url)
except:
        url = unquote(url)  
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
      ok = playVideo(name, url)
   elif mode == str(8):
      ok = getVideos8(name, url)
   elif mode == str(9):
      ok = getVideos9(name, url)
   elif mode == str(10):
      ok = getVideos10(name, url)
     
xbmcplugin.endOfDirectory(thisPlugin)
