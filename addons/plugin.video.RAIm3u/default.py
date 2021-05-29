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


import xbmc,xbmcplugin
import xbmcgui
import sys
# import urllib, urllib2
import time
import re
# from htmlentitydefs import name2codepoint as n2cp
# import httplib
# import urlparse
from os import path, system
import socket
# from urllib2 import Request, URLError, urlopen
# from urlparse import parse_qs
# from urllib import unquote_plus
import string
import os
import xbmcaddon
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

   
thisPlugin = int(sys.argv[1])
addonId = "plugin.video.RAIm3u"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

ADDON = xbmcaddon.Addon()
ADDON_DATA = ADDON.getAddonInfo('profile')
ADDON_PATH = ADDON.getAddonInfo('path')
DESCRIPTION = ADDON.getAddonInfo('description')
FANART = ADDON.getAddonInfo('fanart')
ICON = ADDON.getAddonInfo('icon')
ID = ADDON.getAddonInfo('id')
NAME = ADDON.getAddonInfo('name')
VERSION = ADDON.getAddonInfo('version')
       
this = ADDON_PATH + '/rai-play-'       

def getUrl(url):
    print("Here in getUrl url =", url)
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urlopen(req)
    link=response.read()
    response.close()
    return link

def getUrl2(url, referer):
    print("Here in getUrl2 url =", url)
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', referer)
    response = urlopen(req)
    link=response.read()
    response.close()
    return link 

