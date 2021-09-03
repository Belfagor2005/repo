#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys, xpath, xbmc, os
if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"): # enigma2 KodiLite
    libs = sys.argv[0].replace("default.py", "resources/lib")
    import six
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
import xbmc
import xbmcaddon
import re
from os import path, system, walk
import socket
import base64

PY3 = False
try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import quote, unquote_plus, unquote, urlencode
    from urllib.request import urlretrieve
    from urllib.parse import urlparse
    from html.entities import name2codepoint as n2cp
    import http.client
except:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urllib import quote, unquote_plus, unquote, urlencode
    from urllib import urlretrieve
    from urlparse import urlparse
    from htmlentitydefs import name2codepoint as n2cp
    import httplib


thisPlugin = int(sys.argv[1])
addonId = "plugin.video.freearhey"
__settings__ = xbmcaddon.Addon(addonId)
thisAddonDir = xbmc.translatePath(__settings__.getAddonInfo('path'))#.decode('utf-8')
sys.path.append(os.path.join(thisAddonDir, 'resources', 'lib'))
home = __settings__.getAddonInfo('path')
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)
fanart = xbmc.translatePath(os.path.join(home, 'fanart.png'))

m3u = 'aHR0cHM6Ly9naXRodWIuY29tL2lwdHYtb3JnL2lwdHYv'
server = base64.b64decode(m3u)
estm3u = 'aHR0cHM6Ly90aXZ1c3RyZWFtLndlYnNpdGUvcGhwX2ZpbHRlci9maC5waHA='
m3uest = base64.b64decode(estm3u)

host1 = 'https://raw.githubusercontent.com/freearhey/iptv/master/index.m3u'
host = 'https://raw.githubusercontent.com/freearhey/iptv/master/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' }
def checkStr(txt):
    if PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(six.text_type())):
            txt = txt.encode('utf-8')
    return txt

def checkStr(txt):
    if PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(six.text_type())):
            txt = txt.encode('utf-8')
    return txt

def getUrl2(url, referer):
    try:
        req =Request(url)
    except:
        req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', referer)
    try:
        try:
            response = urlopen(req)
        except:
            response = urlopen(req)
        link=response.read().decode('utf-8')
        response.close()
        return link
    except:
        import ssl
        gcontext = ssl._create_unverified_context()
        try:
            response = urlopen(req)
        except:
            response = urlopen(req)
        link=response.read().decode('utf-8')
        response.close()
        return link

def getUrl(url):
    link = []
    try:
        import requests
        link = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'}).text
        return link
    except ImportError:
        print("Here in client2 getUrl url =", url)
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urlopen(req, None, 30)
        link=response.read().decode('utf-8')
        response.close()
        print("Here in client2 link =", link)
        return link
    except:
        return
    return

def showContent():
        names = []
        urls = []
        names.append("freearhey (git)")
        urls.append(host1)
        names.append("Free Cowntry")
        urls.append(m3uest)
        i = 0
        for name in names:
                url = urls[i]
                pic = " "
                i = i+1
                addDirectoryItem(name, {"name":name, "url":url, "mode":1}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def showContent2(name, url):
    print('url---:', url)
    content = getUrl(url)
    # content = six.ensure_str(content)
    print("content 2 =", content)
    pass#print "content 2 =", content
    # fpage = content.read()
    regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
    match = re.compile(regexcat,re.DOTALL).findall(content)
    for name, url in match:
            url = url.replace(" ", "%20")
            url = url.replace("\\n", "")
            url = url.replace('\r','')
            name = name.replace('\r','')
            pic = " "
            addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent3(name, url):
    url = str(url)
    # url = six.ensure_str(url)
    print('url--semifininal-:', url)
    if 'fh.php' in url:
        url = url
    else:
        # url = six.ensure_str(host) + url
        url = str(host) + url

    content = getUrl(url)
    # req = Request(url, None, headers=headers)
    # content = urlopen(req, timeout=30).read()
    # content = six.ensure_str(content)
    print("content 3 =", content)
    pass
    regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
    match = re.compile(regexcat,re.DOTALL).findall(content)
    for name, url in match:
            url = url.replace(" ", "%20")
            url = url.replace("\\n", "")
            url = url.replace('\r','')
            url = url.replace('https','http')
            name = name.replace('\r','')
            pic = " "
            print('url final:', url)
            addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)


def playVideo(name, url):
    print("Here in playVideo url =", url)
    pic = "DefaultFolder.png"
    print("Here in playVideo url B=", url)
    li = xbmcgui.ListItem(label=name)
    li.setArt({'thumb': "DefaultFolder.png", 'icon': pic})
    player = xbmc.Player()
    player.play(url, li)

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(label=name)
    li.setArt({'thumb': "DefaultFolder.png", 'icon': pic})
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
        ok = showContent2(name, url)
    elif mode == str(2):
        ok = showContent3(name, url)
    elif mode == str(3):
        ok = playVideo(name, url)
