#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, xpath, xbmc,os
libs = sys.argv[0].replace("default.py", "resources/lib")
if os.path.exists(libs):
   sys.path.append(libs)
print("dclip Here in default-py sys.argv =", sys.argv)
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
print("dclip Here in default-py sys.argv B=", sys.argv)



import xbmc,xbmcplugin, xbmcaddon
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
addonId = "plugin.video.tvitalia"
__settings__ = xbmcaddon.Addon(addonId)
thisAddonDir = xbmc.translatePath(__settings__.getAddonInfo('path')).decode('utf-8')
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(thisAddonDir, 'icon.png'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)


vidpc = xbmc.translatePath(os.path.join(home, 'vid.txt'))
vide2 = "/tmp/vid.txt"         

# thisPlugin = int(sys.argv[1])
# addonId = "plugin.video.tvitalia"
# dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
# if not path.exists(dataPath):
       # cmd = "mkdir -p " + dataPath
       # system(cmd)


def getUrl(url):
   print(" Here in getUrl url =", url)
   req = urllib2.Request(url)
   req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
   response = urllib2.urlopen(req)
   link=response.read()
   response.close()
   return link

def getUrl2(url, referer):
   print(" Here in getUrl2 url =", url)
   req = urllib2.Request(url)
   req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
   req.add_header('Referer', referer)
   response = urllib2.urlopen(req)
   link=response.read()
   response.close()
   return link

def showContent():
                names = []
                urls = []
                modes = []

                names.append("Paesi")
                urls.append("https://www.tvdream.net/web-tv/paesi/")
                modes.append("41")
                names.append("Italia")
                urls.append("https://www.tvdream.net/web-tv/paesi/italia/")
                modes.append("21")
                names.append("Regioni")
                urls.append("https://www.tvdream.net/web-tv/regioni/")
                modes.append("11")
                names.append("VOD")
                urls.append("https://www.raiplay.it/")
                modes.append("31")
                i = 0
                for name in names:
                        pic = icon
                        url = urls[i]
                        mode = modes[i]
                        i = i+1
                        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

##########################################################
def showContent10(name, urlmain):
        content = getUrl(urlmain)
#        print "content A =", content
        icount = 0
        start = 0
        n1 = content.find('<ul class="menu-sub">"', start)
        if n1<0:
            return
        n2 = content.find("</ul>", n1)
        content = content[n1:n2]
        print("content A2 =", content)
        pic = " "
        regexcat = 'href="(.*?)">(.*?)<'
        match = re.compile(regexcat,re.DOTALL).findall(content)
        for url, name in match:
                addDirectoryItem(name, {"name":name, "url":url, "mode":11}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)


def showContent11(name, urlmain):
        content = getUrl(urlmain)
#        print "content A =", content  #paesi
        icount = 0
        start = 0
        n1 = content.find('menu-sub">', start)
        if n1<0:
                return
        n2 = content.find("</ul>", n1)
        content = content[n1:n2]
        print("content A2 =", content)
        pic = " "
        regexcat = 'href="(.*?)">(.*?)<'
        match = re.compile(regexcat,re.DOTALL).findall(content)
        for url, name in match:
                addDirectoryItem(name, {"name":name, "url":url, "mode":12}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)