def showContent():
                names = []
                urls = []
                modes = []
                names.append("tutti")
                urls.append('https://www.raiplay.it/genere/Film---Tutti-377b40d5-e723-4bfa-bc64-3e44c0d5b6e3.html')
                modes.append("10")
                names.append("commedia")
                urls.append('https://www.raiplay.it/genere/Film---Commedia-6b833537-2e77-477e-9719-5d75716591ee.html')
                modes.append("10")               
                names.append("drammatico")
                urls.append('https://www.raiplay.it/genere/Drammatico-9307f261-b0eb-4bf4-b07a-a63acddc24e9.html')
                modes.append("10")        
                names.append("triller")
                urls.append('https://www.raiplay.it/genere/Film---Thriller-bb5c23c2-302a-4119-8d23-4c8c5ddd5a8f.html')        
                modes.append("10") 
                names.append("sentimentale")
                urls.append('https://www.raiplay.it/genere/Film---Sentimentale-8e12ada5-c2fc-4bfb-b3de-d671c099cbe5.html')        
                modes.append("10") 
                names.append("action")
                urls.append('https://www.raiplay.it/genere/Film---Azione-d81d3adf-f07e-4238-9342-319990ec7801.html')        
                modes.append("10") 
                names.append("western")
                urls.append('https://www.raiplay.it/genere/Avventura-cfe3ba02-d3bb-449e-a31f-abc95ddc6f6a.html')        
                modes.append("10") 
                names.append("corti")
                urls.append('https://www.raiplay.it/genere/Film-Azione-3b9b3b6a-1b30-41d9-b820-da801a2872f2.html')        
                modes.append("10") 
                names.append("animazione")
                urls.append('https://www.raiplay.it/genere/Teen---Animazione-717f1618-4b0a-4e2c-b312-e9525934c651.html')        
                modes.append("10") 
                names.append("ragazzi")
                urls.append('https://www.raiplay.it/genere/Film-per-ragazzi-6e567ae1-4d10-4894-8002-00f79fea4b21.html')        
                modes.append("10") 
                names.append("scuola")
                urls.append('https://www.raiplay.it/genere/LaScuolaNonSiFerma-17efa786-03cb-4b7d-b4d5-53e37d51efa3.html')        
                modes.append("10") 
                names.append("cartoni-bambini")
                urls.append('https://www.raiplay.it/genere/Bambini---Cartoni-per-bambini-e054e438-522e-48aa-a631-51b6af17f09d.html')        
                modes.append("10") 
                names.append("cartoni-grandi")
                urls.append('https://www.raiplay.it/genere/Bambini---Cartoni-per-ragazzi-97f2b856-d486-4e33-9211-8bd006f8f109.html')        
                modes.append("10") 
                names.append("film-bimbi")
                urls.append('https://www.raiplay.it/genere/Bambini---Film-di-animazione-6b076020-f300-404a-aa58-15eef3b16eda.html')        
                modes.append("10") 
                names.append("film-animazione")
                urls.append('https://www.raiplay.it/genere/Fiction---Sottotitolate-70526feb-348f-4a57-94c7-e570aa24b926.html')        
                modes.append("10") 
                names.append("fiction-sottotitolate")
                urls.append('https://www.raiplay.it/genere/Fiction---Sottotitolate-70526feb-348f-4a57-94c7-e570aa24b926.html')        
                modes.append("10")                 
                names.append("fiction-drammatico")
                urls.append('https://www.raiplay.it/genere/Fiction---Drammatico-a25e89bc-d7e3-4ce4-a6c5-d8e081fc49d7.html')        
                modes.append("10")                          
                names.append("fiction-commedia")
                urls.append('https://www.raiplay.it/genere/Fiction---Commedia-0a2e1a90-b257-4ae6-9695-8e4338cc320c.html')        
                modes.append("10")                          
                names.append("fiction-sentimentale")
                urls.append('https://www.raiplay.it/genere/Fiction---Sentimentale-719f377c-b684-49e6-8360-0ec2008929f5.html')        
                modes.append("10")   
                names.append("fiction-crime")
                urls.append('https://www.raiplay.it/genere/Fiction---Crime-14013de2-c8a8-4537-bc93-96502d550ff8.html')        
                modes.append("10")   
                names.append("fiction-docu")
                urls.append('https://www.raiplay.it/genere/Fiction---Docufiction-44c8b957-0529-4363-b1cb-2ec3b8fee21d.html')        
                modes.append("10") 
                names.append("fiction-sceneggiati")
                urls.append('https://www.raiplay.it/genere/Fiction---Sceneggiati-8290688b-8ee8-43f5-9461-6721318a47b5.html')        
                modes.append("10")                 
                names.append("fiction-costume")
                urls.append('https://www.raiplay.it/genere/Fiction---In-costume-ffa11285-88bd-4e14-b561-f19db720dc49.html')        
                modes.append("10")                  
                names.append("fiction-religioso")
                urls.append('https://www.raiplay.it/genere/Fiction---Religioso-28a02b4f-3a16-4569-9c6e-0da3afaa47c5.html')        
                modes.append("10")                  
                pic = " "
                i = 0
                for name in names:
                    url = urls[i]
                    mode = modes[i]
                    i = i+1
                    addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos1(name, urlmain):
        content = getUrl(urlmain)
        content = six.ensure_str(content)
        regexvideo = 'data-video-json="(.*?)".*?"name" content="(.*?)".*?" src="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        filex = this + name + '.m3u'
        f=open(filex,"w")        
        f.write("EXTM3U\n")
        for url, name, pic in match:
             url = "https://www.raiplay.it" + url
             url1 = getVideos(name, url)
             name = name.replace('&#x27;', "'")
             txt1 = "#EXTINF:-1," +name + "\n"
             f.write(txt1)
             txt2 = url1 + "\n"
             f.write(txt2)
        f.close()
        
def getVideos(name, urlmain):
    content = getUrl(urlmain)
    content = six.ensure_str(content)
    regexvideo = '"first_item_path".*?"(.*?)"'
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    print("getVideos match =", match)
    url = "https://www.raiplay.it" + match[0]
    content2 = getUrl(url)
    content2 = six.ensure_str(content2)
    print("getVideos content2 =", content2)
    regexvideo = 'content_url".*?"(.*?)"'
    match2 = re.compile(regexvideo,re.DOTALL).findall(content2)
    print("match2 =", match2)
    url = match2[0]
    return url
                
def playVideo(name, url):
           print("Here in playVideo url =", url)
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
    url = sys.argv[0] + '?' + urlencode(parameters)
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
url = unquote(url)
mode =  str(params.get("mode", ""))

if not sys.argv[2]:
    ok = showContent()
else:
    if mode == str(1):
        ok = getVideos(name, url)
    elif mode == str(10):
        ok = getVideos1(name, url)  
    elif mode == str(3):
        ok = playVideo(name, url)   
    elif mode == str(4):
        ok = getVideos2(name, url)  
