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




import xbmc,xbmcaddon, xbmcplugin
import xbmcgui
import os, sys
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
import ssl

import json
import codecs
from urlparse import urljoin

#Here in default-py sys.argv B= ['plugin://plugin.video.youtube/play/', '1', '?video_id=63dLq5GHUIc']
#Here in default-py sys.argv B= ['plugin://plugin.video.youtube/channel/UCFKE7WVJfvaHW5q283SxchA/', '4', '?page=0']
thisPlugin = int(sys.argv[1])
addonId = "plugin.video.youtube"
adn = xbmcaddon.Addon('plugin.video.youtube')
#Hostmain = adn.getSetting('domain')
#pass#print "Hostmain =", Hostmain
#Host = Hostmain + "/index.php?"
#Hostpop = Hostmain + "?sort=views"
#Hosttv = Hostmain + "/?tv"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)

def getUrl(url):
        print "Here in youtube getUrl url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        try:
               response = urllib2.urlopen(req)
        except:
               ctx = ssl.create_default_context()
               ctx.check_hostname = False
               ctx.verify_mode = ssl.CERT_NONE
  	       response = urllib2.urlopen(req, context=ctx)
	link=response.read()
	response.close()
	return link
	
def getUrl2(url, referer):
        print "Here in  getUrl2 url =", url
        print "Here in  getUrl2 referer =", referer
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
		
	
#langurl = "https://www.youtube.com/feed/guide_builder?gl=IT"
#fp = getUrl(langurl)

#def showContent():
#        content = getUrl("https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ?gl=IT")
#        print "In showContent content =", content

def showContent():

        names = []
        urls = []
        modes = []
        name = "Search"
        urlmain = "https://www.youtube.com/"
        pic = " "
        addDirectoryItem(name, {"name":name, "url":urlmain, "mode":1}, pic)
        names.append("Youtube-GB")
        urls.append("gl=GB")
        modes.append("11")  
        names.append("Youtube-ES")
        urls.append("gl=ES")
        modes.append("11")  
        names.append("Youtube-IT")
        urls.append("gl=IT")
        modes.append("11")                            
        names.append("Youtube-FR")
        urls.append("gl=FR")
        modes.append("11")
        names.append("Youtube-DE")
        urls.append("gl=DE")
        modes.append("11")  
        names.append("Youtube-GR")
        urls.append("gl=GR")
        modes.append("11")                            
        names.append("Youtube-IN")
        urls.append("gl=IN")
        modes.append("11")
        names.append("Youtube-DK")
        urls.append("gl=DK")
        modes.append("11")  
        names.append("Youtube-SE")
        urls.append("gl=SE")
        modes.append("11")                            
        names.append("Youtube-RO")
        urls.append("gl=RO")
        modes.append("11")
        print "names =", names
        i1 = 0
        for name in names:
                        print "i1 =", i1
                        url = urls[i1]
                        mode = modes[i1]
                        pic = " "
                        ##print "Here in Showcontent url1 =", url1
                        i1 = i1+1
                        addDirectoryItem(name, {"name":name, "url":url, "mode":mode}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)
	
def showContent1(name1, url):
        print "showContent1 name1 =", name1
        print "showContent1 url =", url
        
        url1 = "https://www.youtube.com/feed/guide_builder?" + url
 
        content = getUrl(url1)
        print "showContent1 content A =", content
        
        url2 = url               
#        regexcat = '"\:{"browseId"\:"(.*?)".*?}},"title".*?simpleText"\:"(.*?)"'
        regexcat = '}},"title".*?simpleText"\:"(.*?)".*?"\:{"browseId"\:"(.*?)"'

        match = re.compile(regexcat,re.DOTALL).findall(content)
        print "showContent1 match =", match
        n1 = 0
        for name, url in match:
                if n1>6:
                    break
                else:    
                        url3 = "https://www.youtube.com/channel/" + url + "/?" + url2
                        pic = " "
                        n1 = n1+1
#                        print "Here in Showcontent url3 =", url3
                        addDirectoryItem(name, {"name":name, "url":url3, "mode":21}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)        

def showContent2(name, url):
        print "showContent2 name =", name     #music
        print "showContent2 url =", url
        
        content = getUrl(url)
        print "showContent2 content A =", content
        