def showContent12(name, url):
                pages = [1, 2]
                for page in pages:
                        url1 = url + "page/" + str(page) + "/"
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":13}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def showContent13(name1, urlmain):
        content = getUrl(urlmain)
        print(" content B =", content)

        regexvideo = '<div class="item-head.*?href="(.*?)".*?bookmark">(.*?)<'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        print(" match =", match)
        for url, name in match:
            pic = " "
            addDirectoryItem(name, {"name":name, "url":url, "mode":14}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def playVideo14(name, urlmain):
        content = getUrl(urlmain)
        print(" content B =", content)

        regexvideo = '<iframe src="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        print(" match =", match)
        url = match[0]
        content2 = getUrl(url)
        print(" content2 =", content2)
        regexvideo2 = 'sources:.*?src.*?"(.*?)"'
        match2 = re.compile(regexvideo2,re.DOTALL).findall(content2)
        print(" match2 =", match2)
        url2 = match2[0]
        pic = "DefaultFolder.png"
        print(" Here in playVideo url2 =", url2)
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
        player = xbmc.Player()
        player.play(url2, li)
##########################################################

def showContent21(name, url):
                np = 28
                page = 1
                while page < np:
                        url1 = url + "page/" + str(page) + "/"
                        name = "Page " + str(page)
                        pic = " "
                        page = page+1
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":22}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)



def showContent22(name, url):
        content = getUrl(url)
        print("showContent2 content =", content)

        pic = " "
        regexcat = '<div class="item-head.*?a href="(.*?)".*?bookmark">(.*?)<'
        match = re.compile(regexcat,re.DOTALL).findall(content)
        print("showContent2 match =", match)

        for url, name in match:
                if ("rai" in url.lower()) or ("rai" in name.lower()):
                       mode = 23
                else:
                       mode = 24
                addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def showContent23(name, urlmain):
        content = getUrl(urlmain)
        print("getVideos content =", content)

        pic = " "
        regexcat = '"player".*?href="(.*?)"'
        match = re.compile(regexcat,re.DOTALL).findall(content)
        print("getVideos match =", match)

        url2 = match[0]
        content2 = getUrl(url2)
        print("getVideos content2 =", content2)
        regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
        match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
        print("getVideos match2 =", match2)
        url3 = match2[0]
        play(name, url3)

def showContent24(name, urlmain):
        content = getUrl(urlmain)
        print("getVideos2 content =", content)

        regexcat = '"player".*?href="(.*?)"'
        match = re.compile(regexcat,re.DOTALL).findall(content)
        print("getVideos2 match =", match)

        url2 = match[0]
        content2 = getUrl(url2)
        print("getVideos2 content2 =", content2)

        n1 = content2.find(".m3u8")
        n2 = content2.rfind("http", 0, n1)
        url3 = content2[n2:(n1+5)]
        print("getVideos2 url3 =", url3)

        play(name, url3)

def play(name, urlmain):
        pic = "DefaultFolder.png"
        print(" Here in playVideo urlmain =", urlmain)
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
        player = xbmc.Player()
        player.play(urlmain, li)

def showContent41(name, url):
                names = []
                urls = []
                modes = []
                names.append("Albania")
                urls.append("https://www.tvdream.net/web-tv/paesi/albania/")
                modes.append("21")
                names.append("Argentina")
                urls.append("https://www.tvdream.net/web-tv/paesi/argentina/")
                modes.append("21")
                names.append("Bangladesh")
                urls.append("https://www.tvdream.net/web-tv/paesi/bangladesh/")
                modes.append("21")
                names.append("Bulgaria")
                urls.append("https://www.tvdream.net/web-tv/paesi/bulgaria/")
                modes.append("21")
                names.append("Canada")
                urls.append("https://www.tvdream.net/web-tv/paesi/canada/")
                modes.append("21")
                names.append("Cina")
                urls.append("https://www.tvdream.net/web-tv/paesi/cina/")
                modes.append("21")
                names.append("Corea del Sud")
                urls.append("https://www.tvdream.net/web-tv/paesi/corea-del-sud/")
                modes.append("21")
                names.append("Croazia")
                urls.append("https://www.tvdream.net/web-tv/paesi/croazia/")
                modes.append("21")
                names.append("Francia")
                urls.append("https://www.tvdream.net/web-tv/paesi/francia/")
                modes.append("21")
                names.append("Germania")
                urls.append("https://www.tvdream.net/web-tv/paesi/germania/")
                modes.append("21")
                names.append("Giappone")
                urls.append("https://www.tvdream.net/web-tv/paesi/giappone/")
                modes.append("21")
                names.append("Grecia")
                urls.append("https://www.tvdream.net/web-tv/paesi/grecia/")
                modes.append("21")
                names.append("Italia")
                urls.append("https://www.tvdream.net/web-tv/paesi/italia/")
                modes.append("21")
                names.append("Malta")
                urls.append("https://www.tvdream.net/web-tv/paesi/malta/")
                modes.append("21")
                names.append("Nigeria")
                urls.append("https://www.tvdream.net/web-tv/paesi/nigeria/")
                modes.append("21")
                names.append("Olanda")
                urls.append("https://www.tvdream.net/web-tv/paesi/olanda/")
                modes.append("21")
                names.append("Polonia")
                urls.append("https://www.tvdream.net/web-tv/paesi/polonia/")
                modes.append("21")
                names.append("Portogallo")
                urls.append("https://www.tvdream.net/web-tv/paesi/portogallo/")
                modes.append("21")
                names.append("Qatar")
                urls.append("https://www.tvdream.net/web-tv/paesi/qatar/")
                modes.append("21")
                names.append("Regno Unito")
                urls.append("https://www.tvdream.net/web-tv/paesi/regno-unito/")
                modes.append("21")
                names.append("Romania")
                urls.append("https://www.tvdream.net/web-tv/paesi/romania/")
                modes.append("21")
                names.append("Russia")
                urls.append("https://www.tvdream.net/web-tv/paesi/russia/")
                modes.append("21")
                names.append("Slovacchia")
                urls.append("https://www.tvdream.net/web-tv/paesi/slovacchia/")
                modes.append("21")
                names.append("Spagna")
                urls.append("https://www.tvdream.net/web-tv/paesi/spagna/")
                modes.append("21")
                names.append("Svezia")
                urls.append("https://www.tvdream.net/web-tv/paesi/svezia/")
                modes.append("21")
                names.append("Svizzera")
                urls.append("https://www.tvdream.net/web-tv/paesi/svizzera/")
                modes.append("21")
                names.append("Turchia")
                urls.append("https://www.tvdream.net/web-tv/paesi/turchia/")
                modes.append("21")
                names.append("Ucraina")
                urls.append("https://www.tvdream.net/web-tv/paesi/ucraina/")
                modes.append("21")
                names.append("Ungheria")
                urls.append("https://www.tvdream.net/web-tv/paesi/ungheria/")
                modes.append("21")
                names.append("USA")
                urls.append("https://www.tvdream.net/web-tv/paesi/usa/")
                modes.append("21")
                names.append("Venezuela")
                urls.append("https://www.tvdream.net/web-tv/paesi/venezuela/")
                modes.append("21")
                pic = " "
                i = 0
                for name in names:
                        url = urls[i]
                        mode = modes[i]
                        i = i+1
                        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)





