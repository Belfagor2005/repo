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

versione='1.0.1'
# Module: launcher
# Author: TivuStream
# Created on: 22.02.2021
# Last update: 03.09.2021
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
import logging
import xbmcgui
import xbmc
import os
import xbmcplugin
import xbmcaddon
import json
import re
import xbmcvfs

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]

# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

addon_id = 'plugin.video.tvsxxx'
selfAddon = xbmcaddon.Addon(id=addon_id)
debug = selfAddon.getSetting("debug")
testoLog = "";

viewmode=None

PY3 = False
try:
    from urllib.parse import urlencode, parse_qsl
    PY3 = True; unicode = str; unichr = chr; long = int

except:
    from urlparse import urlparse, parse_qsl
    from urllib import urlencode, quote


def logga(mess):
    global testoLog
    if debug == "on":
        testoLog += mess+"\n";


def makeRequest(url, hdr=None):
    logga('Try to open '+url)
    html = ""
    if PY3:
	    import urllib.request as myRequest
    else:
	    import urllib2 as myRequest

    pwd = selfAddon.getSetting("password")
    version = selfAddon.getAddonInfo("version")

    if hdr is None:
        ua = "TivuStreamXxX@@"+version+"@@"+pwd
        hdr = {"User-Agent" : ua}
    try:
        req = myRequest.Request(url, headers=hdr)
        response = myRequest.urlopen(req)
        html = response.read().decode('utf-8')
        response.close()
    except:
        logga('Error to open url')
        pass

    return html


def getSource():
    startUrl = "https://tivustream.website/urls/disclxxx"
    try:
        strSource = makeRequest(startUrl)
        if strSource is None or strSource == "":
            logga('We failed to get source from '+startUrl)
            strSource = getTxtMessage("um.txt")
        else:
            logga('OK SOURCE ')
    except:
        logga('Errore getSource')
        strSource = getTxtMessage("um.txt")
        pass

    jsonToItems(strSource)


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def getTxtMessage(vName):
    home = ''
    if PY3:
        home = xbmc.translatePath(selfAddon.getAddonInfo('path'))
    else:
        home = xbmc.translatePath(selfAddon.getAddonInfo('path').decode('utf-8'))
    fPath = os.path.join(home, vName)
    resF = open(fPath)
    file_content = resF.read()
    resF.close()
    return file_content



def getExternalJson(strPath):
    strSource = makeRequest(strPath)
    jsonToItems(strSource)



