#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, xpath, os
"""
Copyright (C) 2019
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
Developed by Lululla for TiVuStream.com
Thank's @MasterG & @pcd for all (Linuxsat support)
"""

# import urllib, urllib2
import unicodedata, json
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import xbmcvfs, socket, time, threading 
import os
import re
import base64
import logging

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


import six
from sys import version_info

PY3 = version_info[0] == 3
if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import quote, unquote_plus, unquote, urlencode
    from urllib.request import urlretrieve
    from urllib.parse import urlparse, quote_plus
    from html.entities import name2codepoint as n2cp
    import http.client
    import html.parser
else:
    from urllib2 import urlopen, Request
    from urllib2 import URLError, HTTPError
    from urllib import quote, unquote_plus, unquote, urlencode
    from urllib import urlretrieve, quote_plus
    from urlparse import urlparse
    from htmlentitydefs import name2codepoint as n2cp
    import httplib
    import HTMLParser
    
PLUGIN_NAME = "tivustream"
plugin_handle = int(sys.argv[1])
ua = "&ua=TiVuStream"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' }

mysettings = xbmcaddon.Addon(id="plugin.video." + PLUGIN_NAME)
# __language__ = mysettings.get_string
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
artfolder = (home + '/resources/img/')
fanart2 = xbmc.translatePath(os.path.join(home, 'fanart2.png'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
show = xbmc.translatePath(os.path.join(home, 'show.txt'))
contentx = xbmc.translatePath(os.path.join(home, 'contentx.txt'))
#############################
f_events = xbmc.translatePath(os.path.join(artfolder, 'events.jpg'))
f_free = xbmc.translatePath(os.path.join(artfolder, 'free.jpg'))
f_sport = xbmc.translatePath(os.path.join(artfolder, 'sport.jpg'))
f_media = xbmc.translatePath(os.path.join(artfolder, 'media.jpg'))
f_series = xbmc.translatePath(os.path.join(artfolder, 'series.jpg'))
f_fiction = xbmc.translatePath(os.path.join(artfolder, 'fiction.jpg'))
f_media_60_90 = xbmc.translatePath(os.path.join(artfolder, 'media_60_90.jpg'))
f_music = xbmc.translatePath(os.path.join(artfolder, 'music.jpg'))
f_news = xbmc.translatePath(os.path.join(artfolder, 'news.jpg'))
f_radio = xbmc.translatePath(os.path.join(artfolder, 'radio.jpg'))
f_int = xbmc.translatePath(os.path.join(artfolder, 'int.jpg'))
f_mediaint = xbmc.translatePath(os.path.join(artfolder, 'mediaint.jpg'))
f_seriesint = xbmc.translatePath(os.path.join(artfolder, 'series.png'))
f_radioint = xbmc.translatePath(os.path.join(artfolder, 'radioint.jpg'))
f_search = xbmc.translatePath(os.path.join(artfolder, 'search.jpg'))
##############################3
i_events = xbmc.translatePath(os.path.join(artfolder, 'events.png'))
i_free = xbmc.translatePath(os.path.join(artfolder, 'free.png'))
i_sport = xbmc.translatePath(os.path.join(artfolder, 'sport.png'))
i_media = xbmc.translatePath(os.path.join(artfolder, 'media.png'))
i_series = xbmc.translatePath(os.path.join(artfolder, 'series.png'))
i_fiction = xbmc.translatePath(os.path.join(artfolder, 'fiction.png'))
i_media_60_90 = xbmc.translatePath(os.path.join(artfolder, 'media_60_90.png'))
i_music = xbmc.translatePath(os.path.join(artfolder, 'music.png'))
i_news = xbmc.translatePath(os.path.join(artfolder, 'news.png'))
i_radio = xbmc.translatePath(os.path.join(artfolder, 'radio.png'))
i_int = xbmc.translatePath(os.path.join(artfolder, 'int.png'))
i_mediaint = xbmc.translatePath(os.path.join(artfolder, 'mediaint.png'))
i_seriesint = xbmc.translatePath(os.path.join(artfolder, 'series.png'))
i_radioint = xbmc.translatePath(os.path.join(artfolder, 'radioint.png'))
i_search = xbmc.translatePath(os.path.join(artfolder, 'search.png'))
####################################
events_m3u = mysettings.getSetting('events_m3u') + ua
free_it_m3u = mysettings.getSetting('free_it_m3u') + ua
free_reg_m3u = mysettings.getSetting('free_reg_m3u') + ua
sport_it_m3u = mysettings.getSetting('sport_it_m3u') + ua
sport_int_m3u = mysettings.getSetting('sport_int_m3u') + ua
media_m3u = mysettings.getSetting('media_m3u') + ua
media_09_m3u = mysettings.getSetting('media_09_m3u') + ua
media_af_m3u = mysettings.getSetting('media_af_m3u') + ua
media_gl_m3u = mysettings.getSetting('media_gl_m3u') + ua
media_mr_m3u = mysettings.getSetting('media_mr_m3u') + ua
media_sz_m3u = mysettings.getSetting('media_sz_m3u') + ua
mediaint_m3u = mysettings.getSetting('mediaint_m3u') + ua
series_09_m3u = mysettings.getSetting('series_09_m3u') + ua
series_ae_m3u = mysettings.getSetting('series_ae_m3u') + ua
series_fk_m3u = mysettings.getSetting('series_fk_m3u') + ua
series_lr_m3u = mysettings.getSetting('series_lr_m3u') + ua
series_sz_m3u = mysettings.getSetting('series_sz_m3u') + ua
seriesint_m3u = mysettings.getSetting('seriesint_m3u')
music_m3u = mysettings.getSetting('music_m3u') + ua
news_m3u = mysettings.getSetting('news_m3u') + ua
int_m3u = mysettings.getSetting('int_m3u') + ua

int2_m3u = mysettings.getSetting('int2_m3u')

radio_m3u = mysettings.getSetting('radio_m3u') + ua
radioint_m3u = mysettings.getSetting('radioint_m3u') + ua
radiodash_m3u = mysettings.getSetting('radiodash_m3u') + ua
relax_m3u = mysettings.getSetting('relax_m3u') + ua
online_m3u = mysettings.getSetting('online_m3u')
log_m3u     = mysettings.getSetting('log_m3u')
####################################
# data        = 'aHR0cDovL2x1bHVsbGEuYWx0ZXJ2aXN0YS5vcmcvaXB0di1tYXN0ZXIv'
# h           = base64.b64decode(data)
h= 'https://raw.githubusercontent.com/iptv-org/iptv/master/'
xml_regex   = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
m3u_regex   = '#(.+?),(.+)\s*(.+)\s*'
m3u_regex2  = 'EXTINF.*?,(.*?)\\n(.*?)\\n' #'#(.+?),(.+)\s*(.+)\s*'
u_tube      = 'http://www.youtube.com'
# estm3u = 'aHR0cDovL3BhdGJ1d2ViLmNvbS9waHBfZmlsdGVyL2ZoLnBocA=='
# m3uest = base64.b64decode(estm3u)

m3uest = 'https://raw.githubusercontent.com/iptv-org/iptv/master/index.m3u'
host = 'https://raw.githubusercontent.com/iptv-org/iptv/master/'

def removeAccents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))