##########################################################
def showContent31(name, url):
                names = []
                urls = []
                modes = []
                names.append("Rai")
#                urls.append("https://www.raiplay.it/fiction/")
                urls.append("https://www.raiplay.it/")
                modes.append("32")
                names.append("Mediaset")
                urls.append("https://www.mediasetplay.mediaset.it/")
                modes.append("321")
                pic = " "
                i = 0
                for name in names:
                        url = urls[i]
                        mode = modes[i]
                        i = i+1
                        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def showContent32(name, url):
        content = getUrl(url)
        print("showContent2 content =", content)
        #card-item cell"
        regexcat = 'card-list__title">(.*?)<'
#        regexcat = 'data-video-json="(.*?)"'
        match = re.compile(regexcat,re.DOTALL).findall(content)
        print("showContent2 match =", match)
        for name in match:
                pic = " "
                addDirectoryItem(name, {"name":name, "url":url, "mode":33}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)


def showContent33(name, url):
        print("showContent3 name =", name)
        print("showContent3 url =", url)
        content = getUrl(url)
        print("showContent3 content =", content)
        name = name.replace("+", " ")
        n1 = content.find(name)
#        n2 = content.find("card-list__title", n1)
        n2 = content.find("card-list__title", n1)
        if n2 == -1:
                n2 = len(content)
        print("showContent3 n1, n2 =", n1, n2)
        content2 = content[n1:n2]
        print("showContent3 content2 =", content2)

        pic = " "
        regexcat = '<a aria-label=.*?href="(.*?)"'
        match = re.compile(regexcat,re.DOTALL).findall(content2)
        print("showContent2 match =", match)
        if match == []:
                regexcat = 'data-type="video".*?a href="(.*?)"'
                match = re.compile(regexcat,re.DOTALL).findall(content2)
                print("showContent2 match 2=", match)
                for url in match:
                        name = url
                        url1 = "https://www.raiplay.it" + url
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":34}, pic)
        else:
                for url in match:
                        name = url
                        url1 = "https://www.raiplay.it" + url
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":34}, pic)

        xbmcplugin.endOfDirectory(thisPlugin)