def jsonToItems(strJson):
    global viewmode
    dataJson = json.loads(strJson)
    xbmcplugin.setContent(_handle, 'videos')
    try:
        nvs = dataJson['name']
        if nvs == addon_id:
            vS = dataJson['groups'][0]["stations"][0]["url"]
            if not vS.startswith("http"):
                return jsonToItems(getTxtMessage(vS))
            return getExternalJson(vS)
    except:
        pass

    try:
        viewmode = dataJson['SetViewMode']
        skin_name = xbmc.getSkinDir()
        logga("setting view mode for "+skin_name+" on "+viewmode)
        #xbmc.executebuiltin("Container.SetViewMode("+viewmode+")")
    except:
        logga('no view mode')
        pass

    try:
        arrChan = dataJson['channels']
        logga("OK CHANNELS")
        return jsonToChannels(strJson)
    except:
        logga('no channels. GetItems')
        pass

    for item in dataJson["items"]:
        titolo = "NO TIT"
        thumb = "https://www.andreisfina.it/wp-content/uploads/2018/12/no_image.jpg"
        fanart = "https://www.andreisfina.it/wp-content/uploads/2018/12/no_image.jpg"
        genre = "generic"
        info = ""
        regExp = ""
        resolverPar = "no_par"
        link = ""

        extLink = False
        extLink2 = False
        is_folder = False
        is_magnet = False
        is_myresolve = False
        is_regex = False
        is_m3u = False
        is_chrome = False
        is_yatse = False
        is_pvr = False
        is_log = False
        is_copyXml = False
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

        if 'myresolve' in item:
            is_myresolve = True
            is_folder = True
            link = item["myresolve"]
            if "@@" in link:
                arrT=link.split("@@")
                link=arrT[0]
                resolverPar=arrT[1]
            elif ":" in link:
                arrT=link.split(":")
                link=arrT[0]
                resolverPar=arrT[1]

        if 'regexPage' in item:
            is_regex = True
            link = item["regexPage"]
            if 'regexExpres' in item:
                regExp = item["regexExpres"]

        if 'chrome' in item:
            is_chrome = True
            is_folder = True
            link = item["chrome"]

        if 'yatse' in item:
            is_yatse = True
            is_folder = True
            link = item["yatse"]

        if 'm3u' in item:
            is_m3u = True
            is_folder = True
            link = item["m3u"]

        if 'magnet' in item:
            is_magnet = True
            link = item["magnet"]

        if 'pvr' in item:
            is_pvr = True
            link = item["pvr"]

        if 'log' in item:
            is_log = True
            is_folder = True
            link = "ignore"

        if 'copyXml' in item:
            is_copyXml = True
            is_folder = True
            link = "ignore"

        list_item = xbmcgui.ListItem(label=titolo)
        list_item.setInfo('video', {'title': titolo,'genre': genre,'mediatype': 'video'})
        list_item.setArt({'thumb': thumb, 'icon': thumb, 'fanart': fanart})

        url = ""

        if extLink == True:
            url = get_url(action='getExtData', url=link)
        elif extLink2 == True:
            url = get_url(action='getExtData2', url=link)
        elif is_regex == True:
            list_item.setProperty('IsPlayable', 'true')
            url = get_url(action='regex', url=link, exp=regExp)
        elif is_myresolve == True:
            url = get_url(action='myresolve', url=link, parIn=resolverPar)
        elif is_pvr == True:
            url = get_url(action='pvr', url=link)
        elif is_log == True:
            url = get_url(action='log', url=link)
        elif is_m3u == True:
            url = get_url(action='m3u', url=link)
        elif is_copyXml == True:
            url = get_url(action='copyXml', url=link)
        elif is_yatse == True:
            list_item.setProperty('IsPlayable', 'true')
            url = get_urlYatse(action='share', type='unresolvedurl', data=link)
        elif is_magnet == True:
            list_item.setProperty('IsPlayable', 'true')
            url = get_urlMagnet(uri=link)
        elif is_chrome == True:
            url = get_urlChrome(mode='showSite', stopPlayback='no', kiosk='no', url=link)
        else:
            if 'apk' in item:
                logga('APK MODE')
                list_item.setProperty('IsPlayable', 'true')
                is_folder = True
                apkName=item["apk"]
                url = get_url(action='apk', url=link, apk=apkName)
            else:
                list_item.setProperty('IsPlayable', 'true')
                if not link.startswith("plugin://plugin"):
                    url = get_url(action='play', url=link)
                else:
                    url = get_url(action='plugin', url=link)

        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.endOfDirectory(_handle)

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def get_urlMagnet(**kwargs):
    return '{0}?{1}'.format("plugin://plugin.video.elementum/play", urlencode(kwargs))

def get_urlChrome(**kwargs):
    return '{0}?{1}'.format("plugin://plugin.program.browser.launcher/", urlencode(kwargs))

def get_urlYatse(**kwargs):
    return '{0}?{1}'.format("plugin://script.mandra.kodi/", urlencode(kwargs))

def parameters_string_to_dict(parameters):
    params = dict(parse_qsl(parameters.split('?')[1]))
    return params

def jsonToChannels(strJson):
    channelsArray = json.loads(strJson)
    window = xbmcgui.Window(10000)
    window.setProperty("chList", strJson)
    xbmcplugin.setContent(_handle, 'videos')
    for channel in channelsArray["channels"]:
        titolo = "NO TIT"
        thumb = "https://www.andreisfina.it/wp-content/uploads/2018/12/no_image.jpg"
        fanart = "https://www.andreisfina.it/wp-content/uploads/2018/12/no_image.jpg"
        genre = "generic"
        info = ""
        link = ""

        if 'name' in channel:
            titolo = channel["name"]

        if 'thumbnail' in channel:
            thumb = channel["thumbnail"]

        if 'fanart' in channel:
            fanart = channel["fanart"]

        if 'info' in channel:
            info = channel["info"]

        list_item = xbmcgui.ListItem(label=titolo)
        list_item.setInfo('video', {'title': titolo,'genre': genre,'mediatype': 'video'})
        list_item.setArt({'thumb': thumb, 'icon': thumb, 'fanart': fanart})
        url = get_url(action='getChannel', url=titolo)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.endOfDirectory(_handle)
   
