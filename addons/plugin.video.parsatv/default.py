#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, xpath, xbmc, os
if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"): # enigma2 KodiLite
    import six
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

from os import path, system
import re
import socket
import string
import sys
import time
import xbmc, xbmcplugin
import xbmcgui, xbmcaddon

PY3 = False
try:
    from urllib.request import urlopen, Request
    from urllib.parse import quote, unquote_plus, unquote, urlencode
    from urllib.parse import urlparse
    from html.entities import name2codepoint as n2cp
    import http.client
    PY3 = True; unicode = str; unichr = chr; long = int
except:
    from urllib2 import urlopen, Request
    from urllib import quote, unquote_plus, unquote, urlencode
    from urlparse import urlparse
    from htmlentitydefs import name2codepoint as n2cp
    import httplib

thisPlugin = int(sys.argv[1])
addonId = "plugin.video.parsatv"
__settings__ = xbmcaddon.Addon(addonId)
thisAddonDir = xbmc.translatePath(__settings__.getAddonInfo('path'))#.decode('utf-8')
sys.path.append(os.path.join(thisAddonDir, 'resources', 'lib'))
home = __settings__.getAddonInfo('path')
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)
fanart = xbmc.translatePath(os.path.join(home, 'fanart.png'))

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
        link=response.read()
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
        modes = []
        names.append("ParsaTV Sport")
        urls.append('http://www.parsatv.com/streams/fetch/varzeshtv.php')
        modes.append("1")
        names.append("ParsaTV Mobile")
        urls.append('https://www.parsatv.com/m/')
        modes.append("2")
        i = 0
        pic = ''
        for name in names:
            url = urls[i]
            mode = modes[i]
            i = i+1
            print('mode = ', mode)
            addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def showContent1(name, url):
        content = getUrl('http://www.parsatv.com/m/')
        items = []
        n1 = content.find('channels">', 0)
        n2 = content.find("</table>", n1)
        content = content[n1:n2]
        regexvideo = '<li><a href="(.*?)"><button.*?myButton">(.*?)</button'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        print("match =", match)
        for url, name in match:
            if 'sport' in str(url).lower():
                name1 = name.replace('%20', ' ')
                item = name + "###" + url
                items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url = item.split("###")[1]
            name = 'Sport ' + name
            pic = " "
            print("getVideos5 name =", name)
            print("getVideos5 url =", url)
            addDirectoryItem(name, {"name":name, "url":url, "mode":33}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos33(name, urlmain):
    content = getUrl(urlmain)
    print("content B =", content)
    n1 = content.find('class="myButton" id=', 0)
    n2 = content.find("</button></a>", n1)
    content = content[n1:n2]
    regexvideo = '<a href="(.*?)"><b'
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    print("getVideos match =", match)
    for url in match:
        url = url
        name = name.replace('%20', ' ')
        pic = ''
        print("getVideos15 name =", name)
        print("getVideos15 url =", url)
        addDirectoryItem(name, {"name":name, "url":url, "mode":50}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent2(name, url):
        content = getUrl('https://www.parsatv.com/m/')
        print("match content2=", content)
        items = []
        regexvideo = 'li><a href="(.*?)">.*?myButton">(.*?)</'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        print("match =", match)
        for url, name in match:
            url = url
            name = name
            pic = " "
            print("getVideos5 name =", name)
            print("getVideos5 url =", url)
            item = name + "###" + url
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url = item.split("###")[1]
            addDirectoryItem(name, {"name":name, "url":url, "mode":34}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def showContent21(name, url):
        content = getUrl('https://www.parsatv.com/m/')
        # if PY3:
            # content = six.ensure_str(content)
        print("match content2=", content)
        items = []
        n6 = content.find("<a></a></td>")
        if str(n6) in content:
            content.replace(str(n6),'<a></a></li></td>')
            print('yes is n6')
        else:
            print('no, no n6 in content!')
        regexvideo = '<tr>.*?<td id=".*?><li>(.*?)<a>.*?</td>.*?</tr>'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        print("showContent21 match =", match)
        for name in match:
            url = url
            name = name
            pic = " "
            print("getVideos5 name =", name)
            print("getVideos5 url =", url)
            item = name + "###" + url
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url = item.split("###")[1]
            addDirectoryItem(name, {"name":name, "url":url, "mode":22}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def showContent22(name, url):
        content = getUrl('https://www.parsatv.com/m/')
        print("showContent22 content=", content)
        n6 = content.find("<a></a></td>")
        if str(n6) in str(content):
            content.replace(str(n6),'<a></a></li></td>')
            print('yes is n6')
        else:
            print('no, no n6 in content!')
        s1 = str(name) + "<a></a>"                
        n1 = content.find(s1)
        n2 = content.find("<td id=", n1)
        content2 = content[n1:n2]
        print("showContent22 content2=", content2)            
        items = []
        regexvideo = 'a href="(.*?)".*?"myButton">(.*?)<'
        match = re.compile(regexvideo,re.DOTALL).findall(content2)
        print("showContent22 match =", match)
        for url, name in match:
            url = url
            name = name
            pic = " "
            print("getVideos5 name =", name)
            print("getVideos5 url =", url)
            item = name + "###" + url
            items.append(item)
        items.sort()
        for item in items:
            name = item.split("###")[0]
            url = item.split("###")[1]
            addDirectoryItem(name, {"name":name, "url":url, "mode":34}, pic)
            # add_link(name, url1, 33, pic, fanart)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos34(name, urlmain):
    content = getUrl(urlmain)
    # if PY3:
        # content = six.ensure_str(content)
    print("content B =", content)
    n1 = content.find('class="myButton" id=', 0)
    n2 = content.find("</button></a>", n1)
    content = content[n1:n2]
    regexvideo = '<a href="(.*?)"><b'
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    print("getVideos match =", match)
    for url in match:
        url = url
        name = name.replace('%20',' ')
        pic = ''
        print("getVideos15 name =", name)
        print("getVideos15 url =", url)
        addDirectoryItem(name, {"name":name, "url":url, "mode":50}, pic)
        # add_link(name, url, 50, pic, fanart)
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


def add_link(name, url, mode, iconimage, fanart):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name) + "&iconimage=" + quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(label=name)    
    liz.setInfo('video', {'title': name,'genre': genre,'mediatype': 'video'})
    liz.setArt({'thumb': iconimage, 'icon': iconimage, 'fanart': fanart})
    try:
        liz.setContentLookup(False)
    except:
        pass
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)
    return ok

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
        ok = showContent1(name, url)
    elif mode == str(2):
        ok = showContent21(name, url)
    elif mode == str(22):
        ok = showContent22(name, url)
    elif mode == str(33):
        ok = getVideos33(name, url)
    elif mode == str(34):
        ok = getVideos34(name, url)
    elif mode == str(50):
        ok = playVideo(name, url)