def read_file(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        pass

def make_request(url):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
        response = urlopen(req)
        link = response.read()
        response.close()
        print("link =", link)
        return link
    except URLError as e:
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)

##########pcd###############
def showInfo(content):
    ############# not needed if server text changed #############
    content = content.replace("#EXTM3U", "")
    content = content.replace("#EXTINF:-1,", "")
    content = content.replace("#EXTINF:0,", "")
    content = content.replace("http://0.0.0.0", "")
    content = content.replace("[/COLOR]", "")
    content = content.replace("[COLOR yellow]", "")
    content = content.replace("Support:", "Support:\n")
    content = content.replace("Thank's to", "Thanks to:\n")
    ##############################################################
    msg = content
    if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"):  #KodiLite
        f1 = open(show, "w")
        f1.write(msg)
        pic = " "
        name = "Version Support"
        url = "showtext"
        addDirectoryItem(name, {"name":name, "url":url, "mode":6}, pic)
    else:      #kodi
        dialog = xbmcgui.Dialog()
        dialog.textviewer("Version Support", msg)
        Main()
################################
def main():
    add_dir('[COLOR gray][B] Version Support (changelog) [/B][/COLOR]', u_tube, 111, icon, fanart2)
    add_dir('[B]°°° SEARCH °°°[/B]', 'searchlink', 99, i_search, f_search)
    add_dir('[COLOR lime][B]Eventi Live[/B][/COLOR]', u_tube, 2, i_events, f_events)
    add_dir('[COLOR yellow][B]Canali Italiani Top[/B][/COLOR]', u_tube, 3, i_free, f_free)
    add_dir('[COLOR yellow][B]Canali Italiani Regionali[/B][/COLOR]', u_tube, 4, i_free, f_free)
    add_dir('[COLOR blue][B]Canali Sport Italia[/B][/COLOR]', u_tube, 5, i_sport, f_sport)
    add_dir('[COLOR blue][B]Canali Sport Estero[/B][/COLOR]', u_tube, 6, i_sport, f_sport)
    add_dir('[COLOR cyan][B]Film Recenti[/B][/COLOR]', u_tube, 10, i_media, f_media)
    add_dir('[COLOR cyan][B]Film 0-9[/B][/COLOR]', u_tube, 11, i_media, f_media)
    add_dir('[COLOR cyan][B]Film A-F[/B][/COLOR]', u_tube, 12, i_media, f_media)
    add_dir('[COLOR cyan][B]Film G-L[/B][/COLOR]', u_tube, 13, i_media, f_media)
    add_dir('[COLOR cyan][B]Film M-R[/B][/COLOR]', u_tube, 14, i_media, f_media)
    add_dir('[COLOR cyan][B]Film S-Z[/B][/COLOR]', u_tube, 15, i_media, f_media)
    add_dir('[COLOR fuchsia][B]Serie TV 0-9[/B][/COLOR]', u_tube, 20, i_fiction, f_fiction)
    add_dir('[COLOR fuchsia][B]Serie TV A-E[/B][/COLOR]', u_tube, 21, i_fiction, f_fiction)
    add_dir('[COLOR fuchsia][B]Serie TV F-K[/B][/COLOR]', u_tube, 52, i_fiction, f_fiction)
    add_dir('[COLOR fuchsia][B]Serie TV L-R[/B][/COLOR]', u_tube, 23, i_fiction, f_fiction)
    add_dir('[COLOR fuchsia][B]Serie TV S-Z[/B][/COLOR]', u_tube, 24, i_fiction, f_fiction)
    
    add_dir('[COLOR orange][B]Canali Musica ( Radio Tv )[/B][/COLOR]', u_tube, 40, i_music, f_music)
    add_dir('[COLOR orange][B]Radio Italiane[/B][/COLOR]', u_tube, 41, i_radio, f_radio)
    add_dir('[COLOR orange][B]International Radio[/B][/COLOR]', u_tube, 42, i_radioint, f_radioint)
    add_dir('[COLOR orange][B]Dash Radio[/B][/COLOR]', u_tube, 43, i_radio, f_radio)
    add_dir('[COLOR pink][B]Look And Relax[/B][/COLOR]', u_tube, 60, icon, fanart)
    add_dir('[COLOR red][B]All News[/B][/COLOR]', u_tube, 30, i_news, f_news)  
    
    add_dir('[COLOR yellow][B] +++ OTHER +++ [/B][/COLOR]', u_tube, 50, icon, fanart)  
    add_dir('[COLOR red][B]International Channels[/B][/COLOR]', u_tube, 31, i_int, f_int)
    add_dir('[COLOR red][B]International Channels II[/B][/COLOR]', u_tube, 35, i_int, f_int)    
    add_dir('[COLOR cyan][B]International Movies[/B][/COLOR]', u_tube, 16, i_mediaint, f_mediaint)    
    add_dir('[COLOR fuchsia][B]International Tv Series[/B][/COLOR]', u_tube, 25, i_seriesint, f_seriesint)


    
    if (  len(events_m3u) < 1 and len(free_it_m3u) < 1 and len(free_reg_m3u) < 1 and len(sport_it_m3u) < 1 and len(sport_int_m3u) < 1 and len(media_m3u) < 1 and len(media_09_m3u) < 1 and len(media_af_m3u) < 1 and len(media_gl_m3u) < 1 and  len(media_mr_m3u) < 1 and len(media_sz_m3u) < 1 and len(mediaint_m3u) < 1 and len(series_09_m3u) < 1 and len (series_ae_m3u) < 1 and len(series_fk_m3u) < 1 and len(series_lr_m3u) < 1 and len(series_sz_m3u) < 1 and len(seriesint_m3u) < 1 and len(music_m3u) < 1 and len(news_m3u) < 1 and len(int_m3u) < 1 and len(radio_m3u) < 1 and len(radioint_m3u ) < 1 and len(radiodash_m3u) < 1 and len(log_m3u) < 1 ):
        mysettings.openSettings()
        xbmc.executebuiltin("Container.Refresh")

