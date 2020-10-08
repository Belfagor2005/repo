#!/usr/bin/python
import sys, xpath, xbmc
import os

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

import xbmc,xbmcaddon, xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from os import path, system, walk
import socket
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs
from urllib import unquote_plus
import base64

thisPlugin = int(sys.argv[1])
# addonId = "plugin.video.freearhey"
# dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
# if not path.exists(dataPath):
       # cmd = "mkdir -p " + dataPath
       # system(cmd)
# Addon = xbmcaddon.Addon(addonId)
# AddonName = Addon.getAddonInfo("name")
# fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
# icon = Addon.getAddonInfo('icon')
# addonDir = Addon.getAddonInfo('path').decode("utf-8")
# print "Here in playlistloader addonDir =", addonDir

addonId = "plugin.video.freearhey"
Addon = xbmcaddon.Addon(addonId)
mysettings = xbmcaddon.Addon(id = addonId)
# __language__ = mysettings.get_string
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
# artfolder = (home + '/resources/img/')
AddonName = Addon.getAddonInfo("name")
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
addonDir = Addon.getAddonInfo('path').decode("utf-8")
print "Here in playlistloader addonDir =", addonDir
m3u = 'aHR0cDovL2x1bHVsbGEuYWx0ZXJ2aXN0YS5vcmcvaXB0di1tYXN0ZXIv'
server = base64.b64decode(m3u)
estm3u = 'aHR0cDovL3RpdnVzdHJlYW0uY29tL2ZoLnBocA=='
m3uest = base64.b64decode(estm3u)
host = 'https://bit.ly/2ZRG8Fd'

def getUrl(url):
        # print "Here in getUrl url =", url
        # req = urllib2.Request(url)
        # req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        # response = urllib2.urlopen(req)
        # link=response.read()
        # response.close()
        # return link
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason

def showContent():
        names = []
        urls = []
        names.append("freearhey")
        urls.append("http://bit.ly/2ZRG8Fd")
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

                print 'url---:', url
                content = getUrl(url)
                print "content 2 =", content
                pass#print "content 2 =", content
                # fpage = content.read()
                regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                for name, url in match:
                        url = url.replace(" ", "")
                        url = url.replace("\\n", "")
                        url = url.replace('\r','')
                        name = name.replace('\r','')
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)


def showContent3(name, url):

                url=url
                print 'url--semifininal-:', url
                # url = 'http://bit.ly/2RpPCCg' + url
                if 'fh.php' in url:
                    url = url
                else:
                    url = server + url
                content = getUrl(url)
                print "content 3 =", content
                pass#print "content 3 =", content
                # fpage = content.read()
                regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                for name, url in match:
                        url = url.replace(" ", "")
                        url = url.replace("\\n", "")
                        url = url.replace('\r','')
                        url = url.replace('https','http')
                        name = name.replace('\r','')
                        pic = " "
                        print 'url final:', url
                        addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)


def playVideo(name, url):
           pass#print "Here in playVideo url =", url
           pic = "DefaultFolder.png"
           print "Here in playVideo url B=", url
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
        ok = showContent2(name, url)

    elif mode == str(2):
        ok = showContent3(name, url)

    elif mode == str(3):
        ok = playVideo(name, url)




