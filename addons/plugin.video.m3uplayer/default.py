#!/usr/bin/python
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


import xbmc,xbmcaddon, xbmcplugin
import xbmcgui
import sys
import time
import re
from os import path, system, walk
import socket
import urllib, urllib2
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs
from urllib import unquote_plus


thisPlugin = int(sys.argv[1])
addonId = "plugin.video.m3uplayer"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)
       
Addon = xbmcaddon.Addon(addonId)
addonDir = Addon.getAddonInfo('path').decode("utf-8")
print("Here in playlistloader addonDir =", addonDir)
playlistDir = path.join(addonDir, 'Playlists')
print("Here in playlistloader playlistDir =", playlistDir)       
fanart = xbmc.translatePath(os.path.join(addonDir, 'fanart.jpg'))
i_free = xbmc.translatePath(os.path.join(addonDir, 'icon.png'))
       
       
def getUrl(url):
    print("Here in youtube getUrl url =", url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
           response = urllib2.urlopen(req)
    except:
           ctx = ssl.create_default_context()
           ctx.check_hostname = False
           ctx.verify_mode = ssl.CERT_NONE
           response = urllib2.urlopen(req, context=ctx)
    link=response.read()
    response.close()
    return link
    
def getUrl2(url, referer):
    print("Here in  getUrl2 url =", url)
    print("Here in  getUrl2 referer =", referer)
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
        
    
def showContent():
#        url = "http://freestreams-live1.com/"
        url = "https://dailym3uiptv.com/list/"
        content = getUrl(url)
        print("content A =", content)
        pic = " "
        i1 = 0           
        if i1 == 0:
                regexcat = 'figure class="mh-posts-grid-thumb".*?a href="(.*?)" title="(.*?)"'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                print("match 1=", match)
                n1 = 0
                for url, name in match:
                        url1 = url
#                        n1 = ni+1
#                        if n1 == 1: break
                        pic = i_free
                        addDirectoryItem(name, {"name":name, "url":url, "mode":1}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)
               
#                url1 = match[0][0]
#                name1 = " "
#                getVideos(name1, url1) 

def getVideos(name1, urlmain):
    content = getUrl(urlmain)
    print("getVideos content B =", content)

    regexvideo = '<p.*?code>(.*?)<'
#regexvideo = 'The iptv from here.*?href="(.*?)".*?tle="(.*?)"' 
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    print("match 2 =", match)
    n1 = 1
    for url in match:
         pic = i_free
         name = "Link " + str(n1)
         n1 = n1+1
         addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)                      


def getVideos2(name, url):
#        url = match[0][0]
        from zipfile import ZipFile
        content = getUrl(url)
        f1=open("/tmp/w.zip","w")
        f1.write(content)
        f1.close()
        zf = ZipFile('/tmp/w.zip', 'r')
        zf.extractall(playlistDir)
        zf.close()
        getFiles()


#######################################################
def getFiles():
      print("Here in showContent playlistDir = ", playlistDir)
      uLists = playlistDir
      for root, dirs, files in walk(uLists):
          for name in files:
              if (not name.endswith(".m3u")) and (not name.endswith(".M3U")):
                     continue
              else:
                             url = " "
                             pic = i_free
                             print("Here in getFiles name  = ", name)
                             addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
          xbmcplugin.endOfDirectory(thisPlugin)

def showContent2(name, url):
                """
                uLists = playlistDir
                name = name.replace("+", " ")
                file1 = uLists + "/" + name
                
                print "Here in showContentA2 file1 = ", file1
                f1=open(file1,"r")
                fpage = f1.read()
                """
                fpage = getUrl(url)
                fpage2 = str(fpage, errors='ignore')
                regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat,re.DOTALL).findall(fpage2)
                print("In showContent2 match =", match)
                n1 = 0
                for name, url in match:
#                        if not ".m3u8" in url:
#                               continue
#                               n1 = n1+1
                        url = url.replace(" ", "")
                        print("In showContent2 url 1=", url)
                        url = url.replace("\\n", "")
                        print("In showContent2 url 2=", url)
                        url = url.replace('\\r','')
                        print("In showContent2 url 3=", url)
                        name = name.replace('\\r','')
                        name = name.replace('\\n','')
                        print("In showContent2 name =", name)
                        print("In showContent2 url =", url)
#                        request = requests.get(url)
#                        if request.status_code != 200:
#                                continue
#                        n1 = n1+1        
                        pic = i_free
                        addDirectoryItem(name, {"name":name, "url":url, "mode":4}, pic)
                        # add_link(name, url, 4, pic, fanart)
#                if n1 == 0: return        
                xbmcplugin.endOfDirectory(thisPlugin)
                
def playVideo(name, url):
           pic = "DefaultFolder.png"
           print("Here in playVideo url B=", url)
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
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

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
print("In default.py name =", name)
url =  str(params.get("url", ""))
print("In default.py url =", url)
url = urllib.unquote(url)
print("In default.py url 2=", url)
mode =  str(params.get("mode", ""))

if not sys.argv[2]:
    ok = showContent()
else:
    if mode == str(1):
        ok = getVideos(name, url)
    elif mode == str(2):
#               ok = getVideos2(name, url)
        ok = showContent2(name, url)
    elif mode == str(3):
        ok = showContent2(name, url)
    elif mode == str(4):
        ok = playVideo(name, url)   


