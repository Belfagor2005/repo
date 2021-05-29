#!/usr/bin/python
# -*- coding: utf-8 -*-
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


import sys
import logging
import xbmcgui
import xbmc
import xbmcplugin
import xbmcaddon
import json

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

addon_id = 'plugin.video.tivustreampro'
selfAddon = xbmcaddon.Addon(id=addon_id)

viewmode=None

import six
import sys

PY3 = sys.version_info.major >= 3

if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse, unquote
    from urllib.parse import urlencode, quote
    import urllib.request, urllib.parse, urllib.error
    from html.entities import name2codepoint as n2cp
    import http.client
    from urllib.parse import parse_qs, parse_qsl
    from urllib.parse import unquote_plus
    import http.cookiejar
    from urllib.request import urlretrieve
else:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urlparse import urlparse
    from urllib import urlencode, quote
    import urllib, urllib2
    from htmlentitydefs import name2codepoint as n2cp
    import httplib
    from urlparse import parse_qs, parse_qsl
    from urllib import unquote_plus, unquote
    import cookielib
    from urllib import urlretrieve
    
UserAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
def checkUrl(url):
    try:
        response = checkStr(urlopen(url, None, 5))
        response.close()
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True

try:
    from OpenSSL import SSL
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False

if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSO
                
def makeRequest(url, hdr=None):
    try:
        pwd = selfAddon.getSetting("password")
        version = selfAddon.getAddonInfo("version")
        if hdr is None:
            ua = "TiVuStreamPro@@"+version+"@@"+pwd
            hdr = {"User-Agent" : ua}
        req = Request(url, headers=hdr)
        response = urlopen(req)
        html = response.read()
        response.close()
        print("link =", html)
        return html
    except:
        e = URLError
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def getSource():
    startUrl = selfAddon.getSetting("baseUrl")
    strSource = makeRequest(startUrl)
    if strSource is None or strSource == "":
        logging.warning('We failed to get source from '+startUrl)
    else:
        logging.warning('OK SOURCE ')
        jsonToItems(strSource)

def getExternalJson(strPath):
    strSource = makeRequest(strPath)
    jsonToItems(strSource)

def jsonToItems(strJson):
    global viewmode
    dataJson = json.loads(strJson)
    xbmcplugin.setContent(_handle, 'videos')
    try:
        viewmode = dataJson['SetViewMode']
        skin_name = xbmc.getSkinDir()
        logging.warning("setting view mode for "+skin_name+" on "+viewmode)
        #xbmc.executebuiltin("Container.SetViewMode("+viewmode+")")
    except:
        logging.warning('no view mode')
        pass

    for item in dataJson["items"]:
        titolo = "NO TIT"
        thumb = "https://www.andreisfina.it/wp-content/uploads/2018/12/no_image.jpg"
        fanart = "https://www.andreisfina.it/wp-content/uploads/2018/12/no_image.jpg"
        genre = "generic"
        info = ""
        link = ""
        extLink = False
        extLink2 = False
        is_folder = False
        is_yatse = False
        is_chrome = False
        is_enabled = True

        if 'enabled' in item:
            is_enabled = item["enabled"]

        if is_enabled == False:
            continue
        
        if 'title' in item:
            titolo = item["title"]
        
        if 'thumbnail' in item:
            thumb = item["thumbnail"]

        if 'fanart' in item:
            fanart = item["fanart"]

        if 'info' in item:
            info = item["info"]

        if 'genre' in item:
            genre = item["genre"]

        if 'link' in item:
            link = item["link"]

        if 'externallink' in item:
            extLink = True
            is_folder = True
            link = item["externallink"]

        if 'externallink2' in item:
            extLink2 = True
            is_folder = True
            link = item["externallink2"]

        if 'chrome' in item:
            is_chrome = True
            is_folder = True
            link = item["chrome"]

        if 'yatse' in item:
            is_yatse = True
            is_folder = True
            link = item["yatse"]

        list_item = xbmcgui.ListItem(label=titolo)
        list_item.setInfo('video', {'title': titolo,
                                    'genre': genre,
                                    'mediatype': 'video'})
        list_item.setArt({'thumb': thumb, 'icon': thumb, 'fanart': fanart})
        
        url = ""
        if extLink == True:
            url = get_url(action='getExtData', url=link)
        elif extLink2 == True:
            url = get_url(action='getExtData2', url=link)
        elif is_yatse == True:
            list_item.setProperty('IsPlayable', 'true')                                                       
            url = get_urlYatse(action='share', type='unresolvedurl', data=link)
        elif is_chrome == True:
            url = get_urlChrome(mode='showSite', stopPlayback='no', kiosk='no', url=link)
        else:
            list_item.setProperty('IsPlayable', 'true')
            url = get_url(action='play', url=link)

        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def get_urlYatse(**kwargs):
    return '{0}?{1}'.format("plugin://script.yatse.kodi/", urlencode(kwargs))

def get_urlChrome(**kwargs):
    return '{0}?{1}'.format("plugin://plugin.program.browser.launcher/", urlencode(kwargs))

def parameters_string_to_dict(parameters):
    params = dict(parse_qsl(parameters.split('?')[1]))
    return params

if not sys.argv[2]:
    logging.warning("=== ADDON START ===")
    getSource()
else:
    params = parameters_string_to_dict(sys.argv[2])
    action =  params['action']
    url =  params['url']
    logging.warning("ACTION ==> "+action)
    logging.warning("URL ==> "+url)
    if action == 'getExtData':
        getExternalJson(url)
    elif action == 'getExtData2':
        keyboard = xbmc.Keyboard('','Insert string')
        keyboard.doModal()
        if not (keyboard.isConfirmed() == False):
            userInput = keyboard.getText()
            strUrl = url + str(userInput)
            getExternalJson(strUrl)
    elif action == 'youtubedl':
        logging.warning("TRY TO RESOLVE URL: "+url)
        urlSolved = youtubeResolve(url)
        play_video(urlSolved)
    elif action == 'play':
        play_video(url)
    else:
        raise ValueError('Invalid paramstring: {0}!'.format(params))

if not viewmode==None:
   logging.warning("setting view mode")
   xbmc.executebuiltin("Container.SetViewMode("+viewmode+")")