#        regexcat = '"\:{"title"\:{"runs"\:\[{"text"\:"(.*?)".*?"\:{"url"\:"(.*?)"'
        regexcat = '"\:{"title"\:{"simpleText"\:"(.*?)".*?list=(.*?)\\\\u0026'
        
        
        match = re.compile(regexcat,re.DOTALL).findall(content)
        print "showContent2 match =", match
        if (len(match)==1) and ('Want to subscribe to this channel?' in match[0][0]):
                print "going in showContent4 url =", url
                showContent4(name, url) 
        else:                
                for name, url in match:
                        url = url.replace("\u0026", "&")
                        name = name.replace("%27", "'")
                        url3 = "https://www.youtube.com/feeds/videos.xml?playlist_id=" + url
                        pic = " "
#                        print "Here in Showcontent url3 =", url3
                        addDirectoryItem(name, {"name":name, "url":url3, "mode":31}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)        

def showContent4(name, url):
        print "showContent4 name =", name     #music
        print "showContent4 url =", url
        
        content = getUrl(url)
        print "showContent4 content A =", content
        
        regexcat = '"\:{"title"\:{"runs"\:\[{"text"\:"(.*?)".*?"\:{"url"\:"/playlist\?list=(.*?)"'
#        regexcat = '"\:{"title"\:{"simpleText"\:"(.*?)".*?list=(.*?)\\\\u0026'
        
        
        match = re.compile(regexcat,re.DOTALL).findall(content)
        print "showContent4 match =", match
                         
        for name, url in match:
                        url = url.replace("\u0026", "&")
                        name = name.replace("%27", "'")
                        url3 = "https://www.youtube.com/feeds/videos.xml?playlist_id=" + url
                        pic = " "
#                        print "Here in Showcontent url3 =", url3
                        addDirectoryItem(name, {"name":name, "url":url3, "mode":31}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)        
        
        
	
def showContent3(name, url):
        print "showContent3 name1 =", name
        print "showContent3 url =", url
        
        content = getUrl(url)
        print "showContent3 content A =", content
        
        url2 = url               
#        regexcat = '"\:{"title"\:{"runs"\:\[{"text"\:"(.*?)".*?"\:{"url"\:"/playlist\?list=(.*?)"'
        regexcat = '<id>yt\:video.*?<title>(.*?)<.*?<link rel="alternate" href="(.*?)".*?thumbnail url="(.*?)"'

        match = re.compile(regexcat,re.DOTALL).findall(content)
        print "showContent3 match =", match
        for name, url, pic in match:
#                        print "Here in Showcontent url3 =", url3
                        addDirectoryItem(name, {"name":name, "url":url, "mode":41}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)        
        
                            
def getPage(name, url):
                pages = [1, 2, 3]
                print "In getPage name A=", name
                print "In getPage url A=", url
                for page in pages:
                        url1 = url + "&page=" + str(page)
                        name1 = name + " - Page " + str(page)
                        
                        pic = " "
                        addDirectoryItem(name1, {"name":name1, "url":url1, "mode":21}, pic)       
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name, url):
                f = open("/tmp/xbmc_search.txt", "r")
                icount = 0
                for line in f.readlines(): 
                    print "In getVideos line =", line
                    sline = line
                    icount = icount+1
                    if icount > 0:
                           break

                name = sline.replace(" ", "+")
                print "In getVideos name =", name
                url1 = "https://www.youtube.com/results?search_query=" + name
                pages = [1, 2, 3]
                for page in pages:
                        url = url1 + "&page=" + str(page)
                        print "Here in getVideos url =", url
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos2(name1, urlmain):
        print "In getVideos21 urlmain =", urlmain
	content = getUrl(urlmain)
	print "In getVideos21 content =", content
	
	regexvideo = 'title"\:\{"runs"\:\[\{"text"\:"(.*?)".*?"url"\:"/watch\?v=(.*?)"'
#        regexvideo = 'title":{"runs":[{"text":"(.*?)".*?"url"\:"/watch?v=(.*?)"'
        
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        print "In getVideos21 match =", match
        
        for name, url in match:
                 pic = " "
                 #https://www.youtube.com/watch?v=YQHsXMglC9A
                 url1 = "https://www.youtube.com/watch?v=" + url
                 #print "Here in getVideos21 name, url =", name, url
	         addDirectoryItem(name, {"name":name, "url":url, "mode":5}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)
        
        
                

