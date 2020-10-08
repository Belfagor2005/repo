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
import xbmc, xbmcplugin, xbmcaddon
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
addonId = "plugin.video.altadefinizione01"


__settings__ = xbmcaddon.Addon(addonId)
thisAddonDir = xbmc.translatePath(__settings__.getAddonInfo('path')).decode('utf-8')
# sys.path.append(os.path.join(thisAddonDir, 'resources', 'lib'))
home = __settings__.getAddonInfo('path')

dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
i_free = xbmc.translatePath(os.path.join(home, 'icon.png'))
Host = "https://www.altadefinizione01.photo/"

def getUrl(url):
    pass#print "Here in getUrl url =", url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def getrealUrl(url):
    pass#print "Here in getUrl url =", url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.geturl()
    response.close()
    return link

def showContent():
                names = []
                urls = []
                modes = []
                names.append("Cinema")
                urls.append('https://www.altadefinizione01.photo/cinema/')
                modes.append("11")
                # name = "Cinema"
                # url = "https://www.altadefinizione01.photo/cinema/"
                # pic = " "
                # addDirectoryItem(name, {"name":name, "url":url, "mode":11}, pic)
                # xbmcplugin.endOfDirectory(thisPlugin)
                names.append("Last Movie")
                urls.append('https://www.altadefinizione01.photo/find/2020/')
                modes.append("6")                
                # name = "Last Movie"
                # url = "https://www.altadefinizione01.photo/find/2020/"
                # pic = " "
                # addDirectoryItem(name, {"name":name, "url":url, "mode":5}, pic)
                # xbmcplugin.endOfDirectory(thisPlugin)
                
                i = 0
                pic = i_free
                for name in names:
                    url = urls[i]
                    mode = modes[i]
                    i = i+1
                    # addDirectoryItem(name, url, mode, pic, fanart)
                    addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
                # pass
                xbmcplugin.endOfDirectory(thisPlugin)
                
def getPage(name, url):
                #https://www.altadefinizione01.photo/cinema/page/2/
                pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                url = 'https://www.altadefinizione01.photo/page/'
                for page in pages:
#                    if str(page) == "1":
#                        url1 = url
#                    else:
                    url = url + str(page) #+ "/"
                    name = "Page " + str(page)
                    pic = " "
                    addDirectoryItem(name, {"name":name, "url":url, "mode":1}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name1, urlmain):
    content = getUrl(urlmain)
    pass#print "content B =", content
    """
    n1 = content.find('iv class="container main">', 0)
    n2 = content.find("</ul>", n1)
    content = content[n1:n2]
    pass#print "getVideos content B 2=", content
    """
    regexvideo = '<div class="cover boxcaption">.*?<h2> <a href="(.*?)".*?data-src="(.*?)".*?alt="(.*?)".*?<li><span class="ml-label">(.*?)<'
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    pass#print "getVideos match =", match
    for url, pic, name,  year in match:
             #https://www.altadefinizione01.tel/uploads/thumb/203x293-0-70/2017-11/1511644542_gli-eroi-del-natale.jpg
             pic = "https://www.altadefinizione01.photo" + pic
             name = name + "(" + year + ")"
             addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def getVideos2(name1, urlmain):
    content = getUrl(urlmain)
    pass#print "getVideos2 content =", content
    regexvideo = 'a href="#" data-link="(.*?)".*?alt.*?>(.*?)<'
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    pass#print "In getVideos2 match =", match
    for url, name in match:
         pic = " "
         if url.startswith("//"):
                 url = "https:" + url
         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def findurl(url):
            content = getUrl(url)
            pass#print "content findurl =", content
            regexvideo = '<table class="linknfo">.*?href="(.*?)"'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            pass#print "In getVideos2 match =", match
            url = match[0]
            n1 = url.find("/f/", 0)
            n2 = url.find("/", (n1+5))
            url = url[:n2]
            url = url.replace("/f/", "/embed/")
            return url

def getVideos3(name, urlmain):
        content = getUrl(urlmain)
        pass#print "getVideos3 content =", content
        regexvideo = 'id="filename".*?a href="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "getVideos3 match =", match
        url = match[0]
        pass#print "getVideos3 url =", url
        import urlresolver
        url = urlresolver.HostedMediaFile(url=url).resolve()
        pic = "DefaultFolder.png"
        pass#print "Here in playVideo url B=", url
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
        player = xbmc.Player()
        player.play(url, li)

def playVideo(name, url):
        pass#print "Here in playVideo url A=", url
        import urlresolver
        url = urlresolver.HostedMediaFile(url=url).resolve()
        pic = "DefaultFolder.png"
        pass#print "Here in playVideo url B=", url
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
        player = xbmc.Player()
        player.play(url, li)

