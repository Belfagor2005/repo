#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xpath
import xbmc
import os

if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/KodiLite'):
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


from os import path, system
import xbmcplugin, xbmcaddon
import xbmcgui
import time
import re
import socket
import six
PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import quote, unquote_plus, unquote, urlencode
    from urllib.request import urlretrieve
    from urllib.parse import urlparse
    from html.entities import name2codepoint as n2cp
    import http.client
    from urllib.parse import parse_qs
else:
    from urlparse import parse_qs
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urllib import quote, unquote_plus, unquote, urlencode
    from urllib import urlretrieve
    from urlparse import urlparse
    from htmlentitydefs import name2codepoint as n2cp
    import httplib



thisPlugin = int(sys.argv[1])
addonId = "plugin.video.tvitalia"
__settings__ = xbmcaddon.Addon(addonId)
thisAddonDir = xbmc.translatePath(__settings__.getAddonInfo('path'))#.decode('utf-8')
icon = xbmc.translatePath(os.path.join(thisAddonDir, 'icon.png'))
fanart = xbmc.translatePath(os.path.join(thisAddonDir, 'fanart.jpg'))
main = xbmc.translatePath(os.path.join(thisAddonDir, '__main__.py')) 

dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
    cmd = "mkdir -p " + dataPath
    system(cmd)

vidpc = xbmc.translatePath(os.path.join(thisAddonDir, 'vid.txt'))
vide2 = "/tmp/vid.txt"



def decodeUrl(text):
	text = text.replace('%20',' ')
	text = text.replace('%21','!')
	text = text.replace('%22','"')
	text = text.replace('%23','&')
	text = text.replace('%24','$')
	text = text.replace('%25','%')
	text = text.replace('%26','&')
	text = text.replace('%2B','+')
	text = text.replace('%2F','/')
	text = text.replace('%3A',':')
	text = text.replace('%3B',';')
	text = text.replace('%3D','=')
	text = text.replace('&#x3D;','=')
	text = text.replace('%3F','?')
	text = text.replace('%40','@')
	return text

def decodeHtml(text):
	text = text.replace('&auml;','ä')
	text = text.replace('\u00e4','ä')
	text = text.replace('&#228;','ä')
	text = text.replace('&oacute;','ó')
	text = text.replace('&eacute;','e')
	text = text.replace('&aacute;','a')
	text = text.replace('&ntilde;','n')

	text = text.replace('&Auml;','Ä')
	text = text.replace('\u00c4','Ä')
	text = text.replace('&#196;','Ä')
	
	text = text.replace('&ouml;','ö')
	text = text.replace('\u00f6','ö')
	text = text.replace('&#246;','ö')
	
	text = text.replace('&ouml;','Ö')
	text = text.replace('\u00d6','Ö')
	text = text.replace('&#214;','Ö')
	
	text = text.replace('&uuml;','ü')
	text = text.replace('\u00fc','ü')
	text = text.replace('&#252;','ü')
	
	text = text.replace('&Uuml;','Ü')
	text = text.replace('\u00dc','Ü')
	text = text.replace('&#220;','Ü')
	
	text = text.replace('&szlig;','ß')
	text = text.replace('\u00df','ß')
	text = text.replace('&#223;','ß')
	
	text = text.replace('&amp;','&')
	text = text.replace('&quot;','\"')
	text = text.replace('&quot_','\"')

	text = text.replace('&gt;','>')
	text = text.replace('&apos;',"'")
	text = text.replace('&acute;','\'')
	text = text.replace('&ndash;','-')
	text = text.replace('&bdquo;','"')
	text = text.replace('&rdquo;','"')
	text = text.replace('&ldquo;','"')
	text = text.replace('&lsquo;','\'')
	text = text.replace('&rsquo;','\'')
	text = text.replace('&#034;','\'')
	text = text.replace('&#038;','&')
	text = text.replace('&#039;','\'')
	text = text.replace('&#39;','\'')
	text = text.replace('&#160;',' ')
	text = text.replace('\u00a0',' ')
	text = text.replace('&#174;','')
	text = text.replace('&#225;','a')
	text = text.replace('&#233;','e')
	text = text.replace('&#243;','o')
	text = text.replace('&#8211;',"-")
	text = text.replace('\u2013',"-")
	text = text.replace('&#8216;',"'")
	text = text.replace('&#8217;',"'")
	text = text.replace('#8217;',"'")
	text = text.replace('&#8220;',"'")
	text = text.replace('&#8221;','"')
	text = text.replace('&#8222;',',')
	text = text.replace('&#x27;',"'")
	text = text.replace('&#8230;','...')
	text = text.replace('\u2026','...')
	text = text.replace('&#41;',')')
	text = text.replace('&lowbar;','_')
	text = text.replace('&rsquo;','\'')
	text = text.replace('&lpar;','(')
	text = text.replace('&rpar;',')')
	text = text.replace('&comma;',',')
	text = text.replace('&period;','.')
	text = text.replace('&plus;','+')
	text = text.replace('&num;','#')
	text = text.replace('&excl;','!')
	text = text.replace('&#039','\'')
	text = text.replace('&semi;','')
	text = text.replace('&lbrack;','[')
	text = text.replace('&rsqb;',']')
	text = text.replace('&nbsp;','')
	text = text.replace('&#133;','')
	text = text.replace('&#4','')
	text = text.replace('&#40;','')

	text = text.replace('&atilde;',"'")
	text = text.replace('&colon;',':')
	text = text.replace('&sol;','/')
	text = text.replace('&percnt;','%')
	text = text.replace('&commmat;',' ')
	text = text.replace('&#58;',':')

	return text	

