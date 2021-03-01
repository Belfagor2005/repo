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


import xbmc, xbmcaddon, xbmcplugin
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


thisPlugin = int(sys.argv[1])
addonId = "plugin.video.worldcam"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

Addon = xbmcaddon.Addon(addonId)
__settings__ = xbmcaddon.Addon(addonId)
home = __settings__.getAddonInfo('path')
addonDir = Addon.getAddonInfo('path').decode("utf-8")
print("Here in playlistloader addonDir =", addonDir)
playlistDir = path.join(addonDir, 'Playlists')
fanart = xbmc.translatePath(os.path.join(addonDir, 'fanart.jpg'))
# icon = xbmc.translatePath(os.path.join(addonDir, 'icon.png'))
pixx = xbmc.translatePath(os.path.join(home, 'pic.png'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))


def getUrl(url):
   print("Here in getUrl url =", url)
   req = urllib2.Request(url)
   req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
   response = urllib2.urlopen(req)
   link=response.read()
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
        regexvideo = 'class="ln_css ln-(.*?)" alt="(.*?)"'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'getVideos match =', match
        pic = pixx
        
        items = []           
        
        for url, name in match:
            url1 = 'https://www.skylinewebcams.com/' + url + '.html'

            item = name + "###" + url1
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
        n1 = content.find('div class="dropdown-menu mega-dropdown-menu', start)
        n2 = content.find('div class="collapse navbar-collapse', n1)
        content2 = content[n1:n2]
        pass#print 'content2 =', content2
        ctry = urlmain.replace ("https://www.skylinewebcams.com/", "")
        ctry = ctry.replace (".html", "")
        #https://www.skylinewebcams.com/it/webcam/anguilla.html
#ok        regexvideo = '<a href="/en/webcam(.*?)">(.*?)</a>'
        regexvideo = '<a href="/' + ctry + '/webcam(.*?)">(.*?)</a>'
        match = re.compile(regexvideo, re.DOTALL).findall(content2)
        pass#print 'getVideos3 match =', match
        pic = pixx
        
        items = []        
        
        for url, name in match:
            url1 = 'https://www.skylinewebcams.com/' + ctry + '/webcam' + url
            
            
            item = name + "###" + url1
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
        regexvideo = '><a href="' + stext + '(.*?)".*?alt="(.*?)"'
        pass#print 'getVideos3 regexvideo =', regexvideo
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'getVideos3 match =', match
        
        #https://www.skylinewebcams.com/en/webcam/united-kingdom/england/dover/dover-beach-kent.html
        items = []
        pic = pixx
        items = []
        for url, name in match:
            url1 = 'https://www.skylinewebcams.com/' + stext + url
            pass#print "getVideos4 name =", name
            pass#print "getVideos4 url1 =", url1
            
            item = name + "###" + url1
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url1 = item.split("###")[1]
            
            addDirectoryItem(name, {"name":name, "url":url1, "mode":"4"}, pic)


def getVideos4(name, url):
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
           pass#print "Here in playVideo name =", name
           pass#print "Here in playVideo url =", url
           pic = "DefaultFolder.png"
           li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
           player = xbmc.Player()
           player.play(url, li)
        
std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}
def addDirectoryItem(name, url, mode, iconimage, fanart):

        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
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
      
      
      
xbmcplugin.endOfDirectory(thisPlugin)