def playVideo2(name, url):
        pic = "DefaultFolder.png"
        pass#print "Here in playVideo url B=", url
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
        player = xbmc.Player()
        player.play(url, li)


########################################################
def showContent2(name, url):
        content = getUrl(url)
        pass#print "content =", content
        """
        n1 = content.find('>Film per Genere<', 0)
        n2 = content.find("</ul>", n1)
        content = content[n1:n2]
        pass#print "content B =", content
        """
        # regexvideo = '<option value="/category/hd-alta-definizione(.*?)">(.*?)<'
        regexvideo = '<div class="cover boxcaption">.*?<h2> <a href="(.*?)".*?data-src="(.*?)".*?alt="(.*?)".*?<li><span class="ml-label">(.*?)<'        
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        i1 = 0
        pass#print "In showContent match =", match
        #https://www.guardarefilm.live/film-streaming-hd/
        # for url, name in match:
              # if i1<3:
                        # i1 = i1+1
                        # continue
              # pic = " "
              # url1 = 'https://www.altadefinizione01.photo/find/2020/' + url
              # i1 = i1+1
              # addDirectoryItem(name, {"name":name, "url":url1, "mode":6}, pic)
        # xbmcplugin.endOfDirectory(thisPlugin)
# #http://www.italia-film.online/category/film-avventura/page/3/
        for url, pic, name,  year in match:
             #https://www.altadefinizione01.tel/uploads/thumb/203x293-0-70/2017-11/1511644542_gli-eroi-del-natale.jpg
             pic = "https://www.altadefinizione01.photo" + pic
             name = name + "(" + year + ")"
             addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getPage2(name, url):
                pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                for page in pages:
                    # if str(page) == "1":
                        # url1 = url
                    # else:
                        # url1 = url + "page/" + str(page) + "/"
                    url1 = url + "page/" + str(page) + "/"
                    name = "Page " + str(page)
                    pic = " "
                    addDirectoryItem(name, {"name":name, "url":url1, "mode":5}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos4(name1, urlmain):
        pass#print "getVideos4 urlmain =", urlmain
        content = getUrl(urlmain)
        pass#print "getVideos4 content B =", content
    #   regexvideo = '<h3 class="entry-title"><a href="(.*?)".*?bookmark">(.*?)<.*?img src="(.*?)"'
        regexvideo = 'div class="span4.*?href="(.*?)".*?img src="(.*?)".*?<h1>(.*?)</h1>'
    #   https://www.guardarefilm.live/uploads/thumb/150x206-0-70/2017-08/1502327838_alta-infedelta.jpg
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "getVideos4 match =", match
        for url, pic, name in match:
#                 pic = " "
             addDirectoryItem(name, {"name":name, "url":url, "mode":8}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def getVideos5(name1, urlmain):
        content = getUrl(urlmain)
        pass#print "content B =", content
        n1 = content.find('strong>Streaming:', 0)
        n2 = content.find("strong>Download", n1)
        content = content[n1:n2]
        pass#print "content B =", content
        regexvideo = '<td><a href="(.*?)".*?noreferrer">(.*?)<'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "getVideos5 match =", match
        for url, name in match:
                 pic = " "
                 if "swzz.xyz/link" in url:
                         url = findurl(url)
                         pass#print "Here in playVideo url A=", url
                 name = url
                 print "getVideos5 name =", name
                 print "getVideos5 url =", url
                 if (not "streamango" in name.lower()) and (not "speedvideo" in name.lower()) and (not "www.nowvideo.li" in url.lower()) and (not "ok.ru" in url.lower()) and (not "rapidvideo" in url.lower()):
                         continue
                 if url.startswith("//"):
                         url1 = "http:" + url
                 else:
                         url1 = url
                 # addDirectoryItem(name, {"name":name, "url":url1, "mode":4}, pic)
                 add_link(name, url1, 4, pic, fanart)
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
    if mode == str(11):
        ok = getPage(name, url)
    elif mode == str(1):
        ok = getVideos(name, url)

    elif mode == str(2):
        ok = getVideos2(name, url)

    elif mode == str(3):
        ok = playVideo(name, url)
    elif mode == str(9):
        ok = playVideo2(name, url)

################################################
    elif mode == str(5):
        ok = showContent2(name, url)
    elif mode == str(6):
        ok = getPage2(name, url)
    elif mode == str(7):
        ok = getVideos4(name, url)
    elif mode == str(8):
        ok = getVideos5(name, url)