def playVideo34(name, url):
        print("In playVideo2 url =", url)
        vidurl  = vidpc 
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/KodiLite'):
            vidurl = vide2
        cmd = "python '/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/__main__.py' --no-check-certificate --skip-download -f best --get-url '" + url + "' > " + vidurl # /tmp/vid.txt"
        print("In playVideo2 cmd =", cmd)            
        if os.path.exists(vidurl):
            os.remove(vidurl)
           # if os.path.exists("/tmp/vid.txt"):
               # os.remove("/tmp/vid.txt")
           # os.system(cmd)
           # vidurl = "/tmp/vid.txt"
           if not os.path.exists(vidurl):
              os.system("sleep 5")
              play(name, vidurl)
           else:
              play(name, vidurl)
#######################
def showContent321(name, url):
        names = []
        urls = []
        modes = []
        names.append("Programmitv")
        urls.append("https://www.mediasetplay.mediaset.it/programmitv")
        modes.append("3211")
        # names.append("Film")
        # urls.append("https://www.mediasetplay.mediaset.it/film")
        # modes.append("")
        # names.append("Family")
        # urls.append("https://www.mediasetplay.mediaset.it/family")
        # modes.append("")
        # names.append("Fiction")
        # urls.append("https://www.mediasetplay.mediaset.it/fiction")
        # modes.append("")
        # names.append("Kids")
        # urls.append("https://www.mediasetplay.mediaset.it/kids")
        # modes.append("")
        # names.append("Documentari")
        # urls.append("https://www.mediasetplay.mediaset.it/documentari")
        # modes.append("")        
        content = getUrl(url)
        print("showContent321 content =", content)
        #card-item cell"
        regexcat = '"><a href="/video(.*?)"'
        match = re.compile(regexcat,re.DOTALL).findall(content)
        print("showContent2 match =", match)
        for url in match:
                pic = " "
                name = url
                url1 = "https://www.mediasetplay.mediaset.it/video" + url
                addDirectoryItem(name, {"name":name, "url":url1, "mode":34}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)



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


    if mode == str(11):
            ok = showContent11(name, url)

    elif mode == str(10):
            ok = showContent10(name, url)
    elif mode == str(12):
            ok = showContent12(name, url)
    elif mode == str(13):
            ok = showContent13(name, url)
    elif mode == str(14):
            ok = playVideo14(name, url)

    elif mode == str(21):
            ok = showContent21(name, url)
    elif mode == str(22):
            ok = showContent22(name, url)
    elif mode == str(23):
            ok = showContent23(name, url)
    elif mode == str(24):
            ok = showContent24(name, url)

    elif mode == str(31):
            ok = showContent31(name, url)
    elif mode == str(32):
            ok = showContent32(name, url)

    elif mode == str(321):
            ok = showContent321(name, url)
    elif mode == str(33):
            ok = showContent33(name, url)
    elif mode == str(41):
            ok = showContent41(name, url)
    elif mode == str(45):
            ok = showContent45(name, url)     
    elif mode == str(46):
            ok = showContent46(name, url)    
    elif mode == str(47):
            ok = showContent47(name, url)                
    elif mode == str(34):
            ok = playVideo34(name, url)