def channelToItems(strChName, _handle):
    window = xbmcgui.Window(10000)
    strJson = window.getProperty("chList")
    channelsArray = json.loads(strJson)
    xbmcplugin.setContent(_handle, 'videos')
    for channel in channelsArray["channels"]:
        titolo = channel["name"]
        if titolo == strChName:
            logga("FOUND CH: "+titolo)
            jsonToItems(json.dumps(channel))


def simpleRegex(page, find):
    html = makeRequest(page)
    if PY3:
        html = html.decode('utf-8')		
    urlSteam = re.findall(find, html)[0]
    return urlSteam

def callReolver(metodo, parametro):
    import myResolver
    retVal = myResolver.run(metodo, parametro)
    xbmcplugin.setContent(_handle, 'videos')
    thumb="https://cdn.pixabay.com/photo/2012/04/12/20/56/play-30619_640.png"
    fanart="https://interrogati.it/wp-content/uploads/2019/10/xxx.png"
    if isinstance(retVal, list):
        numLink=1
        
        for linkTmp in retVal:
            newList=list(retVal[0])
            newLink=newList[0]
            logga("Stream_Url ==> " + newLink)
            newTit="[COLOR lime]PLAY LINK "+str(numLink)+" ("+newLink[0:4]+")[/COLOR]"
            list_item = xbmcgui.ListItem(label=newTit)
            list_item.setInfo('video', {'title': newTit,'genre': 'generic','mediatype': 'video'})
            list_item.setArt({'thumb': thumb, 'icon': thumb, 'fanart': fanart})
            list_item.setProperty('IsPlayable', 'true')
            url = get_url(action='play', url=newLink)
            xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
            numLink += 1
    else:
        logga("StreamUrl ==> " + retVal)
        newTit="[COLOR lime]PLAY LINK ("+retVal[0:4]+")[/COLOR]"
        list_item = xbmcgui.ListItem(label=newTit)
        list_item.setInfo('video', {'title': newTit,'genre': 'generic','mediatype': 'video'})
        list_item.setArt({'thumb': thumb, 'icon': thumb, 'fanart': fanart})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', url=retVal)
        xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
    xbmcplugin.endOfDirectory(_handle)

def uploadLog():
    from xbmcaddon import Addon
    addon_log_uploader = None
    try:
        addon_log_uploader = Addon('script.kodi.loguploader')
    except:
        logga.info('loguploader seems to be not installed or disabled')

    if not addon_log_uploader:
        xbmc.executebuiltin('InstallAddon(script.kodi.loguploader)', wait=True)
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "script.kodi.loguploader", "enabled": true }}')
        try:
            addon_log_uploader = Addon('script.kodi.loguploader')
        except:
            logga.info('Logfile Uploader cannot be found')

    if not addon_log_uploader:
        logga('Cannot send log because Logfile Uploader cannot be found')
        return False

    xbmc.executebuiltin('RunScript(script.kodi.loguploader)')
    return True

def checkMsgOnLog():
    LOGPATH = xbmc.translatePath('special://logpath')
    log_file = os.path.join(LOGPATH, 'kodi.log')
    if os.path.exists(log_file)==True:
        try:
            logF = open(log_file)
            log_content = logF.read()
            logF.close()
            log_msg = re.findall("TVSXXX_DNS",log_content)
            if (log_msg):
                return False
            else:
                return True
        except:
            return True

#CONTROLLO VERSIONI FILES
def checkResolver():
    home = ''
    if PY3:
        home = xbmc.translatePath(selfAddon.getAddonInfo('path'))
    else:
        home = xbmc.translatePath(selfAddon.getAddonInfo('path').decode('utf-8'))
    resolver_file = os.path.join(home, 'myResolver.py')
    if os.path.exists(resolver_file)==True:
        resF = open(resolver_file)
        resolver_content = resF.read()
        resF.close()
        local_vers = preg_match(resolver_content, "versione='(.*)'")
        logga('local_vers '+local_vers)
        remoteResolverUrl = "https://tivustream.website/urls/xxxrespy"
        strSource = makeRequest(remoteResolverUrl)
        if strSource is None or strSource == "":
            logga('We failed to get source from '+remoteResolverUrl)
            remote_vers = local_vers
        else:
            # if PY3:
                # strSource = strSource.decode('utf-8')		
            remote_vers = preg_match(strSource, "versione='(.*)'")
        logga('remote_vers '+remote_vers)
        if local_vers != remote_vers:
            logga('TRY TO UPDATE VERSION')
            f = open(resolver_file, "w")
            f.write(strSource)
            f.close()
            logga('VERSION UPDATE')

