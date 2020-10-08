#!/usr/bin/python
# -*- coding: latin-1 -*-
"""
Copyright (C) 2018-2020
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
############################################################
Developed by Lululla & Pcd for TiVuStream.com and linuxsat-support
Thanks all developer includes in this addon..
"""
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
from os import path, system
import socket


##py 3
# import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
# from html.entities import name2codepoint as n2cp
# import http.client
# import urllib.parse
# from urllib.request import Request, urlopen
# from urllib.error import URLError
# from urllib.parse import parse_qs
# from urllib.parse import unquote_plus
##py2
import urllib, urllib2
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs
from urllib import unquote_plus
import base64
# import resolver
# sources = resolver.sources
# from resolver import getVideo
from resources.lib import resolver
sources = resolver.sources
from resources.lib.resolver import getVideo
from resources.lib.videos import *

thisPlugin = int(sys.argv[1])
addonId = "plugin.video.tivustream18"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))

if not path.exists(dataPath):
    cmd = "mkdir -p " + dataPath
    system(cmd)

__settings__ = xbmcaddon.Addon(addonId)
thisAddonDir = xbmc.translatePath(__settings__.getAddonInfo('path')).decode('utf-8')
sys.path.append(os.path.join(thisAddonDir, 'resources', 'lib'))
adult_request_password = __settings__.getSetting("adult_request_password")
print("In default.py adult_request_password =", adult_request_password)
adult_password = __settings__.getSetting("adult_password")
print("In default.py adult_password =", adult_password)
home = __settings__.getAddonInfo('path')
log_m3u = __settings__.getSetting('log_m3u')
artfolder = (home + '/resources/img/')
logos = (home + '/resources/logos/')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
fanart2 = xbmc.translatePath(os.path.join(home, 'fanart2.png'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
i_xxx = xbmc.translatePath(os.path.join(artfolder, 'xxx.png'))
f_xxx = xbmc.translatePath(os.path.join(artfolder, 'xxx.jpg'))
t_xxx = xbmc.translatePath(os.path.join(logos, 'thumbzilla.png'))
f_free = xbmc.translatePath(os.path.join(artfolder, 'free.jpg'))
f_search = xbmc.translatePath(os.path.join(artfolder, 'search.jpg'))
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'
####################################


std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}

HostThumb = "https://www.thumbzilla.com"
Host = "http://www.deviantclip.com/categories"


def get_data_path():
    dev = xbmc.translatePath(__settings__.getAddonInfo('profile'))
    if not os.path.exists(dev):
        os.makedirs(dev)
    return dev

def find_single_match(data, patron, index=0):
    try:
        matches = re.findall(patron, data, flags=re.DOTALL)
        return matches[index]
    except:
        return ""

def find_multiple_matches(text, pattern):
    return re.findall(pattern, text, re.DOTALL)

def get_all_settings_addon():
    # read settings.xml and return {id: value}
    infile = open(os.path.join(get_data_path(), "settings.xml"), "r")
    data = infile.read()
    infile.close()
    ret = {}
    matches = find_multiple_matches(data, '<setting id="([^"]*)" value="([^"]*)')
    for _id, value in matches:
        ret[_id] = get_setting(_id)
    return ret

# def get_setting(name, channel="", server="", default=None):
def get_setting(name, default=None):
    value = __settings__.getSetting(name)
    if not value:
        return default
    if value == "true":
        return True
    elif value == "false":
        return False
    else:
        if name in ["adult_password"]:
            return value
        else:
            try:
                value = int(value)
            except ValueError:
                pass
            return value

def getUrl(url):
        print("Here in getUrl url =", url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
               response = urllib2.urlopen(req)
               link=response.read()
               response.close()
               return link
        except urllib2.URLError as e:
               print(e.reason)

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

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		return link
	except urllib2.URLError as e:
		print('We failed to open "%s".' % url)
		if hasattr(e, 'code'):
			print('We failed with error code - %s.' % e.code)
		if hasattr(e, 'reason'):
			print('We failed to reach a server.')
			print('Reason: ', e.reason)

def showContent():
        names = []
        urls = []
        modes = []
        #http://bit.ly/tvstreamclxxx
        names.append("Version Support (changelog)")
        thost = 'aHR0cDovL2JpdC5seS8='
        SS0 = base64.b64decode(thost)
        thost3 = 'dHZzdHJlYW1jbHh4eA=='
        SS3 = base64.b64decode(thost3)
        Host1 = SS0 + SS3
        urls.append(Host1)
        modes.append("112")
        
        names.append("Live Stream and Adult Movies")
        thost1 = 'aHR0cHM6Ly90aXZ1c3RyZWFtLmNvbS8='
        SS1 = base64.b64decode(thost1)
        thost2 = 'dHNsRW4ucGhwP3A9NQ=='
        SS2 = base64.b64decode(thost2)
        Host2 = SS1 + SS2
        urls.append(Host2)
        modes.append("11")
        # names.append("Live Stream and Adult Movies")
        # thost1 = 'aHR0cDovL3BhdGJ1d2ViLmNvbQ=='
        # SS1 = base64.b64decode(thost1)
        # thost2 = 'L2lwdHYvZTJsaXN0ZS9zdWJib3VxdWV0LnRpdnVzdHJlYW1fYWR1bHR4eHgudHY='
        # SS2 = base64.b64decode(thost2)
        # Host2 = SS1 + SS2
        # urls.append(Host2)
        # modes.append("11")        
        names.append("Adult Videos")
        urls.append("https://www.pornhd.com/category")
        modes.append("21")
        names.append("XXX Porn Video")
        urls.append("https://www.ashemaletube.com")
        modes.append("105")
        names.append("Thumbzilla")
        urls.append("https://www.thumbzilla.com")
        modes.append("90")
        i = 0
        pic = f_free
        for name in names:
                url = urls[i]
                mode = modes[i]
                i = i+1
                addDirectoryItem(name, url, mode, pic, fanart)
        # xbmcplugin.endOfDirectory(thisPlugin)

def showContentB():
        #home()
        names = []
        urls = []
        modes = []
        names.append("Drtuber")   #ok
        urls.append("https://www.drtuber.com/categories")
        modes.append("1")
        names.append("Empflix")     #ok
        urls.append("https://www.empflix.com/categories/")
        modes.append("1")
        names.append("Eporner")   #search ok
        urls.append("https://www.eporner.com/categories")
        modes.append("1")
        names.append("Hellporno")   #search ok
        urls.append("https://hellporno.com/categories/")
        modes.append("1")
        names.append("Pornotube")   #ok
        urls.append("https://www.pornotube.com/orientation/straight/home/page/1")
        modes.append("1")
        names.append("Tnaflix")    #ok
        urls.append("https://www.tnaflix.com/categories")
        modes.append("1")
        names.append("Youjizz")  #nok but plays video
        urls.append("https://www.youjizz.com/")
        modes.append("1")
        names.append("Youporn")     #search ok
        urls.append("https://www.youporn.com/categories/")
        modes.append("1")
        names.append("Xtube")       #ok
        urls.append("https://www.xtube.com/categories")
        modes.append("1")
        names.append("Xvideos")  #ok
        urls.append("https://www.xvideos.com/")
        modes.append("1")
        names.append("Xxxymovies")
        urls.append("https://xxxymovies.com/categories/")
        modes.append("1")
        i = 0
        for name in names:
                url = urls[i]
                mode = modes[i]
                pic = f_xxx
                i = i+1
                addDirectoryItem(name, url, mode, pic, fanart)
        # xbmcplugin.endOfDirectory(thisPlugin)

def showContent1(name, url):
        #home()
        pic = f_xxx
        print(" showContent1 name =", name)
        print(" showContent1 url =", url)
        if "pornotube" in name.lower():
               pic = f_search
               url = "https://www.pornotube.com/orientation/straight/search/text/term/pornotube-search/page/1"
               addDirectoryItem("pornotube-search", url, 100, pic, fanart)
               content = getUrl(url)
               print("In showContent1 name =", name)
               print( "In showContent1 content =", content)
              #https://www.pornotube.com/orientation/straight/
              #https://www.pornotube.com/orientation/straight/home/page/1
               regexvideo = 'option value="/orientation/straight/search/category/id/(.*?)".*?>(.*?)<'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               pic = f_xxx
               print("showContent1 match =", match)
               for url, name in match:
                 print( "Here in showContent1 name 1=", name)
                 print("Here in showContent1 url =", url)
                 name = name.replace("&amp;", "&")
                 name = name.replace("\\n", "")
                 name = "Pornotube-" + name
                 print("Here in showContent1 name=", name)
                 url = "https://www.pornotube.com/orientation/straight/search/category/id/" + url
                 print("Here in showContent1 url =", url)
                 addDirectoryItem(name, url,2, pic, fanart)
               # xbmcplugin.endOfDirectory(thisPlugin)
        elif "tnaflix" in name.lower():
               pic = f_search
               url = "https://www.tnaflix.com/search.php?what=searchText&tab="
               addDirectoryItem("Tnaflix-search", url, 100, pic, fanart)
               content = getUrl(url)
               print("In showContent1 name =", name)
               print("In showContent1 content =", content)
               n1 = content.find('<div class="categories-wrapper"></div', 0)
               n2 = content.find('a href="/webcam-shows"', n1)
               content2 = content[n1:n2]
               print( "In showContent1 content2 =", content2)
               regexvideo = '<a href="(.*?)" title="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content2)
               pic = f_xxx
               print("showContent1 match =", match)
               for url, name in match:
                 print("Here in showContent1 name 1=", name)
                 print("Here in showContent1 url =", url)
                 name = name.replace("&amp;", "&")
                 name = name.replace("\\n", "")
                 name = "Tnaflix-" + name
                 print("Here in showContent1 name=", name)
                 url = "https://www.tnaflix.com" + url
                 print("Here in showContent1 url =", url)
                 addDirectoryItem(name, url, 2, pic, fanart)
               # xbmcplugin.endOfDirectory(thisPlugin)
        elif "hellporno" in name.lower():
               pic = f_search
               url = "https://hellporno.com/search/iPage/?q=searchText"
               addDirectoryItem("Hellporno-search", url, 100, pic, fanart)
               pass
        elif "eporner" in name.lower():
               pic = f_search
               url = "https://www.eporner.com/search/searchText/iPage/"
               addDirectoryItem("Eporner-search", url, 100, pic, fanart)
        elif "drtuber" in name.lower():
               pic = f_search
               url = "https://www.drtuber.com/search/videos/searchText/iPage"
               addDirectoryItem("Drtuber-search", url, 100, pic, fanart)
               content = getUrl(url)
               print("In showContent1 name =", name)
               print("In showContent1 content =", content)
               regexvideo = '<a href="/tags/(.*?)"> <span>(.*?)<'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("showContent1 match =", match)
               pic = f_xxx
               for url, name in match:
                 print("Here in showContent1 name 1=", name)
                 print("Here in showContent1 url =", url)
                 name = name.replace("&amp;", "&")
                 name = name.replace("\\n", "")
                 name = "Drtuber-" + name
                 print("Here in showContent1 name=", name)
                 #https://www.drtuber.com/tags/18-amateur
                 url = "https://www.drtuber.com/tags/" + url
                 print("Here in showContent1 url =", url)
                 addDirectoryItem(name, url,2, pic, fanart)
               # xbmcplugin.endOfDirectory(thisPlugin)
        elif "youjizz" in name.lower():
               pic = f_search
               url = "https://www.youjizz.com/search/searchText-iPage.html"
               addDirectoryItem("Youjizz-search",url, 100, pic, fanart)
               names = []
               urls = []
               names.append("popular")
               urls.append("https://www.youjizz.com/most-popular/")
               names.append("new")
               urls.append("https://www.youjizz.com/newest-clips/")
               names.append("top-rated")
               urls.append("https://www.youjizz.com/top-rated-month/")
               names.append("pornstars")
               urls.append("https://www.youjizz.com/pornstars/")
               i = 0
               pic = f_xxx
               for name in names:
                 url = urls[i]
                 i = i+1
                 print("Here in showContent1 name 1=", name)
                 print("Here in showContent1 url =", url)
                 name = "Youjizz-" + name
                 print("Here in showContent1 name=", name)
                 #
                 print("Here in showContent1 url =", url)
                 addDirectoryItem(name, url,2, pic, fanart)
               # xbmcplugin.endOfDirectory(thisPlugin)
        elif "xxxymovies" in name.lower():
               pic = f_search
               url = "https://xxxymovies.com/search/iPage/?q=searchText"
               addDirectoryItem("Xxxymovies-search", url, 100, pic, fanart)
               content = getUrl(url)
               print("In showContent1 name =", name)
               print("In showContent1 content =", content)
               regexvideo = '<a href="https\://xxxymovies.com/categories/(.*?)".*?src="(.*?)" alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("showContent1 match =", match)
               pic = f_xxx
               for url, pic, name in match:
                 print("Here in showContent1 name 1=", name)
                 print("Here in showContent1 url =", url)
                 name = name.replace("&amp;", "&")
                 name = name.replace("\\n", "")
                 name = "Xxxymovies-" + name
                 print("Here in showContent1 name=", name)
                 #https://www.drtuber.com/tags/18-amateur
                 url = "https://xxxymovies.com/categories/" + url
                 print("Here in showContent1 url =", url)
                 addDirectoryItem(name, url,2, pic, fanart)
               # xbmcplugin.endOfDirectory(thisPlugin)
        elif "xvideos" in name.lower():
               pic = f_search
               url = "https://www.xvideos.com/?k=searchText&p=iPage"
               addDirectoryItem("Xvideos-search", url, 100, pic, fanart)
               content = getUrl(url)
               print("In showContent1 name =", name)
               print("In showContent1 content =", content)
               regexvideo = 'li class="dyn  topcat topcat-.*?a href="(.*?)".*?">(.*?)<'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("showContent1 match =", match)
               pic = f_xxx
               for url, name in match:
                 print("Here in showContent1 name 1=", name)
                 print("Here in showContent1 url =", url)
                 name = name.replace("&amp;", "&")
                 name = name.replace("\\n", "")
                 name = "Xvideos-" + name
                 print("Here in showContent1 name=", name)
                 #https://www.xvideos.com/c/Amateur-65
                 url = "https://www.xvideos.com" + url
                 print("Here in showContent1 url =", url)
                 addDirectoryItem(name, url,2, pic, fanart)
               # xbmcplugin.endOfDirectory(thisPlugin)
        elif "xtube" in name.lower():
               pic = f_search
               url = "https://www.xtube.com/search/video/searchText/iPage"
               addDirectoryItem("Xtube-search", url, 100, pic, fanart)
               content = getUrl(url)
               print("In showContent1 name =", name)
               print("In showContent1 content =", content)
               regexvideo = '<a href="/video/(.*?)".*?img src="(.*?)" alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("showContent1 match =", match)
               pic = f_xxx
               for url, pic, name in match:
                 print("Here in showContent1 name 1=", name)
                 print("Here in showContent1 url =", url)
                 name = name.replace("&amp;", "&")
                 name = name.replace("\\n", "")
                 name = "Xtube-" + name
                 print("Here in showContent1 name=", name)
                 #https://www.xtube.com/video/amateur-gay
                 url = "https://www.xtube.com/video/" + url
                 print("Here in showContent1 url =", url)
                 addDirectoryItem(name, url,2, pic, fanart)
               # xbmcplugin.endOfDirectory(thisPlugin)
        elif "redtube" in name.lower():
               pic = f_search
               url = "https://www.redtube.com/?search=searchText"
               addDirectoryItem("Redtube-search", url, 100, pic, fanart)
               content = getUrl(url)
               print("In showContent1 name =", name)
               print("In showContent1 content =", content)
               regexvideo = 'data-category_id=.*?a href="(.*?)".*?data-src="(.*?)".*?alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("showContent1 match =", match)
               pic = f_xxx
               for url, pic, name in match:
                 print("Here in showContent1 name 1=", name)
                 print("Here in showContent1 url =", url)
                 name = name.replace("&amp;", "&")
                 name = name.replace("\\n", "")
                 name = "Redtube-" + name
                 print("Here in showContent1 name=", name)
                 url = "https://www.redtube.com" + url
                 print("Here in showContent1 url =", url)
                 addDirectoryItem(name, url,2, pic, fanart)
               # xbmcplugin.endOfDirectory(thisPlugin)
        elif "youporn" in name.lower():
               pic = f_search
               url = "https://www.youporn.com/search/?search-btn=&query=searchText"
               addDirectoryItem("Youporn-search", url, 100, pic, fanart)
               pass
        elif "empflix" in name.lower():
               pic = f_search
               url = "https://www.empflix.com/search.php?what=searchText&sb=&su=&sd=&dir=&f=&p=&category=&page=iPage&tab=videos"
               addDirectoryItem("Empflix-search", url, 100, pic, fanart)
               content = getUrl(url)
               print("empflix content A =", content)
               n1 = content.find('<div class="categories-wrapper">', 0)
               n2 = content.find('<ul class="sbMenu sbCatsMenu filtered-facets"', n1)
               content2 = content[n1:n2]
               print("empflix content2 A =", content2)
               pic = f_xxx
               regexcat = '<a href="(.*?)" title="(.*?)"'
               match = re.compile(regexcat,re.DOTALL).findall(content2)
               print("empflix match =", match)
               #https://www.empflix.com/vr-porn/?a=1&d=
               for url, name in match:
                        name = "Empflix-" + name
                        url = "https://www.empflix.com" + url
                        #pic = " "
                        print("Here in Showcontent1 url =", url)
                        addDirectoryItem(name, url,2, pic, fanart)
        # xbmcplugin.endOfDirectory(thisPlugin)
#ooooooooooooooooooooooooooooooo

def search(siteName, url):
                #home()
                pic = f_search
                print("In Search siteName, url =", siteName, url)
                siteName = siteName.lower()
                print("In Search siteName 2=", siteName)
                """
                f = open("/tmp/xbmc_search.txt", "r")
                icount = 0
                for line in f.readlines():
                    sline = line
                    icount = icount+1
                    if icount > 0:
                           break
                """
                keyb = xbmc.Keyboard()
                keyb.doModal()
                sline = keyb.getText()
                print("Here in sline =", sline)
                if "esmatube" in siteName:
                        name = sline.replace(" ", "_")
                elif "luxuretv" in siteName:
                        name = sline.replace(" ", "-")
                elif "xtube" in siteName:
                        name = sline.replace(" ", "-")
                elif "eporner" in siteName:
                        name = sline.replace(" ", "-")
                elif "pornoxo" in siteName:
                        name = sline.replace(" ", "_")
                elif "ashemaletube" in siteName:
                        name = sline.replace(" ", "_")
                elif "befuck" in siteName:
                        name = sline.replace(" ", "%20")
                elif "pornotube" in siteName:
                        name = sline.replace(" ", "%20")
                elif "pornxs" in siteName:
                        name = sline.replace(" ", "%20")
                elif "empflix" in siteName:
                        name = sline.replace(" ", "%20")
                elif "tnaflix" in siteName:
                        name = sline.replace(" ", "%20")
                elif "youjizz" in siteName:
                        name = sline.replace(" ", "%20")
                elif "tubemania" in siteName:
                        name = sline.replace(" ", "-")
                elif "femdom" in siteName:
                        name = sline.replace(" ", "%20")
                elif "flashtranny" in siteName:
                        name = sline.replace(" ", "%20")
                else:
                        name = sline.replace(" ", "+")
                print("name =", name)
                pages = [1, 2, 3, 4, 5, 6]
                for page in pages:
                        page = str(page)
                        print("In Search url =", url)
                        url = url.replace("searchText", name)
                        print("Here in search url 1=", url)
                        if "nudevista" in siteName:
                               n1 = (int(page)-1)*25
                               url = url.replace("iPage", str(n1))
                        elif "xvideos" in siteName:
                               n1 = (int(page)-1)
                               url = url.replace("iPage", str(n1))
                        else:
                               url = url.replace("iPage", page)
                        print("Here in search url 2=", url)
                        print("Here in search siteName=", siteName)
                        name = siteName + "-Page" + str(page)
                        print("Here in search name =", name)
                        name = name.replace("search-", "")
                        name = name.replace(".com", "")
                        print("Here in search name 2=", name)
                        #pic = " "
                        addDirectoryItem(name, url,3, pic, fanart)
                # xbmcplugin.endOfDirectory(thisPlugin)
#nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

def getPage(name, urlmain):
                    pic = f_xxx
                    print("In getPage name =", name)
                    print("In getPage urlmain =", urlmain)
                    pages = [1, 2, 3, 4, 5, 6]
                    #https://www.pornotube.com/orientation/straight/search/category/id/2/name/amateur/page/3
                    if "pornotube" in name.lower():
                        for page in pages:
                               n1 = urlmain.find("page", 0)
                               urlmain = urlmain[:n1]
                               url = urlmain + "/page/" + str(page)
#                               url = urlmain + str(page) + "/"
                               name = "Pornotube-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               # xbmcplugin.endOfDirectory(thisPlugin)
                    #https://hellporno.com/mom/4/
                    elif "hellporno" in name.lower():
                        for page in pages:
                               url = urlmain + str(page) + "/"
                               name = "Hellporno-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    elif "tnaflix" in name.lower():
                    #https://www.tnaflix.com/amateur-porn/4
                        for page in pages:
                               url = urlmain + "/" + str(page)
                               name = "Tnaflix-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    #https://www.youjizz.com/most-popular/4.html
                    elif "youjizz" in name.lower():
                        for page in pages:
                               url = urlmain + str(page) + ".html"
                               name = "Youjizz-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    elif "xxxymovies" in name.lower():
                    #https://xxxymovies.com/categories/amateur/4/
                        for page in pages:
                               url = urlmain + str(page) + "/"
                               name = "xxxymovies-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    #https://www.xtube.com/video/amateur-gay/4
                    elif "xtube" in name.lower():
                        for page in pages:
                               url = urlmain + "/" + str(page)
                               name = "Xtube-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    elif "xvideos" in name.lower():
                    #https://www.xvideos.com/c/Anal-12/3
                        for page in pages:
                               p1 = page-1
                               url = urlmain + "/" + str(p1)
                               name = "Xvideos-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    elif "drtuber" in name.lower():
                    #https://www.drtuber.com/tags/18-amateur/4
                        for page in pages:
                               url = urlmain + "/" + str(page)
                               name = "Drtuber-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    elif "redtube" in name.lower():
                    #https://www.redtube.com/redtube/amateur?page=4
                        for page in pages:
                               url = urlmain + "?page=" + str(page)
                               name = "Redtube-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    elif "youporn" in name.lower():
                    #https://www.youporn.com/category/2/anal/?page=4
                        for page in pages:
                               url = urlmain + "?page=" + str(page)
                               name = "Youporn-Page-" + str(page)

                               addDirectoryItem(name, url,3, pic, fanart)
         #               xbmcplugin.endOfDirectory(thisPlugin)
                    elif "empflix" in name.lower():
                    #https://www.empflix.com/amateur-porn/rated/4?d=all
                        for page in pages:
                               url = urlmain + "/rated/" + str(page) +"?d=all"
                               name = name + "-Page " + str(page)
                               addDirectoryItem(name, url,3, pic, fanart)
                    xbmcplugin.endOfDirectory(thisPlugin)
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
def getVideos(name, urlmain):
        pic = f_xxx
        items = name.split("-")
        print("In getVideos items =", items)
        name2 = items[0]
        print("In getVideos name2 =", name2)
        print("In getVideos urlmain =", urlmain)
        content = getUrl(urlmain)
        print("In getVideos name =", name)
        print("content B =", content)
        name = name.lower()
        if "pornotube" in name:
               regexvideo = 'href="/orientation/straight/video(.*?)".*?src="(.*?)".*?" alt="(.*?)"'
#             https://www.pornotube.com/orientation/straight/video/9626/title/cant-get-enough-of-sydnee-capri
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name2 + "-" + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://www.pornotube.com/orientation/straight/video" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "hellporno" in name:
               regexvideo = '<a href="https://hellporno.com/videos/(.*?)".*?title">(.*?)".*?poster="(.*?)"'
#             https://hellporno.com/videos/closeup-sex-with-mommy-in-a-smashing-home-play/
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, name, pic in match:
                 name = name2 + "-" + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://hellporno.com/videos/" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        #https://www.tnaflix.com/amateur-porn/Awesome-BDSM-Hardcore/video757493
        elif "tnaflix" in name:
               regexvideo = "data-vid=.*?data-name='(.*?)'.*?href='(.*?)'.*?data-original='(.*?)'"
#             regexvideo = 'span class="thumb_container_box short.*?thumb_container picture\' href="(.*?)" title="(.*?)".*?src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for name, url, pic in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://www.tnaflix.com" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "eporner" in name:
               regexvideo = 'mbcontent"><a href="/hd-porn/(.*?)"><img src="(.*?)".*?alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               #https://www.eporner.com/hd-porn/fJvIoiMQQzd/Mom-and-friend-s-comrade-hardcore-hd-school-girl-dominates-woman-Ashly-Anderpatron-s-son/
               for url, pic, name in match:
                 name = name2 + "-" + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://www.eporner.com/hd-porn/" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "extremetube" in name:
               regexvideo = 'div class="fullDescrBox">.*?<a href="(.*?)" title="(.*?)".*?data-thumb="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, name, pic in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        #https://www.youjizz.com/videos/pinay-sex-scandal-18739701.html
        elif "youjizz" in name:
               regexvideo = 'href="/videos/(.*?)".*?src="(.*?)".*?video-title.*?>(.*?)<'
#             regexvideo = 'span class="thumb_container_box short.*?thumb_container picture\' href="(.*?)" title="(.*?)".*?src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 pic = "https:" + pic
                 url = "https://www.youjizz.com/videos/" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "xxxymovies" in name:
               regexvideo = 'href="https\://xxxymovies.com/videos/(.*?)" title="(.*?)".*?data-original="(.*?)"'
#             regexvideo = 'span class="thumb_container_box short.*?thumb_container picture\' href="(.*?)" title="(.*?)".*?src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, name, pic in match:
                 name = name2 + "-" + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://xxxymovies.com/videos/" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "xtube" in name:
               regexvideo = '<a href="/video-watch/(.*?)" title=\'(.*?)\'.*?<img src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               #https://www.xtube.com/video-watch/look-ma-no-hands-43776071
               for url, name, pic in match:
                 name = name2 + "-" + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://www.xtube.com/video-watch/" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "xvideos" in name:
#             regexvideo = '<a href="/search-video/(.*?)" title="(.*?).*?data-src="(.*?)"'
               regexvideo = '<a href="/video(.*?)".*?data-src="(.*?).*?title="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               #https://www.xvideos.com/search-video/eAEtUMtKQ1EM_JesQ5vnSc7d1i6KRUVbQayUQqsWBEGrG_HfzaWukkxmyGR-4AEGmAHCZdX94Xn39XaqaQFDuDdOhCUMj_-9eSc3DmST4O6O4mKNuqNW5bSOEmbm3lE5nXowcq2EhbF5o6CGbiS9RaBW00KK66kefRQFWY6IWWeuRlq3QhVdm0Q4oyVFI-NahbZIxcalyeJyGZQ-bqhL2UfmJuk6Ok7vqo7OmUbFKZfsdbUcZ6py_cBZl1KfENaVxmb6fdwf3s-_b6bb-8XF_Hq1WC3n69vl9gxvK6sbGAjhCgZFWJXu8_SxO768jjHOYGAp9K6qZz1EPWtelASyTcruRNwmQgS_f3CMViQ=/d47f409df3ce9beaecc49b8d944fe562
               for url, pic, name in match:
                 name = name2 + "-" + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://www.xvideos.com/video" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "drtuber" in name:
        #https://www.drtuber.com/video/5906376/teen-18-petite-amateur-seducing-my-stepfather
               regexvideo = '<a href="/video/(.*?)".*?src="(.*?)" alt="(.*?)"'
#             regexvideo = 'span class="thumb_container_box short.*?thumb_container picture\' href="(.*?)" title="(.*?)".*?src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name2 + "-" + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://www.drtuber.com/video/" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "redtube" in name:
               #https://www.redtube.com/11395991
               regexvideo = 'span class="video_thumb_wrap.*?href = "(.*?)".*?data-src="(.*?)".*?lt="(.*?)"'
#             regexvideo = 'span class="thumb_container_box short.*?thumb_container picture\' href="(.*?)" title="(.*?)".*?src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://www.redtube.com" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "shemaletubevideos" in name:
               regexvideo = 'div class="thumb"> <a href="(.*?)" class="ha">(.*?)<.*?img src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("getVideos match 2=", match)
               for url, name, pic in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 url = url
                 #print "Here in getVideos url =", url
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "xnxx" in name:
               regexvideo = 'class="thumb-block.*?a href="(.*?)".*?data-src="(.*?)".*?title="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("getVideos match 3=", match)
               for url, pic, name in match:
                 #http://www.xnxx.com/video-8xolv4f/anal_wife
                 url = "http://www.xnxx.com" + url
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 #print "Here in getVideos url =", url
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "luxuretv" in name:
               regexvideo = '<div class="content".*?a href="(.*?)".*?><img class="img" src="(.*?)" alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("getVideos match 3=", match)
               for url, pic, name in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "hotgoo" in name:
               regexvideo = '</td><td width=160><a href="(.*?)".*?img src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("getVideos match 1=", match)
               for url, pic in match:
                 n1 = url.rfind("/")
                 name = name + url[n1:]
                 url = "http://www.hotgoo.com" + url
                 #print "Here in getVideos url =", url
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "heavy-r" in name:
               regexvideo = 'iv class="video-item compact.*?a href="(.*?)".*?img src="(.*?)".*?alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("getVideos match 2=", match)
               for url, pic, name in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 url = "http://www.heavy-r.com" + url
                 #print "Here in getVideos url =", url
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "spicytranny" in name:
               n1 = content.find('<ul class="content">', 0)
               n2 = content.find('</ul>', n1)
               content = content[n1:n2]
               regexvideo = '<li.*?ref="(.*?)".*?title="(.*?)"><img class'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("In getVideos match =", match)
               for url, name in match:
#                 if "xhamster" not in url:
#                      continue
                       name = name + name.replace('"', '')
                       name = name.replace("Page", "")
                       url = "http://www.spicytranny.com" + url
                       ##print "Here in getVideos url =", url
                       add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "esmatube" in name:
               regexvideo = '<iframe class=iframeresdif src="(.*?)".*?data-title=\'(.*?)\'.*?src=\'(.*?)\''
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, name, pic in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "pornplaying" in name:
               regexvideo = '<a href="/video/(.*?)".*?<img src="(.*?)" title="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               #http://www.pornplaying.com/video/126567/Real_Amateur_Doggystyle_Sex/
               for url, pic, name in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 url = "http://www.pornplaying.com/video/" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "XXtubeshemalesXX" in name:
               host = "http://www.tubeshemales.com"
               content = getUrl2(urlmain, host)
               print("content B2 =", content)
               regexvideo = 'data-title="(.*?)".*?data-thumbnail="(.*?)".*?u=(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for name, pic, url in match:
                 print("In tubeshemales url =", url)
                 if ("txxx" in url) or ("sunporno" in url) or ("xhamster" in url) or ("befuck" in url) or ("xtube" in url) or ("nuvid" in url) or ("pornxs" in url) or ("sheshaft" in url) or ("freeshemaletube" in url) or ("ashemaletube" in url) or ("upornia" in url):
                     name = name + name.replace('"', '')
                     name = name.replace("Page", "")
                     url = url.replace("%3A", ":")
                     url = url.replace("%2F", "/")
                     url = url.replace("%3F", "?")
                     url = url.replace("%3D", "=")
                     url = url.replace("%26", "&")
                     print("Here in getVideos url =", url)
                     add_link(name, url,3, pic, fanart)
                 else:
                     continue
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "tubeshemales" in name:
               regexvideo = 'data-title="(.*?)".*?data-thumbnail="(.*?)".*?data-item-url="(.*?)".*?data-source="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("tubeshemales match =", match)
               sources = ["txxx", "sunporno", "xhamster", "befuck", "xtube", "nuvid", "pornxs", "sheshaft", "freeshemaletube", "ashemaletube", "upornia"]
               for name, pic, url, source in match:
                 if source.lower() in sources:
                     print("In tubeshemales source 2=", source)
                     print("In tubeshemales name 2=", name)
                     url = "https://www.tubeshemales.com" + url.replace("&amp;", "&")
                     host = "https://www.tubeshemales.com"
                     content2 = getUrl2(url, urlmain)
#                 content2 = getUrl(url)
                     print("tubeshemales content2 =", content2)
                     regexvideo = 'link rel="canonical" href="(.*?)"'
                     match = re.compile(regexvideo,re.DOTALL).findall(content2)
                     url = match[0]
                     print("In tubeshemales url 2=", url)
                     name = name + name.replace('"', '')
                     name = name.replace("Page", "")
                     print("Here in getVideos url =", url)
                     add_link(name, url,3, pic, fanart)
                 else:
                     continue
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "nudevista" in name:
               regexvideo = 'add"></div><a href="(.*?)".*?<img src="(.*?)".*?</a> <b>(.*?)</b>'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "sunporno" in name:
               regexvideo = 'data-type="movie".*?href="(.*?)".*?src="(.*?)".*?title="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "jizzbunker" in name:
               regexvideo = '<li><figure>.*?href="(.*?)".*?title="(.*?)".*?data-original="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, name, pic in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "pornoxo" in name:
               regexvideo = 'data-video-id.*?a href="(.*?)".*?src="(.*?)".*?" alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 url = "https://www.pornoxo.com" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "youporn" in name:
               regexvideo = 'a href="/watch/(.*?)".*?alt=\'(.*?)\'.*?data-thumbnail="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, name, pic in match:
                 name = name + name.replace('"', '')
                 name = name.replace("Page", "")
                 url = "https://www.youporn.com/watch/" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "vporn" in name:
               regexvideo = 'div  class="video">.*?<a  href="(.*?)".*?<img src="(.*?)" alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "sheshaft" in name:
#             regexvideo = 'div class="item".*?href="(.*?)".*?title="(.*?)".*?"thumb" src="(.*?)"'
               regexvideo = 'itemtype="https://schema.org/ImageObject.*?a href="(.*?)".*?img src="(.*?)".*?alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "xvideos" in name:
               regexvideo = 'data-src="(.*?)".*?data-videoid.*?a href="(.*?)" title="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               #https://www.xvideos.com/video31410981/morther_and_son_go_trip_and_together_on_bedroom
               for pic, url, name in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "https://www.xvideos.com" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "txxx" in name:
               regexvideo = '"un-grid--thumb--content"><a href="(.*?)".*?img src="(.*?)" alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name.replace("Page", "")
                 url = url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "befuck" in name:
               regexvideo = '<div class="ic">.*?href="(.*?)" title="(.*?)".*?data-src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, name, pic in match:
                 name = name.replace("Page", "")
                 url = url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "pornxs" in name:
               n1 = content.find('<div class="content', 0)
               content = content[n1:]
               regexvideo = '<a href="(.*?)".*?img src="(.*?)" alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name.replace("Page", "")
                 url = "http://pornxs.com" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "ashemaletube" in name:
               regexvideo = '<div class="thumb-inner-wrapper.*?href="(.*?)".*?img src="(.*?)" alt="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('&#039;', '')
                 name = name.replace("Page", "")
                 url = "https://www.ashemaletube.com" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        #https://www.empflix.com/amateur-porn/Pole-dancer-in-lingerie-fucked-by-doc-in-his-office/video312774?isFeatured=0
        elif "empflix" in name:
               regexvideo = "data-vid=.*?href='(.*?)'.*?data-original='(.*?)' alt=\"(.*?)\""
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("getVideos empflix match =", match)
               for url, pic, name in match:
                 name = name + name.replace("Page", "")
                 url = "https://www.empflix.com" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,4, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "tubemania" in name:
             regexvideo = 'div class="video".*?<a href="(.*?)" title="(.*?)"><img src="(.*?)"'
             match = re.compile(regexvideo,re.DOTALL).findall(content)
             print("match =", match)
             for url, name, pic in match:
                 #https://tubemania.org/mov/3290775/
                 name = "tubemania-" + name.replace('"', '')
                 url = "https://tubemania.org" + url
                 ##print "Here in getVideos url =", url
                 add_link(name, url,3, pic, fanart)
             # xbmcplugin.endOfDirectory(thisPlugin)
        elif "femdom" in name:
               regexvideo = '<div class="img".*?<a href="(.*?)".*?ata-original="(.*?)" title="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "tranny.one" in name:
               regexvideo = '<a class="textIndent" href="(.*?)".*?<img src="(.*?)".*?video-title"><span>(.*?)<'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for url, pic, name in match:
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
#               xbmcplugin.endOfDirectory(thisPlugin)
        elif "flashtranny" in name:
               regexvideo = '<div class="b-thumb-item">.*?title="(.*?)".*?ref="(.*?)".*?<img src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               print("match =", match)
               for name, url, pic in match:
                 #http://www.flashtranny.com/gallery/162366-lascivious-curious-daddy-pounding-wicked-latin-sheboy-pretty-anal-gap
                 name = name + name.replace('&plus;', ' ')
                 name = name.replace("Page", "")
                 url = "http://www.flashtranny.com" + url
                 print("Here in getVideos url =", url)
                 add_link(name, url,3, pic, fanart)
        # xbmcplugin.endOfDirectory(thisPlugin)

#ooooooooooooooooooooooooooooo
def playVideo(name, url):
        print("Here in getVideos4 url 1=", url)
#        url = "https://www.youtube.com/watch?v=" + url
        from youtube_dl import YoutubeDL
        print("Here in getVideos4 url 2", url)
        ydl_opts = {'format': 'best'}
        ydl = YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
       # url = "https://www.youtube.com/watch?v=CSYCEyMQWQA"
        result = ydl.extract_info(url, download=False)
        print("result =", result)
        url = result["url"]
        print("Here in Test url =", url)
        play(name, url)
        return
        
def play(name, url):
           pic = icon
           print("Here in playVideo url B=", url)
           li = xbmcgui.ListItem(name,iconImage=icon, thumbnailImage=pic)
           player = xbmc.Player()
           player.play(url, li)
           return

################## tivu ##############################
def showContent11(name, url):
                content = getUrl(url)
                print("showContent1 content A =", content)
                n1 = content.find("#DESCRIPTION  ---ADULT XXX LIVE CHANNELS---", 0)
                n2 = content.find("#DESCRIPTION ---", (n1+20))
                print("showContent2 n1 =", n1)
                print("showContent2 n2 =", n2)
                content2 = content[n1:n2]
                print("showContent2 content A 2=", content2)
                regexcat = '#SERVICE.*?http(.*?)\:.*?DESCRIPTION(.*?)\n'
                match = re.compile(regexcat,re.DOTALL).findall(content2)
                print("match A=", match)
                for url, name in match:
                        print("name =", name)
                        print("url =", url)
                        url = "http" + url
                        url = url.replace("%3a",":")
                        print("url 2=", url)
                        pic = i_xxx
                        # addDirectoryItem(name, url,23, pic, fanart)
                        add_link(name, url,23, pic, fanart)                        
                        # addDirectoryItem(name, {"name":name, "url":url, "mode":4}, pic)
                # xbmcplugin.endOfDirectory(thisPlugin)
# def showContent11(name, url):
                # content = getUrl(url)
                # print("showContent1 content A =", content)
                # n1 = content.find("#DESCRIPTION  ---ADULT XXX LIVE CHANNELS---", 0)
                # content2 = content[(n1):]
                # print("showContent1 content A 2=", content2)
                # regexcat = '#DESCRIPTION ---(.*?)---'
                # match = re.compile(regexcat,re.DOTALL).findall(content2)
                # print("match A=", match)
                # # thost = 'aHR0cDovL3BhdGJ1d2ViLmNvbQ=='
                # # SS1 = base64.b64decode(thost)
                # # Host = SS1 + "/iptv/e2liste/subbouquet.tivustream_adultxxx.tv"
                # for name in match:
                        # print("name =", name)
                        # pic = i_xxx
                        # addDirectoryItem(name, url,22, pic, fanart)
                # # xbmcplugin.endOfDirectory(thisPlugin)
def showContent22(name, url):
                pic = i_xxx
                content = getUrl(url)
                print("showContent2 content A =", content)
                name = name.replace("+", " ")
                name = name.replace("%20", " ")
                text =  "#DESCRIPTION ---" + name + "---"
                print("showContent2 text =", text)
                n1 = content.find(text, 0)
                n2 = content.find("#DESCRIPTION ---", (n1+20))
                print("showContent2 n1 =", n1)
                print("showContent2 n2 =", n2)
                content2 = content[n1:n2]
                print("showContent2 content A 2=", content2)
                regexcat = '#SERVICE.*?http(.*?)\:.*?DESCRIPTION(.*?)\n'
                match = re.compile(regexcat,re.DOTALL).findall(content2)
                print("match A=", match)
                for url, name in match:
                        print("name =", name)
                        print("url =", url)
                        url = "http" + url
                        url = url.replace("%3a",":")
                        print("url 2=", url)
                        # addDirectoryItem(name, url,23, pic, fanart)
                        add_link(name, url,23, pic, fanart)                        
                        # addDirectoryItem(name, {"name":name, "url":url, "mode":4}, pic)
                # xbmcplugin.endOfDirectory(thisPlugin)

def showContent112(name, url):
                #home()
                pic = i_xxx
                content = getUrl(url)
                print("showContent112 content A =", content)
                regexcat = '.*?,(.*?)\n'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                print("match A=", match)
                for name in match:
                        url = " "
                        pic = " "
                        addDirectoryItem(name, url,200, pic, fanart)
                # xbmcplugin.endOfDirectory(thisPlugin)


def showContenttz():
        pic = t_xxx
        content = getUrl(HostThumb)
        pass#print "content A =", content
        icount = 0
        start = 0
        addDirectoryItem("Search", HostThumb, 94, pic, fanart)
        name = "Hottest"
        url = "https://www.thumbzilla.com/"
        addDirectoryItem(name, url,91, pic, fanart)
        name = "Newest"
        url = "https://www.thumbzilla.com/newest"
        addDirectoryItem(name, url,91, pic, fanart)
        name = "Trending"
        url = "https://www.thumbzilla.com/trending"
        addDirectoryItem(name, url,91, pic, fanart)
        name = "Top Videos"
        url = "https://www.thumbzilla.com/top"
        addDirectoryItem(name, url,91, pic, fanart)
        name = "Popular Videos"
        url = "https://www.thumbzilla.com/popular"
        addDirectoryItem(name, url,91, pic, fanart)
        name = "HD Videos"
        url = "https://www.thumbzilla.com/hd"
        addDirectoryItem(name, url,91, pic, fanart)
        name = "Homemade"
        url = "https://www.thumbzilla.com/homemade"
        addDirectoryItem(name, url,91, pic, fanart)
        name = "Pornstars"
        url = "https://www.thumbzilla.com/pornstars"
        addDirectoryItem(name, url,91, pic, fanart)
        i1 = 0
        if i1 == 0:
                #https://www.thumbzilla.com/categories/british
                regexcat = 'div class="checkHomepage".*?a href="/categories/(.*?)"'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                pass#print "match =", match
                for name in match:
                        url = "https://www.thumbzilla.com/categories/" + name
                        # addDirectoryItem(name, {"name":name, "url":url, "mode":91}, pic)
                        addDirectoryItem(name, url,91, pic, fanart)
        # xbmcplugin.endOfDirectory(thisPlugin)

def getVideos2(name, url):
                pass#print "In getVideos2 name =", name
                pass#print "In getVideos2 url =", url
                f = open("/tmp/xbmc_search.txt", "r")
                icount = 0
                for line in f.readlines():
                    sline = line
                    icount = icount+1
                    if icount > 0:
                           break
                name = sline.replace(" ", "+")
                #https://www.thumbzilla.com/video/search?q=mom+anal&page=4
                url = "https://www.thumbzilla.com/video/search?q=" + name
                getPage2(name, url)


def getPage2(name, urlmain):
                pages = [1, 2, 3, 4, 5, 6]
                for page in pages:
                        url = urlmain + str(page)
                        name = "Page " + str(page)
                        pic = t_xxx
                        addDirectoryItem(name, url,92, pic, fanart)
                # xbmcplugin.endOfDirectory(thisPlugin)

#https://www.thumbzilla.com/categories/british?page=4
def getPagetz(name, url):
                pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                for page in pages:
                        url = url + "?page=" + str(page)
                        name = "Page " + str(page)
                        pic = t_xxx
                        # addDirectoryItem(name, {"name":name, "url":url, "mode":92}, pic)
                        addDirectoryItem(name, url, 92, pic, fanart)                        
                # xbmcplugin.endOfDirectory(thisPlugin)

#https://www.thumbzilla.com/video/ph59e667177496c/stella-cox-seduced-by-horny-lesbian-friend
def getVideostz(name, urlmain):
    content = getUrl(urlmain)
    pass#print "content B =", content
    regexvideo = '<a class="js-thumb" href="(.*?)".*?src="(.*?)".*?<span class="title">(.*?)<.'
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    pass#print "getVideostz match =", match
    for url, pic, name in match:
         url = "https://www.thumbzilla.com" + url
         # addDirectoryItem(name, {"name":name, "url":url, "mode":93}, pic)
         # addDirectoryItem(name, url, 93, pic, fanart)
         add_link(name, url, 93, pic, fanart)
    # xbmcplugin.endOfDirectory(thisPlugin)

def playVideotz(name, url):
           pass#print "Here in playVideotz url =", url
           fpage = getUrl(url)
           pass#print "fpage C =", fpage
           regexvideo = 'a class="qualityButton active" data-quality="(.*?)"'
           match = re.compile(regexvideo,re.DOTALL).findall(fpage)
           pass#print "playVideotz match =", match
           url = match[0]
           pic = "DefaultFolder.png"
           li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
           player = xbmc.Player()
           player.play(url, li)
           # xbmcplugin.endOfDirectory(thisPlugin)


def home():
    pic = "DefaultFolder.png"
    addDirectoryItem('...[COLOR yellow]  Home  [/COLOR]...', {"name":'', "url":None, "mode":200}, pic)

# def addDirectoryItem(name, parameters={},pic=""):
    # li = xbmcgui.ListItem(name,iconImage=icon, thumbnailImage=pic)
    # url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    # return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

# def addDirectoryItem(name, parameters={},pic=""):
    # isFolder = False
    # ok = True
    # u = sys.argv[0] + "?"  + urllib.urlencode(parameters) #url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    # liz = xbmcgui.ListItem(name, iconImage = icon, thumbnailImage = pic)
    # liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":"12"})
    # liz.setProperty('fanart_image', fanart)
    # ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
    # return ok

def addDirectoryItem(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":"12"})
	liz.setProperty('fanart_image', fanart)
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok
    
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



if not sys.argv[2]:
    ok = showContent()
else:
    # print 'adult_request_password =', adult_request_password
    # if adult_request_password == "true" :
    pin = adult_password
    if pin != base64.b64decode("MjgwOA=="):
            # showContent()
            pass
    else:
        if mode == str(1):
            ok = showContent1(name, url)
        elif mode == str(2):
            ok = getPage(name, url)
        elif mode == str(3):
            ok = getVideos(name, url)
        elif mode == str(4):
            ok = playVideo(name, url)
        elif mode == str(11):
            ok = showContent11(name, url)
        elif mode == str(21):
            ok = showContentB()
        elif mode == str(22):
            ok = showContent22(name, url)
        elif mode == str(23):
            ok = play(name, url)
        elif mode == str(100):
            ok = search(name, url)
        elif mode == str(112):
           ok = showContent112(name, url)
        elif mode == str(105):
            main()
        elif mode == 101:
            search()
        elif mode == 6:
            resolve_url(url)
        elif mode == 7:
            xbmc.log("mode==7, starturl=%s" % url, xbmc.LOGERROR)
            start(url)
        elif mode == 8:
            redtube_sorting(url)
        elif mode == 9:
            redtube_categories(url)
        elif mode == 12:
            lubtetube_pornstars(url)
        elif mode == 13:
            flv_channels_list(url)
        elif mode == 14:
            porn300_categories(url)
        elif mode == 15:
            tubedupe_categories(url)
        elif mode == 16:
            vikiporn_categories(url)
        elif mode == 17:
            xhamster_categories(url)
        elif mode == 18:
            fantasti_categories(url)
        elif mode == 19:
            tubedupe_rankings(url)
        elif mode == 20:
            tubedupe_content(url)
        elif mode == 24:
            xhamster_content(url)
        elif mode == 27:
            xvideos_categories(url)
        elif mode == 28:
            youjizz_categories(url)
        elif mode == 29:
            hentaigasm_categories(url)
        elif mode == 30:
            ashemaletube_categories(url)
        elif mode == 31:
            ashemaletube_sorting(url)
        elif mode == 32:
            xvideos_pornstars(url)
        elif mode == 33:
            heavyr_categories(url)
        elif mode == 39:
            pornxs_categories(url)
        elif mode == 42:
            xhamster_rankigs(url)
        elif mode == 44:
            motherless_sorting(url)
        elif mode == 45:
            emplix_categories(url)
        elif mode == 46:
            emplix_sorting(url)
        elif mode == 48:
            fantasti_collections(url)
        elif mode == 49:
            fatasti_sorting(url)
        elif mode == 52:
            porngo_categories(url)
        elif mode == 54:
            uflash_categories(url)
        elif mode == 55:
            ashemaletube_pornstars(url)
        elif mode == 60:
            motherless_galeries_cat(url)
        elif mode == 61:
            motherless_being_watched_now(url)
        elif mode == 62:
            motherless_groups_cat(url)
        elif mode == 64:
            javbangers_categories(url)
        elif mode == 68:
            luxuretv_categories(url)
        elif mode == 71:
            xvideos_sorting(url)
        elif mode == 70:
            item = xbmcgui.ListItem(name, path = url)
            item.setMimeType('video/mp4')
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        elif mode == str(90):
            ok = showContenttz()
        elif mode == str(91):
            ok = getPagetz(name, url)
        elif mode == str(92):
            ok = getVideostz(name, url)
        elif mode == str(93):
            ok = playVideotz(name, url)
        elif mode == str(94):
            ok = getVideos2(name, url)
        elif mode == str(200):
            ok = showContent()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
