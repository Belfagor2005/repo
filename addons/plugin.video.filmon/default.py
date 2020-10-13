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

thisPlugin = int(sys.argv[1])
addonId = "plugin.video.filmon"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

def getUrl(url):
   pass#print "Here in getUrl url =", url
   req = urllib2.Request(url)
   req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
   response = urllib2.urlopen(req)
   link=response.read()
   response.close()
   return link
	
def getUrl2(url, referer):
   pass#pass#print "Here in getUrl2 url =", url
   req = urllib2.Request(url)
   req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
   req.add_header('Referer', referer)
   response = urllib2.urlopen(req)
   link=response.read()
   response.close()
   return link 

Host = "http://www.filmon.com/group" 

def showContent():
        content = getUrl(Host)
        pass#print "content A =", content
        regexvideo = '<li class="group-item".*?a href="(.*?)".*?title="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        for url, name in match:
                url = url.replace(" ", "")
                url = url.replace("\\n", "")
                url = url.replace('\r','')
                name = name.replace('\r','')
                pic = " "
                url1 = "http://www.filmon.com" + url 
                addDirectoryItem(name, {"name":name, "url":url1, "mode":1}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name, url):
        pass#print "In name =", name
        pass#print "getVideos url =", url
        content = getUrl2(url, "http://www.filmon.com")
        pass#print "In Filmon2 content A =", content
        regexvideo = '<li class="channel i-box-sizing".*?channel_id="(.*?)".*?title="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        
        pass#print "In getVideos match =", match
        for url, name in match:
                url = "https://www.filmon.com/api-v2/channel/" + url 
                name = name.replace('\r','')
                pic = " "
                addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos2(name1, urlmain):
        url = "http://www.filmon.com/tv/api/init"
        fpage = getUrl(url)
        pass#print "In Filmon2 fpage =", fpage
        regexvideo = 'session_key":"(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(fpage)
        pass#print "In Filmon2 fpage match =", match
        url = urlmain + "?session_key=" + match[0]
        content = getUrl2(url, "http://www.filmon.com")
        pass#print "In getVideos2 content=", content
        regexvideo = '"quality".*?url"\:"(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "In getVideos2 fpage match 2=", match
        for url in match:
                       if "low" in url:
                              name = name1 + "-low.stream"
                       else:       
                              name = name1 + "-high.stream"
                       url = url.replace("\\", "")

                       pic = " "
                       addDirectoryItem(name, {"name":name, "url":url, "mode":4}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	         
        
def getVideos3(name1, urlmain):
        content = getUrl(urlmain)
        pass#print "content C =", content

        regexvideo = 'thumb_container video.*?href="(.*?)" title="(.*?)">.*?src="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        for url, name, pic in match:
                 name = "Dclip-" + name.replace('"', '')
                 url = "http://www.deviantclip.com" + url
                 pic = pic 
                 ##pass#print "Here in getVideos url =", url
                 addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)            
        
                
def playVideo(name, url):
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
      ok = playVideo(name, url)