# def getUrl(url):
   # print(" Here in getUrl url =", url)
   # req = Request(url)
   # req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
   # response = urlopen(req)
   # link=response.read()
   # response.close()
   # return link             
# def getUrl2(url, referer):
   # print(" Here in getUrl2 url =", url)
   # req = Request(url)
   # req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
   # req.add_header('Referer', referer)
   # response = urlopen(req)
   # link=response.read()
   # response.close()
   # return link
   
def getUrl(url):
        print( "Here in getUrl url =", url)
        try:
            req = Request(url)
        except:
            req = Request(url)       
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
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
            link=response.read()
            response.close()
            return link

def getUrl2(url, referer):
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
            response = urlopen(req)
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
    # print "showContent10 =", content
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
    # print "showContent11 =", content  #paesi
    icount = 0
    start = 0
    pic = " "        
    n1 = content.find('menu-sub">', start)
    if n1<0:
        return
    n2 = content.find("</ul>", n1)
    content = content[n1:n2]
    print("content A2 =", content)
    regexcat = 'href="(.*?)">(.*?)<'
    match = re.compile(regexcat,re.DOTALL).findall(content)
    for url, name in match:
        addDirectoryItem(name, {"name":name, "url":url, "mode":12}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent12(name, url):
    pages = [1, 2]
    pic = " "        
    for page in pages:
        url1 = url + "page/" + str(page) + "/"
        name = "Page " + str(page)
        addDirectoryItem(name, {"name":name, "url":url1, "mode":13}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent13(name1, urlmain):
    content = getUrl(urlmain)
    print(" content B =", content)
    pic = " "
    regexvideo = '<div class="item__.*?href="(.*?)".*?alt="(.*?)"'
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    print(" match =", match)
    for url, name in match:
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
    print(" content2b =", content2)
    regexvideo2 = 'sources:.*?src.*?"(.*?)"'
    match2 = re.compile(regexvideo2,re.DOTALL).findall(content2)
    print(" match2 =", match2)
    url2 = match2[0]
    pic = "DefaultFolder.png"
    print(" Here in playVideob url2 =", url2)
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    player = xbmc.Player()
    player.play(url2, li)
##########################################################

def showContent21(name, url):
    np = 28
    page = 1
    pic = " "    
    while page < np:
        url1 = url + "page/" + str(page) + "/"
        name = "Page " + str(page)
        page = page+1
        addDirectoryItem(name, {"name":name, "url":url1, "mode":22}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent22(name, url):
    content = getUrl(url)
    if PY3:        
            content = six.ensure_str(content)    
    print("showContent2 content =", content)
    pic = " "
    regexcat = '<div class="item__.*?href="(.*?)".*?alt="(.*?)"'
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
    if PY3:        
            content = six.ensure_str(content)    
    print("getVideos content =", content)
    pic = " "
    regexcat = '"player".*?href="(.*?)"'
    match = re.compile(regexcat,re.DOTALL).findall(content)
    print("getVideos match =", match)
    url2 = match[0]
    content2 = getUrl(url2)
    if PY3:        
            content2 = six.ensure_str(content2)    
    print("getVideos content2 =", content2)
    regexcat2 = 'liveVideo":{"mediaUrl":"(.*?)"'
    match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
    print("getVideos match2 =", match2)
    url3 = match2[0]
    play(name, url3)

def showContent24(name, urlmain):
    content = getUrl(urlmain)
    if PY3:        
            content = six.ensure_str(content)    
    print("getVideos2 content =", content)
    regexcat = '"player".*?href="(.*?)"'
    match = re.compile(regexcat,re.DOTALL).findall(content)
    print("getVideos2a match =", match)
    url2 = match[0]
    content2 = getUrl(url2)
    print("getVideos2b content2 =", content2)
    n1 = content2.find(".m3u8")
    n2 = content2.rfind("http", 0, n1)
    url3 = content2[n2:(n1+5)]
    print("getVideos2c url3 =", url3)
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
    urls.append("https://www.raiplay.it/")
    modes.append("32")
    names.append("Mediaset")
    urls.append("https://www.mediasetplay.mediaset.it/")
    modes.append("35")
    pic = " "
    i = 0
    for name in names:
        url = urls[i]
        mode = modes[i]
        i = i+1
        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent32(name, url):
    names = []
    urls = []
    modes = []
    names.append("Film")
    urls.append("http://www.raiplay.it/film/")
    modes.append("33")
    names.append("Serietv")
    urls.append("http://www.raiplay.it/serietv/")
    modes.append("33")
    names.append("Fiction")
    urls.append("http://www.raiplay.it/fiction/")
    modes.append("33")
    names.append("Documentari")
    urls.append("http://www.raiplay.it/documentari/")
    modes.append("33")
    names.append("Bambini")
    urls.append("http://www.raiplay.it/bambini/")
    modes.append("33")
    names.append("Teen")
    urls.append("http://www.raiplay.it/teen/")
    modes.append("33")
    names.append("Tgr")
    urls.append("http://www.tgr.rai.it/dl/tgr/mhp/home.xml")
    modes.append("60")
    pic = " "
    i = 0
    for name in names:
        url = urls[i]
        mode = modes[i]
        i = i+1
        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent33(name, url):
    print("showContent3 name =", name)
    print("showContent3 url =", url)
    content = getUrl(url)
    if PY3:        
            content = six.ensure_str(content)    
    print("showContent3 content =", content)
    name = name.replace("+", " ")
    regexcat = 'data-video-json="(.*?)".*?<img alt="(.*?)"'
    match = re.compile(regexcat, re.DOTALL).findall(content)
    pic = " "
    for url, name in match:
        # if 'raiplay' in url.lower():
            url1 = "http://www.raiplay.it" + url
            content2 = getUrl(url1)
            # print ("showContent33 content2 =", content2)
            regexcat2 = '"/video/(.*?)"'
            match2 = re.compile(regexcat2,re.DOTALL).findall(content2)
            # print ("showContent33 match2 =", match2)
            url2 = match2[0].replace("json", "html")
            url3 = "http://www.raiplay.it/video/" + url2
            # name = name.replace("&#x27;","'").replace("&amp;","&")
            # name = name.replace('&quot;','"').replace('&#39;',"'")
            name = decodeHtml(name)
            name = decodeUrl(name)
            addDirectoryItem(name, {"name":name, "url":url3, "mode":34}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)


def showContent60(name, url):
    names = []
    urls = []
    modes = []
    pics = []
    names.append("TG")
    urls.append("http://www.tgr.rai.it/dl/tgr/mhp/regioni/Page-0789394e-ddde-47da-a267-e826b6a73c4b.html?tgr")
    pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/tgr.png")
    modes.append("61")
    names.append("METEO")
    urls.append("http://www.tgr.rai.it/dl/tgr/mhp/regioni/Page-0789394e-ddde-47da-a267-e826b6a73c4b.html?meteo")
    pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/meteo.png")
    modes.append("61")
    names.append("BUONGIORNO ITALIA")
    urls.append("http://www.tgr.rai.it/dl/rai24/tgr/rubriche/mhp/ContentSet-88d248b5-6815-4bed-92a3-60e22ab92df4.html")
    pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/buongiorno%20italia.png")
    modes.append("61")
    names.append("BUONGIORNO REGIONE")
    urls.append("http://www.tgr.rai.it/dl/tgr/mhp/regioni/Page-0789394e-ddde-47da-a267-e826b6a73c4b.html?buongiorno")
    pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/buongiorno%20regione.png")
    modes.append("61")
    names.append("IL SETTIMANALE")
    urls.append("http://www.tgr.rai.it/dl/rai24/tgr/rubriche/mhp/ContentSet-b7213694-9b55-4677-b78b-6904e9720719.html")
    pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/il%20settimanale.png")
    modes.append("61")
    names.append("RUBRICHE")
    urls.append("http://www.tgr.rai.it/dl/rai24/tgr/rubriche/mhp/list.xml")
    pics.append("http://www.tgr.rai.it/dl/tgr/mhp/immagini/rubriche.png")
    modes.append("61")
    pic = " "
    i = 0
    for name in names:
        url = urls[i]
        mode = modes[i]
        i = i+1
        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)


def showContent61(name, url):
    print("showContent3 name =", name)
    print("showContent3 url =", url)
    content = getUrl(url)
    if PY3:        
            content = six.ensure_str(content)    
    content = content.replace("\r", "").replace("\t", "").replace("\n", "")
    print("showContent3 content =", content)
    regexcat = 'data-video-json="(.*?)".*?<img alt="(.*?)"'
    pic = " "
    try:
        if 'type="video">' in content:
            # print('showContent61 : ', content)
            regexcat = '<label>(.*?)</label>.*?type="video">(.*?)</url>' #relinker
            self["key_green"].setText('Play')
        elif 'type="list">' in content:
            # print('showContent61 : ', content)
            regexcat = '<label>(.*?)</label>.*?type="list">(.*?)</url>'
        else:
            print('passsss')
            pass
        match = re.compile(regexcat, re.DOTALL).findall(content)
        # print("showContent61 match =", match)
        # print('name : ', name)
        for name, url in match:
            if url.startswith('http'):
                url1=url
            else:
                url1 = "http://www.tgr.rai.it" + url
            addDirectoryItem(name, {"name":name, "url":url1, "mode":62}, pic)
            
        xbmcplugin.endOfDirectory(thisPlugin)
    except:
        pass

def showContent62(name, url):
    names = []
    urls = []
    modes = []
    pic = " "  
    if 'relinker' in url:
        print('name222 : ', name)
        print('url222 : ', url)
        play(name, url)         
    else:
        content = getUrl(url)
        if PY3:        
            content = six.ensure_str(content)        
        print("showContent62 content =", content)        
        try:
            if 'type="video">' in content:
                # print('showContent62 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="video">(.*?)</url>' #relinker
            elif 'type="list">' in content:
                # print('showContent62 : ', content)
                regexcat = '<label>(.*?)</label>.*?type="list">(.*?)</url>'
            else:
                print('passsss')
                pass
            match = re.compile(regexcat, re.DOTALL).findall(content)
            # print("showContent62 match =", match)
            for name, url in match:
                # print('name : ', name)
                # print('url : ', url)
                if url.startswith('http'):
                    url1=url
                else:
                    url1 = "http://www.tgr.rai.it" + url
 
                addDirectoryItem(name, {"name":name, "url":url1, "mode":34}, pic)
            xbmcplugin.endOfDirectory(thisPlugin)

        except:
            pass


#######################
def showContent35(name, url):
    names = []
    urls = []
    modes = []
    names.append("Programmitv")
    urls.append("https://www.mediasetplay.mediaset.it/programmitv")
    modes.append("45")
    names.append("Film")
    urls.append("https://www.mediasetplay.mediaset.it/film")
    modes.append("45")
    names.append("Family")
    urls.append("https://www.mediasetplay.mediaset.it/family")
    modes.append("45")
    names.append("Fiction")
    urls.append("https://www.mediasetplay.mediaset.it/fiction")
    modes.append("45")
    names.append("Kids")
    urls.append("https://www.mediasetplay.mediaset.it/kids")
    modes.append("45")
    names.append("Documentari")
    urls.append("https://www.mediasetplay.mediaset.it/documentari")
    modes.append("45")
    pic = " "
    i = 0
    for name in names:
        url = urls[i]
        mode = modes[i]
        i = i+1
        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent45(name, url):
    content = getUrl(url)
    if PY3:        
            content = six.ensure_str(content)    
    print("showContent2 content =", content)
    if "fiction" in name.lower():
        regexcat = 'a href="/fiction/(.*?)".*?class="_2_UgV">(.*?)</p'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print ("_gotPageLoad match =", match)
        for url , name in match:
            pic = " "
            name = decodeHtml(name)
            name = decodeUrl(name)
            #name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'").replace('%20'," ").replace('%3a',":").replace('%27',"'") #url
            url = "https://www.mediasetplay.mediaset.it/fiction/" + url
            print('name : ', name)
            print('url:  ', url)
            addDirectoryItem(name, {"name":name, "url":url, "mode":46}, pic)

    elif "family" in url:
        regexcat = 'href="/movie/(.*?)".*?class="_1ovAG">(.*?)</h3'    #ok
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print ("_gotPageLoad match =", match)
        for url, name in match:
            pic = " "
            name = decodeHtml(name)
            name = decodeUrl(name)
#            name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'").replace('%20'," ").replace('%3a',":").replace('%27',"'")# url
            url = "http://www.mediasetplay.mediaset.it/movie/" + url
            print('name : ', name)
            print('url:  ', url)
            addDirectoryItem(name, {"name":name, "url":url, "mode":46}, pic)

    elif "film" in url:
        regexcat = 'a href="/movie/(.*?)".*?class="_2_UgV">(.*?)</p'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print ("_gotPageLoad match =", match)
        for url, name in match:
            pic = " "
            name = decodeHtml(name)
            name = decodeUrl(name)
#            name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'").replace('%20'," ").replace('%3a',":").replace('%27',"'")# url
            url = "https://www.mediasetplay.mediaset.it/movie/" + url
            print('name : ', name)
            print('url:  ', url)
            addDirectoryItem(name, {"name":name, "url":url, "mode":46}, pic)

    elif "programmi" in url:
        regexcat = 'a href="/programmi-tv/(.*?)".*?class="_2_UgV">(.*?)</p'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print ("_gotPageLoad match =", match)
        for url , name in match:
            name = decodeHtml(name)
            name = decodeUrl(name)
#            name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'").replace('%20'," ").replace('%3a',":").replace('%27',"'")# url
            url = "https://www.mediasetplay.mediaset.it/programmi-tv/" + url
            print('name : ', name)
            print('url:  ', url)
            pic = " "
            addDirectoryItem(name, {"name":name, "url":url, "mode":46}, pic)

    elif "kids" in url:
        regexcat = 'href="/video/(.*?)".*?class="_2_UgV">(.*?)</p'
        # regexcat = 'href="/video/(.*?)".*?class="_2s7uR"><span>(.*?)</span'      #ok
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print ("kids _gotPageLoad match =", match)
        for url, name in match:
            name = decodeHtml(name)
            name = decodeUrl(name)
#            name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'").replace('%20'," ").replace('%3a',":").replace('%27',"'")# url
            url = "https://www.mediasetplay.mediaset.it/video/" + url
            print('name : ', name)
            print('url:  ', url)
            pic = " "
            addDirectoryItem(name, {"name":name, "url":url, "mode":46}, pic)
    else:
        if "documentari" in name.lower():
            regexcat = 'a href="/playlist/(.*?)".*?class="_2_UgV">(.*?)</p'
            match = re.compile(regexcat, re.DOTALL).findall(content)
            print ("_gotPageLoad match =", match)
            for url, name in match:
                name = decodeHtml(name)
                name = decodeUrl(name)
                # name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'").replace('%20'," ").replace('%3a',":").replace('%27',"'")# url
                url = "https://www.mediasetplay.mediaset.it/playlist/" + url
                print('name : ', name)
                print('url:  ', url)
                pic = ""
                addDirectoryItem(name, {"name":name, "url":url, "mode":46}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def showContent46(name, url):
    content = getUrl(url)
    if PY3:        
            content = six.ensure_str(content)    
    print("showContent2 content =", content)
    pic = " "    
    if ("movie" in url) or ("video" in url):
            print("In playVideo2 url =", url)
            from youtube_dl import YoutubeDL
            '''
            ydl_opts = {'format': 'best'}
            ydl_opts = {'format': 'bestaudio/best'}
            '''
            ydl_opts = {'format': 'best'}
            ydl = YoutubeDL(ydl_opts)
            ydl.add_default_info_extractors()
            result = ydl.extract_info(url, download=False)
            print ("mediaset result =", result)
            url = result["url"]
            print ("mediaset final url =", url)
            name = decodeHtml(name)
            name = decodeUrl(name)
#            name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'").replace('%20'," ").replace('%3a',":").replace('%27',"'")# url
            url1 = url
            addDirectoryItem(name, {"name":name, "url":url1, "mode":34}, pic)
    else:
        regexcat = '/video/(.*?)".*?"_1ovAG">(.*?)</'
        match = re.compile(regexcat, re.DOTALL).findall(content)
        print ("_gotPageLoad match =", match)
        for url, name  in match:
            name = decodeHtml(name)
            name = decodeUrl(name)
#            name = name.replace("&#x27;","'").replace("&amp;","&").replace('&quot;','"').replace('&#39;',"'").replace('%20'," ").replace('%3a',":").replace('%27',"'")# url
            url1 = "https://www.mediasetplay.mediaset.it/video/" + url
            print('name : ', name)
            print('url1:  ', url1)
            addDirectoryItem(name, {"name":name, "url":url1, "mode":47}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)


def showContent47(name, url):
    print("In playVideo2434 url =", url)
    from youtube_dl import YoutubeDL
    ydl_opts = {'format': 'best'}
    '''
    ydl_opts = {'format': 'bestaudio/best'}
    '''
    ydl = YoutubeDL(ydl_opts)
    ydl.add_default_info_extractors()
    result = ydl.extract_info(url, download=False)
    print ("mediaset result =", result)
    url = result["url"]
    print ("mediaset final url =", url)
    pic = " "
    name = name
    url1 = url
    play(name, url1)



#edit by LULULLA for kodi pc and kodilite
def playVideo34(name, url):
    print("In playVideo2 url =", url)
    vidurl  = vidpc
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/KodiLite'):
        vidurl = vide2
        cmd = "python '/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/__main__.py' --no-check-certificate --skip-download -f best --get-url '" + url + "' > " + vidurl # /tmp/vid.txt"
        print("In playVideo2 cmd =", cmd)
        if os.path.exists(vidurl):
            os.remove(vidurl)
        os.system(cmd)
        # if not os.path.exists(vidurl):
        os.system("sleep 5")
        play(name, vidurl)
    else:
        vidurl  = vidpc
        cmd = main + " --no-check-certificate --skip-download -f best --get-url '" + url + "' > " + vidurl # /tmp/vid.txt"
        print("In playVideo2 cmd =", cmd)
        if os.path.exists(vidurl):
            os.remove(vidurl)
        os.system(cmd)
        if not os.path.exists(vidurl):
            os.system("sleep 5")        
            play(name, vidurl)
#end edit
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
    elif mode == str(33):
            ok = showContent33(name, url)
    elif mode == str(34):
            ok = playVideo34(name, url)            
    elif mode == str(35):
            ok = showContent35(name, url)    
            
    elif mode == str(41):
            ok = showContent41(name, url)
    elif mode == str(45):
            ok = showContent45(name, url)
    elif mode == str(46):
            ok = showContent46(name, url)
    elif mode == str(47):
            ok = showContent47(name, url)
    elif mode == str(60):
            ok = showContent60(name, url)
    elif mode == str(61):
            ok = showContent61(name, url)
    elif mode == str(62):
            ok = showContent62(name, url)

