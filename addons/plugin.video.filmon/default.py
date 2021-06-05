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

import xbmcplugin
import xbmcgui
import time
import re
from os import path, system
import socket
import six
PY3 = sys.version_info.major >= 3

if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse, unquote
    from urllib.parse import urlencode, quote
    import urllib.request, urllib.parse, urllib.error
    from html.entities import name2codepoint as n2cp
    import http.client
    from urllib.parse import parse_qs
    from urllib.parse import unquote_plus

else:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urlparse import urlparse
    from urllib import urlencode, quote
    import urllib, urllib2
    from htmlentitydefs import name2codepoint as n2cp
    import httplib
    from urlparse import parse_qs
    from urllib import unquote_plus, unquote


def checkStr(txt):
    if PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(six.text_type())):
            txt = txt.encode('utf-8')
    return txt
    
thisPlugin = int(sys.argv[1])
addonId = "plugin.video.filmon"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

def getUrl(url):
        print( "Here in getUrl url =", url)
        req = Request(url)       
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
            urlopen(req)
            link=response.read()
            response.close()
            return link
        except:
            import ssl
            gcontext = ssl._create_unverified_context()
            try:
                response = request.urlopen(req)
            except:       
                response = urlopen(req)
            link=response.read()
            response.close()
            return link
            
def getUrl2(url, referer):
        print("Here in  getUrl2 url =", url)
        print("Here in  getUrl2 referer =", referer)
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', referer)
        try:
              response = urlopen(req)
              link=response.read()
              response.close()
              return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urlopen(req, context=gcontext)
               link=response.read()
               response.close()
               return link

Host = "http://www.filmon.com/group" 

def showContent():
        content = getUrl(Host)
        if PY3:
            content = six.ensure_str(content)   
            
        print("content A =", content)
        regexvideo = '<li class="group-item".*?a href="(.*?)".*?title="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        for url, name in match:
                url = url.replace(" ", "")
                url = url.replace("\\n", "")
                url = url.replace('\r','')
                name = name.replace('\r','')
                pic = " "
                url1 = "http://www.filmon.com" + url 
                url1 = checkStr(url1)
                name = checkStr(name)                
                addDirectoryItem(name, {"name":name, "url":url1, "mode":1}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name, url):
        print("In name =", name)
        print("getVideos url =", url)
        content = getUrl2(url, "http://www.filmon.com")
        
        if PY3:
            content = six.ensure_str(content)           
        print("In Filmon2 content A =", content)


        n1 = content.find('id="group-channels', 0)
        n2 = content.find('</body>', n1)
        r2 = content[n1:n2]

        regexvideo = '"channel i-box-sizing.*?channel_id="(.*?)".*?title="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(r2)
        
        print("In getVideos match =", match)
        for url, name in match:
                url = "https://www.filmon.com/api-v2/channel/" + url 
                name = name.replace('\r','')
                
                url = checkStr(url)
                name = checkStr(name) 
            
                pic = " "
                addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos2(name1, urlmain):
        # url = "http://www.filmon.com/tv/api/init"
        try:
            url = 'http://www.filmon.com/tv/api/init?app_android_device_model=GT-N7000&app_android_test=false&app_version=2.0.90&app_android_device_tablet=true&app_android_device_manufacturer=SAMSUNG&app_secret=wis9Ohmu7i&app_id=android-native&app_android_api_version=10%20HTTP/1.1&channelProvider=ipad&supported_streaming_protocol=rtmp'
            # fpage = getUrl(url)
            req = Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            page = urlopen(req)
            content = page.read()
            if PY3:
                content = six.ensure_str(content)                
            # print("In Filmon2 1 =", content)
        # except:
            # print('We failed to open "%s".' % url)

        # try:
            regexvideo = 'session_key":"(.*?)"'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print("In Filmon2 fpage match =", match)
            url = urlmain + "?session_key=" + match[0]
            # content = getUrl2(url, "http://www.filmon.com")
            req = Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            page = urlopen(req)
            content = page.read()
            if PY3:
                content = six.ensure_str(content)               
            
            # print("In Filmon2 2 =", content)
        # except:
            # print('We failed to open "%s".' % url)

        # try:                
            regexvideo = '"quality".*?url"\:"(.*?)"'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            print("In getVideos2 fpage match 2=", match)
            for url in match:
                if "low" in url:
                    name = name1 + "-low.stream"
                else:       
                    name = name1 + "-high.stream"
                url = url.replace("\\", "")

                pic = " "
                addDirectoryItem(name, {"name":name, "url":url, "mode":4}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)	
            
        except:
            print('We failed".')
            
        
def getVideos3(name1, urlmain):
        content = getUrl(urlmain)
        pass#print "content C =", content
        
        if PY3:
            content = six.ensure_str(content)   
            
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
   elif mode == str(2):
      ok = getVideos2(name, url)
   elif mode == str(3):
      ok = getVideos3(name, url)
   elif mode == str(4):
      ok = playVideo(name, url)