def search():
    try:
        keyb = xbmc.Keyboard('', 'Search :')
        keyb.doModal()
        if (keyb.isConfirmed()):
                searchText = quote_plus(keyb.getText()).replace('+', ' ')
        if len(events_m3u) > 0:
                content = make_request(events_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(free_it_m3u) > 0:
                content = make_request(free_it_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(free_reg_m3u) > 0:
                content = make_request(free_reg_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(sport_it_m3u) > 0:
                content = make_request(sport_it_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(sport_int_m3u) > 0:
                content = make_request(sport_int_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(media_09_m3u) > 0:
                content = make_request(media_09_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(media_af_m3u) > 0:
                content = make_request(media_af_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(media_gl_m3u) > 0:
                content = make_request(media_gl_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(media_mr_m3u) > 0:
                content = make_request(media_mr_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(media_sz_m3u) > 0:
                content = make_request(media_sz_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(mediaint_m3u) > 0:
                content = make_request(mediaint_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(series_09_m3u) > 0:
                content = make_request(series_09_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(series_ae_m3u) > 0:
                content = make_request(series_ae_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(series_fk_m3u) > 0:
             content = make_request(series_fk_m3u)
             match = re.compile(m3u_regex).findall(content)
             for thumb, name, url in match:
                if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                   m3u_playlist(name, url, thumb)

        if len(series_lr_m3u) > 0:
             content = make_request(series_lr_m3u)
             match = re.compile(m3u_regex).findall(content)
             for thumb, name, url in match:
                if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                   m3u_playlist(name, url, thumb)


        if len(series_sz_m3u) > 0:
             content = make_request(series_sz_m3u)
             match = re.compile(m3u_regex).findall(content)
             for thumb, name, url in match:
                if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                   m3u_playlist(name, url, thumb)

        if len(seriesint_m3u) > 0:
                content = make_request(seriesint_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(music_m3u) > 0:
                content = make_request(music_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(news_m3u) > 0:
                content = make_request(news_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(int_m3u) > 0:
                content = make_request(int_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)


        if len(radio_m3u) > 0:
                content = make_request(radio_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(radioint_m3u) > 0:
                content = make_request(radioint_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)

        if len(radiodash_m3u) > 0:
                content = make_request(radiodash_m3u)
                match = re.compile(m3u_regex).findall(content)
                for thumb, name, url in match:
                        if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                                m3u_playlist(name, url, thumb)
    except:
        pass

def open_list(cheLista):
    content = make_request(free_it_m3u)
    content = six.ensure_str(content)
    if cheLista == 2:
        content = make_request(events_m3u)
        content = six.ensure_str(content)
    elif cheLista == 3:
        content = make_request(free_it_m3u)
        content = six.ensure_str(content)
    elif cheLista == 4:
        content = make_request(free_reg_m3u)
        content = six.ensure_str(content)
    elif cheLista == 5:
        content = make_request(sport_it_m3u)
        content = six.ensure_str(content)
    elif cheLista == 6:
        content = make_request(sport_int_m3u)
        content = six.ensure_str(content)
    elif cheLista == 10:
        content = make_request(media_m3u)
        content = six.ensure_str(content)
    elif cheLista == 11:
        content = make_request(media_09_m3u)
        content = six.ensure_str(content)
    elif cheLista == 12:
        content = make_request(media_af_m3u)
        content = six.ensure_str(content)
    elif cheLista == 13:
        content = make_request(media_gl_m3u)
        content = six.ensure_str(content)
    elif cheLista == 14:
        content = make_request(media_mr_m3u)
        content = six.ensure_str(content)
    elif cheLista == 15:
        content = make_request(media_sz_m3u)
        content = six.ensure_str(content)
    elif cheLista == 16:
        content = make_request(mediaint_m3u)
        content = six.ensure_str(content)
    elif cheLista == 20:
        content = make_request(series_09_m3u)
        content = six.ensure_str(content)
    elif cheLista == 21:
        content = make_request(series_ae_m3u)
        content = six.ensure_str(content)
    elif cheLista == 52:
        content = make_request(series_fk_m3u)
        content = six.ensure_str(content)
    elif cheLista == 23:
        content = make_request(series_lr_m3u)
        content = six.ensure_str(content)
    elif cheLista == 24:
        content = make_request(series_sz_m3u)
        content = six.ensure_str(content)
    elif cheLista == 25:
        content = make_request(seriesint_m3u)
        content = six.ensure_str(content)
    elif cheLista == 30:
        content = make_request(news_m3u)
        content = six.ensure_str(content)
    #INTERNATIONAL II
    elif cheLista == 35:
        # content = make_request(m3uest)   
        m3u_online3()
    elif cheLista == 31:
        # content = make_request(int_m3u)
        m3u_online()
############ pcd 1 ############################
        countries(content)
###############################################
    elif cheLista == 40:
        content = make_request(music_m3u)
        content = six.ensure_str(content)
    elif cheLista == 41:
        content = make_request(radio_m3u)
        content = six.ensure_str(content)
    elif cheLista == 42:
        content = make_request(radioint_m3u)
        content = six.ensure_str(content)
    elif cheLista == 43:
        content = make_request(radiodash_m3u)
        content = six.ensure_str(content)
    elif cheLista == 50:
        m3u_online()
    elif cheLista == 60:
        content = make_request(relax_m3u)
        content = six.ensure_str(content)
    elif cheLista == 111:
        content = make_request(log_m3u)
        content = six.ensure_str(content)
        showInfo(content)     ############### pcd #################
    match = re.compile(m3u_regex).findall(content)
    for thumb, name, url in match:
        try:
            m3u_playlist(name, url, thumb)
        except:
            pass
################# pcd 2 ############################
def countries(content):
    print("content =", content)
    f = open(contentx, 'w')
    fpage = f.write(content)
    f.close()
    regexvideo = ',---(.*?)---'
    match = re.compile(regexvideo,re.DOTALL).findall(content)
    print("countries match =", match)
    for name in match:
         if "INTENAZIONALI" in name: continue
         url = " "
         pic = " "
         addDirectoryItem(name, {"name":name, "url":url, "mode":112}, pic)
         # add_dir(name, url, 112, pic, pic)
    xbmcplugin.endOfDirectory(plugin_handle)

def links(name, url):
        f = open(contentx, 'r')
        fpage = f.read()
        f.close()
        name = name.replace("+", "")
        name = name.replace("%28", "(")
        name = name.replace("%29", ")")
        name = name.replace("-", " ")
        name = name[:5]
        print("links name =", name)
        print("links fpage =", fpage)
        
        n1 = fpage.find(name, 0)
        n2 = fpage.find(",---", (n1+40))
        print("links n1, n2 =", n1, n2)
        fpage2 = fpage[n1:n2]
        print("links fpage2 =", fpage2)
        regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
        match = re.compile(regexcat,re.DOTALL).findall(fpage2)
        print("In links match =", match)
        for name, url in match:
            url = url.replace(" ", "")
            url = url.replace("?", "")
            url = url.replace("\\n", "")
            url = url.replace('\\r','')
            name = name.replace('\\r','')
            name = name.replace('\\n','')
            pic = " "
            add_dir(name, url, 1, pic, pic)
            # add_link(name, url, 1, pic, pic)
        xbmcplugin.endOfDirectory(plugin_handle)
#######################  pcd end #############################################
def m3u_online():
    content = make_request(online_m3u)
    content = six.ensure_str(content)
    match = re.compile(m3u_regex2).findall(content)
    for name, url in match:
                # url = url
                h= 'https://raw.githubusercontent.com/iptv-org/iptv/master/'
                url = h + url
                print('urlslsl ',url)
                thumb= ''
                add_dir(name, url, 22, thumb, thumb)
    xbmcplugin.endOfDirectory(plugin_handle)
        
def m3u_online3():
    content = make_request(m3uest)
    content = six.ensure_str(content)
    match = re.compile(m3u_regex2).findall(content)
    for name, url in match:
                url = url
                thumb= ''
                add_dir(name, url, 27, thumb, thumb)
    xbmcplugin.endOfDirectory(plugin_handle)        

def m3u_online2(name, url, thumb):
    # content = make_request(url)
    # if PY3:        
        # content = six.ensure_str(content)
    print('urllll  ',url)    
    # url = six.ensure_str(host) + url
    # print('read url: ',  url)
    # content = checkStr(getUrl(url))
    req = Request(url, None, headers=headers)
    content = urlopen(req, timeout=30).read()
    content = six.ensure_str(content)
    print("m3u_online2 =", content)
        
    regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
    match = re.compile(regexcat,re.DOTALL).findall(content)
    for name, url in match:
            url = url.replace(" ", "")
            url = url.replace("\\n", "")
            url = url.replace('\r','')
            if 'tvg-logo' in thumb:
                thumb = re.compile(thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
                # add_link(name, url, 1, thumb, thumb)
            name = name.replace('\r','')
            try:
                m3u_playlist(name, url, thumb)
            except:
                pass

def m3u_local():
    content = read_file(local_m3u)
    content = six.ensure_str(content)
    match = re.compile(m3u_regex).findall(content)
    for thumb, name, url in match:
        try:
            m3u_playlist(name, url, thumb)
        except:
            pass

def xml_online():
    content = make_request(online_xml)
    content = six.ensure_str(content)
    match = re.compile(xml_regex).findall(content)
    for name, url, thumb in match:
        try:
            xml_playlist(name, url, thumb)
        except:
            pass

def xml_local():
    content = read_file(local_xml)
    content = six.ensure_str(content)
    match = re.compile(xml_regex).findall(content)
    for name, url, thumb in match:
        try:
            xml_playlist(name, url, thumb)
        except:
            pass

def m3u_playlist(name, url, thumb):
    name = re.sub('\s+', ' ', name).strip()
    url = url.replace('"', ' ').replace('&amp;', '&').strip()
    if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
        if 'tvg-logo' in thumb:
            thumb = re.compile(thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
            add_dir(name, url, '', thumb, thumb)
        else:
            add_dir(name, url, '', icon, fanart)
    else:
        if 'youtube.com/watch?v=' in url:
            url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
        elif 'dailymotion.com/video/' in url:
            url = url.split('/')[-1].split('_')[0]
            url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url
        else:
            url = url
        if 'tvg-logo' in thumb:
            thumb = re.compile(thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
            add_link(name, url, 1, thumb, thumb)
        else:
            add_link(name, url, 1, icon, fanart)

def xml_playlist(name, url, thumb):
    name = re.sub('\s+', ' ', name).strip()
    url = url.replace('"', ' ').replace('&amp;', '&').strip()
    if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
        if len(thumb) > 0:
            add_dir(name, url, '', thumb, thumb)
        else:
            add_dir(name, url, '', icon, fanart)
    else:
        if 'youtube.com/watch?v=' in url:
            url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
        elif 'dailymotion.com/video/' in url:
            url = url.split('/')[-1].split('_')[0]
            url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url
        else:
            url = url
        if len(thumb) > 0:
            add_link(name, url, 1, thumb, thumb)
        else:
            add_link(name, url, 1, icon, fanart)

def play_video(url):
    media_url = url
    item = xbmcgui.ListItem(name, path = media_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    return

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring)>= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

def add_dir(name, url, mode, iconimage, fanart):
        u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name) + "&iconimage=" + quote_plus(iconimage)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
        liz.setInfo( type = "Video", infoLabels = { "Title": name } )
        liz.setProperty('fanart_image', fanart)
        if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
                u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
                ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
                return ok
        ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
        return ok

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)


def add_link(name, url, mode, iconimage, fanart):
    u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name) + "&iconimage=" + quote_plus(iconimage)
    liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
    liz.setInfo( type = "Video", infoLabels = { "Title": name } )
    liz.setProperty('fanart_image', fanart)
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)

params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
    url = unquote_plus(params["url"])
except:
    pass
try:
    name = unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    iconimage = unquote_plus(params["iconimage"])
except:
    pass

print("Mode: " + str(mode))
print("URL: " + str(url))
print("Name: " + str(name))
print("iconimage: " + str(iconimage))

if mode == None or url == None or len(url) < 1:
    main()
elif mode == 1:
    play_video(url)
elif mode == 99:
    search()
elif mode == 27:
    thumb = icon
    ok = m3u_online2(name, url,thumb)
elif mode == 22:
    thumb = icon
    ok = m3u_online2(name, url,thumb)
elif mode == 112:
    links(name, url)
else:
    open_list(mode)

xbmcplugin.endOfDirectory(plugin_handle)