def getVideos4(name, url):
        import youtube_dl
        print "Here in getVideos4 url 1=", url
#        url = "https://www.youtube.com/watch?v=" + url
        from youtube_dl import YoutubeDL
        print "Here in getVideos4 url 2", url
        ydl_opts = {'format': 'best'}
        ydl = YoutubeDL(ydl_opts)
        ydl.add_default_info_extractors()
       # url = "https://www.youtube.com/watch?v=CSYCEyMQWQA"
        result = ydl.extract_info(url, download=False)
        print "result =", result
        url = result["url"]
        print "Here in Test url =", url
        play(name, url)

def play(name, url):
           print "Here in playVideo url B=", url
           li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
           player = xbmc.Player()
           player.play(url, li)

def getVideos4X(name, url): 
        url = "https://www.youtube.com/watch?v=" + url
        print "In getVideos4 url =", url    
        cmd = "python '/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/__main__.py' --no-check-certificate --skip-download -f best --get-url '" + url + "' > /tmp/vid.txt"
        print "In getVideos4 cmd =", cmd
        if os.path.exists("/tmp/vid.txt"):
               os.remove("/tmp/vid.txt")
        os.system(cmd)
        vidurl = "/tmp/vid.txt"

        if not os.path.exists(vidurl):
              os.system("sleep 5")
              playfile = xbmc.Player()
              playfile.play(vidurl)
        else: 
              playfile = xbmc.Player()
              playfile.play(vidurl)        

def playVideo(name, url):
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
    #print "In addDirectoryItem name, url =", name, url
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
#Here in default-py sys.argv B= ['plugin://plugin.video.youtube/', '4', '?path=/root/video&path=root/video&action=play_video&videoid=q3WIm2jrxSc']
if "action=play_video" in sys.argv[2]:
            sys.argv[2] = sys.argv[2].replace("?", "?mode=5&")
            sys.argv[2] = sys.argv[2].replace("videoid", "url")

#Here in default-py sys.argv B= ['plugin://plugin.video.youtube/channel/UCFKE7WVJfvaHW5q283SxchA/', '4', '?page=0']
    
if ("youtube/channel/" in sys.argv[0]) and (not "mode=" in sys.argv[2]):
            arg1 = sys.argv[0]  
            n1 = arg1.find("/channel", 0)
            n2 = arg1.find("/", (n1+3))
            ch = arg1[(n2+1):]
            ch = ch.replace("/", "")
            print "Here in youtube default-py ch =", ch
            name = "channel"
            url = "https://www.youtube.com/channel/" + ch
            pic = " "
#            addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
#            xbmcplugin.endOfDirectory(thisPlugin)
            getVideos2(name, url)
#Here in default-py sys.argv B= ['plugin://plugin.video.youtube/play/', '1', '?video_id=63dLq5GHUIc']
            
if "youtube/play" in sys.argv[0]:
            arg1 = sys.argv[2]
            n1 = arg1.find("video_id", 0)
            n2 = arg1.find("=", n1)
            n3 = arg1.find("&", n2)
            if n3 < 0:
                   url = arg1[(n2+1):]
            else:       
                   url = arg1[(n2+1):n3]
            print "Here in default-py url =", url     
            pic = " "
            name = "videoName"
#            addDirectoryItem(name, {"name":name, "url":url, "mode":5}, pic)
#            xbmcplugin.endOfDirectory(thisPlugin)
            getVideos4(name, url)
            
params = parameters_string_to_dict(sys.argv[2])
name =  str(params.get("name", ""))
url =  str(params.get("url", ""))
url = urllib.unquote(url)
mode =  str(params.get("mode", ""))

if not sys.argv[2]:
	ok = showContent()
else:
        if mode == str(11):
		ok = showContent1(name, url)
	elif mode == str(21):
		ok = showContent2(name, url)	
		
	elif mode == str(31):
	        ok = showContent3(name, url)

	elif mode == str(41):
	        ok = getVideos4(name, url)

        elif mode == str(1):
		ok = getVideos(name, url)
	elif mode == str(2):
		ok = getVideos2(name, url)
                
                	