def runApk(apkName, apkPar):
    xbmc.executebuiltin('StartAndroidActivity("'+apkName+'", "android.intent.action.VIEW", "", "'+apkPar+'")')

def getPvr():
    myPvr = None
        
    if not os.path.exists(xbmc.translatePath('special://home/addons/pvr.iptvsimple')) and not os.path.exists(xbmc.translatePath('special://xbmcbinaddons/pvr.iptvsimple')):
        xbmc.executebuiltin('InstallAddon(pvr.iptvsimple)', wait=True)
    
    pvr_enabled = '"enabled":true' in xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params":{"addonid":"pvr.iptvsimple", "properties": ["enabled"]}}')
    if (not pvr_enabled):
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "pvr.iptvsimple", "enabled": true }}')
    
    myPvr = xbmcaddon.Addon(id='pvr.iptvsimple')
    return myPvr

def setPvr(urlM3u):
    try:
        pvrSimpleTv=getPvr()
        
        if PY3:
            xbmc.executebuiltin('xbmc.StopPVRManager')
        else:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "pvr.iptvsimple", "enabled": false }}')

        if pvrSimpleTv.getSetting('m3uPathType') != '1': 
            pvrSimpleTv.setSetting('m3uPathType', '1')
        pvrSimpleTv.setSetting('epgUrl','')
        pvrSimpleTv.setSetting('m3uUrl', urlM3u)

        xbmc.sleep(500)

        if PY3:
            xbmc.executebuiltin('xbmc.StartPVRManager')
        else:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "pvr.iptvsimple", "enabled": true }}')
            xbmc.sleep(500)
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "pvr.iptvsimple", "enabled": false }}')
            xbmc.sleep(500)
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id":1, "method": "Addons.SetAddonEnabled", "params": { "addonid": "pvr.iptvsimple", "enabled": true }}')
        
        dialog = xbmcgui.Dialog()
        return dialog.ok("TivuStream XxX", "PVR configurato correttamente.")
    except Exception as err:
        errMsg="ERRORE: {0}".format(err)
        raise Exception(errMsg)


def checkDns():
    logging.warning("TVSXXX_DNS")

def saveFile(fileName, text):
    try:
	    f = xbmcvfs.File(fileName, 'w')
	    f.write(text)
	    f.close()
    except:
	    return False
    return True

def preg_match(data, patron, index=0):
    try:
        matches = re.findall(patron, data, flags=re.DOTALL)
        return matches[index]
    except:
        return ""

def m3u2json(src):
    import re
    m3uSource = makeRequest(src)
    if m3uSource is None or m3uSource == "":
        logga('We failed to get source from '+src)
    else:
        if PY3:
            m3uSource = m3uSource.decode('utf-8')		
    
    #regex = r'#EXTINF:.*?tvg-logo=\"([^\"]+|)\".*?,(.*?)$\s(http.*?//.*?)$'
    regex = r'#EXTINF:(.*?),(.*?)$\s(http.*?//.*?)$'	
    matches = re.compile(regex, re.MULTILINE).findall(m3uSource)
    strJson = '{"items":['
    numIt=0
    for match in matches:
        img = str(match[0]).strip()
        regex2= r'.*?tvg-logo="(.*?)"'
        urlImg=preg_match(img, regex2)
        if (urlImg == ""):
            img = "https://e7.pngegg.com/pngimages/349/361/png-clipart-silver-and-blue-tv-digital-art-television-channel-card-sharing-iptv-front-splash-background-cartoon-tv-television-blue-thumbnail.png"
        else:
            img = urlImg

        title = str(match[1]).strip()
        link = str(match[2]).strip()

        if (numIt > 0):
            strJson += ','
        strJson += '{'
        strJson += '"title":"'+title+'",'
        strJson += '"thumbnail":"'+img+'",'
        strJson += '"fanart":"https://omgeeky.com/wp-content/uploads/2021/03/M3U-playlist-URL.jpg",'
        if link.endswith(".m3u"):
            strJson += '"externallink":"'+link+'",'
        else:
            strJson += '"link":"'+link+'",'
        strJson += '"info":"NO INFO"'
        strJson += '}'
        numIt += 1

    strJson += ']}'
    logga(strJson)
    jsonToItems(strJson)



