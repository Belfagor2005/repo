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
pass#print "Here in playlistloader addonDir =", addonDir
playlistDir = path.join(addonDir, 'Playlists')
fanart = xbmc.translatePath(os.path.join(addonDir, 'fanart.jpg'))
# icon = xbmc.translatePath(os.path.join(addonDir, 'icon.png'))
pixx = xbmc.translatePath(os.path.join(home, 'pic.png'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))


def getUrl(url):
   pass#print "Here in getUrl url =", url
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
        names.append('User Lists')
        urls.append('http://worldcam.eu/')
        modes.append('1')
        names.append('skylinewebcams.com')
        urls.append('https://www.skylinewebcams.com/en.html')
        modes.append('2')
        names.append('earthcam.com')
        urls.append('https://www.earthcam.com')
        modes.append('3')
        names.append('livecameras.gr')
        urls.append('http://www.livecameras.gr/')
        modes.append('9')
        i = 0
        pic = pixx
        for name in names:
                        url = urls[i]
                        mode = modes[i]
                        i = i+1
                        # addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
                        addDirectoryItem(name, url,mode, pic, fanart)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name, url):
                pass#print "In name 1=", name
                pass#print "In url 1=", url
                pic = pixx
                names = []
                for root, dirs, files in os.walk(playlistDir):
                       for name in files:
                              url = "uuu"
            
                              names.append(name)
                              # addDirectoryItem(name, {"name":name, "url":url, "mode":"4"}, pic)
                              addDirectoryItem(name, url,4, pic, fanart)
                       xbmcplugin.endOfDirectory(thisPlugin)


def getVideos2(name, url):
        file1 = playlistDir + '/' + name
        names = []
        urls = []
        f1 = open(file1, 'r')
        
        pic = pixx        
        for line in f1.readlines():
            if '###' not in line:
                continue
            line = line.replace('\n', '')
            items = line.split('###')
            name = items[0]
            url = items[1]
    
            # addDirectoryItem(name, {"name":name, "url":url, "mode":"5"}, pic)
            addDirectoryItem(name, url,5, pic, fanart)
        xbmcplugin.endOfDirectory(thisPlugin)


def getVideos3(name1, urlmain):
        content = getUrl('https://www.skylinewebcams.com/it.html')
        pass#print "getVideos3 content A =", content
        n1 = content.find('menu-title text-center">', 0)
        n2 = content.find('id="cams-category', n1)
        content = content[n1:n2]
        pass#print 'getVideos3 content B =', content

        regexvideo = 'a href="(.*?)" class="menu-item">(.*?)</a>'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pic = pixx
        pass#print 'getVideos3 match =', match
        items = []
        for url, name in match:
            url1 = 'https://www.skylinewebcams.com' + url
            name = name.replace('<strong>', '')
            pic = pixx

            item = name + "###" + url1
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url1 = item.split("###")[1]
            # addDirectoryItem(name, {"name":name, "url":url1, "mode":"6"}, pic)
            addDirectoryItem(name, url1,6, pic, fanart)

        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos4(name1, urlmain):
        content = getUrl(urlmain)
        pass#print "content B =", content
         # webcam"><a href="
        regexvideo = 'webcam">.*?<a href="(.*?)".*?alt="(.*?)"'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'match =', match
        items = []
        pic = pixx
        for url, name in match:
            url1 = 'https://www.skylinewebcams.com' + url
    
            f = file(playlistDir +'/Favorit.txt', 'a')
            f.write(name + '\n')
            f.write(url1 + '\n')
            f.close()
            item = name + "###" + url1
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url1 = item.split("###")[1]
            # addDirectoryItem(name, {"name":name, "url":url1, "mode":"7"}, pic)
            add_link(name, url1, 7, pic,fanart )


def getVideos5X(name, url):
        name = "video"
#        url = "https://www.skylinewebcams.com/en/webcam/brasil/rio-de-janeiro/rio-de-janeiro/copacabana-beach.html"
        if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"): # enigma2 KodiLite
            vid = playlistDir + '/vid.txt'
            cmd = "python '/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/__main__.py' --no-check-certificate --skip-download -f best --get-url '" + url + "' > " + vid #/tmp/vid.txt"
            pass#print "In getVideos5 cmd =", cmd
            if os.path.exists(vid): #"/tmp/vid.txt"):
                os.remove(vid) #"/tmp/vid.txt")
            os.system(cmd)
            url = vid #"/tmp/vid.txt"

        if not os.path.exists(url):
              os.system("sleep 5")
              playVideo(name, url)
        else:
              playVideo(name, url)

def getVideos5(name, url):
        import youtube_dl
        print "Here in getVideos4 url 1=", url
        from youtube_dl import YoutubeDL
        print "Here in getVideos4 url 2", url
        ydl_opts = {'format': 'best'}
        ydl = YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
       # url = "https://www.youtube.com/watch?v=CSYCEyMQWQA"
        result = ydl.extract_info(url, download=False)
        print "result =", result
        url = result["url"]
        print "Here in Test url =", url
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
        player = xbmc.Player()
        player.play(url, li)


def getVideos6(name1, urlmain):
        content = getUrl(urlmain)
        pass#print "content B =", content
        regexvideo = '<a class="noDec" href="(.*?)".*?alt="(.*?)"'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'match =', match
        pic = pixx        
        for url, name in match:
            if not "https://www.earthcam.com" in url:
                   continue
            url1 = url
    
            addDirectoryItem(name, url1,8, pic, fanart)
            # addDirectoryItem(name, {"name":name, "url":url1, "mode":"8"}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos7(name, urlmain):
        content = getUrl(urlmain)
        pass#print "content C =", content
#        regexvideo = '"livestreamingpath"\:"(.*?)m3u8'
        regexvideo = 'html5_streamingdomain"\:"(.*?)".*?html5_streampath"\:"(.*?)m3u8'
        match = re.compile(regexvideo, re.DOTALL).findall(content)
        pass#print 'match =', match

        url = match[0][0] + match[0][1] + "m3u8"
        url = url.replace("\\", "")
        pass#print "In Webcam7 url =", url
        playVideo(name, url)

def getVideos8(name, urlmain):
        content = getUrl('http://www.livecameras.gr/')
        pass#print 'Webcam8 content A =', content#pass#
        
        # regexvideo = 'item1".*?href="(.*?)".*?data-title="(.*?)".*?<img src=""(.*?)"/>'        
        
        regexvideo = 'a class="item1" href="(.*?)".*?data-title="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pic = pixx
        pass#print 'Webcam8 match =', match#pass#
        for url, name in match:
            url1 = 'http:' + url

    
            # addDirectoryItem(name, url1,5, pic, fanart)

            add_link(name, url1, 5, pic,fanart )
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
        
# def addDirectoryItem(name, parameters={},pic=""):
    # li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    # url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    # return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	try:
		liz.setContentLookup(False)
	except:
		pass
	liz.setProperty('IsPlayable', 'true')
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)
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
   elif mode == str(4):
      ok = getVideos2(name, url)
   elif mode == str(5):
      ok = playVideo(name, url)
   elif mode == str(2):
      ok = getVideos3(name, url)
   elif mode == str(6):
      ok = getVideos4(name, url)
   elif mode == str(7):
      ok = getVideos5(name, url)
   elif mode == str(3):
      ok = getVideos6(name, url)
   elif mode == str(8):
      ok = getVideos7(name, url)
   elif mode == str(9):
      ok = getVideos8(name, url)
xbmcplugin.endOfDirectory(thisPlugin)

