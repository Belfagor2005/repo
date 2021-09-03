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

import os
import sys
import re
import xbmc
import xbmcaddon
import xbmcgui
import logging


addon_id = 'plugin.video.tvsxxx'
selfAddon = xbmcaddon.Addon(id=addon_id)
debug = selfAddon.getSetting("debug")

PY3 = sys.version_info[0] == 3

def logga(mess):
    if debug == "on":
        logging.warning('TVSXXX_LOG: '+mess)

def checkLauncher():
    home = ''
    if PY3:
        home = xbmc.translatePath(selfAddon.getAddonInfo('path'))
    else:
        home = xbmc.translatePath(selfAddon.getAddonInfo('path').decode('utf-8'))
    launcher_file = os.path.join(home, 'launcher.py')
    if os.path.exists(launcher_file)==True:
        resF = open(launcher_file)
        resolver_content = resF.read()
        resF.close()
        local_vers = re.findall("versione='(.*)'",resolver_content)[0]
        logga('local_vers '+local_vers)
        remoteLauncherUrl = selfAddon.getSetting("baseUrl")
        strSource = makeRequest(remoteLauncherUrl)
        if strSource is None or strSource == "":
            logga('We failed to get source from '+remoteLauncherUrl)
            remote_vers = local_vers
        else:
            # if PY3:
                # strSource = strSource.decode('utf-8')		
            remote_vers = re.findall("versione='(.*)'",strSource)[0]
        logga('remote_vers '+remote_vers)
        if local_vers != remote_vers:
            logga('TRY TO UPDATE VERSION')
            f = open(launcher_file, "w")
            f.write(strSource)
            f.close()
            logga('VERSION UPDATE')

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
                logga("CHECK PASS")
                return False
            else:
                return True
        except:
            return True


if sys.argv[2] == "":
    logga("OPEN ADDON")
    checkLauncher()

logga("PAR - "+sys.argv[2])
try:
    import launcher
    launcher.run()
except Exception as err:
    import traceback
    errMsg="ERRORE: {0}".format(err)
    logging.warning(errMsg+"\nPAR_ERR --> "+sys.argv[2])
    traceback.print_exc()
    dialog = xbmcgui.Dialog()
    mess = "Accidenti!\nSembra esserci qualche errore non gestito.\nSe il problema persiste, prova ad inviare il log."
    dialog.ok("TivuStream XxX", mess)