def run():
    try:
        if not sys.argv[2]:
            logga("=== ADDON START ===")

            if (checkMsgOnLog()):
                checkDns()
                checkResolver()

            getSource()
        else:
            params = parameters_string_to_dict(sys.argv[2])
            action =  params['action']
            url =  params['url']
            logga("ACTION ==> "+action)

            if action == 'getExtData':
                getExternalJson(url)
            elif action == 'getExtData2':
                clipB=""
                keyboard = xbmc.Keyboard(clipB,'Insert string')
                keyboard.doModal()
                if not (keyboard.isConfirmed() == False):
                    userInput = keyboard.getText()
                    if not (userInput == ''):
                        strUrl = url + userInput.replace(" ", "+")
                        logga("GET JSON FROM: "+strUrl)
                        getExternalJson(strUrl)
                    else:
                        logga("NO INPUT")
                        mesNoInput='{"SetViewMode":"500","items":[{"title":"[COLOR red]NO INPUT[/COLOR]","link":"ignore","thumbnail":"https://e7.pngegg.com/pngimages/56/148/png-clipart-computer-icons-wrong-miscellaneous-blue-thumbnail.png","fanart":"https://interrogati.it/wp-content/uploads/2019/10/xxx.png","info":"NO INPUT"}]}'
                        jsonToItems(mesNoInput)
                else:
                    logga("EXIT KEYBOARD")
                    mesNoInput='{"SetViewMode":"500","items":[{"title":"[COLOR red]NO INPUT[/COLOR]","link":"ignore","thumbnail":"https://e7.pngegg.com/pngimages/56/148/png-clipart-computer-icons-wrong-miscellaneous-blue-thumbnail.png","fanart":"https://interrogati.it/wp-content/uploads/2019/10/xxx.png","info":"NO INPUT"}]}'
                    jsonToItems(mesNoInput)
            elif action == 'apk':
                apkN =  params['apk']
                logga("RUN APK: "+apkN)
                runApk(apkN, url)
            elif action == 'getChannel':
                logga("OPEN CHANNEL: "+url)
                channelToItems(url, _handle)
            elif action == 'regex':
                express =  params['exp']
                logga("REGEX: "+url+" - "+express)
                url = simpleRegex(url, express)
                play_video(url)
            elif action == 'myresolve':
                parIn =  params['parIn']
                logga("MyResolver: "+url+" - "+parIn)
                callReolver(url, parIn)
            elif action == 'openSettings':
                selfAddon.openSettings()
                xbmcgui.Dialog().ok('[B][COLOR yellow]AVVISO[/COLOR][/B]','[COLOR lime]CHIUDI KODI E APRI DI NUOVO PER AGGIORNARE IMPOSTAZIONI[/COLOR]')
                xbmc.executebuiltin("XBMC.Container.Refresh()")
            elif action == 'plugin':
                logga("CALL PLUGIN: "+url)
                url2=url.replace("plugin://", "")
                url3=url2.split("?")
                pl=""
                par=""
                if ('?' in url):
                    pl=url3[0].replace("/", "")
                    par=url3[1]
                    logga("plug: "+pl+" --> "+par)
                    xbmc.executebuiltin("RunPlugin("+url+")")
                else:
                    pl=url3[0].replace("/", "")
                    logga("onlyplugin: "+pl)
                    xbmc.executebuiltin('RunAddon("'+pl+'")')
            elif action == 'play':
                play_video(url)
            elif action == 'm3u':
                m3u2json(url)
            elif action == 'pvr':
                setPvr(url)
            elif action == 'log':
                uploadLog()
            else:
                raise Exception('Invalid paramstring: {0}!'.format(params))
    except Exception as err:
        errMsg="ERRORE: {0}".format(err)
        raise Exception(errMsg)

    if not viewmode==None:
        logga("setting view mode")
        xbmc.executebuiltin("Container.SetViewMode("+viewmode+")")
        logga("setting view mode again")
        xbmc.executebuiltin("Container.SetViewMode("+viewmode+")")

    if debug == "on":
        logging.warning("MANDRA_LOG: \n"+testoLog)