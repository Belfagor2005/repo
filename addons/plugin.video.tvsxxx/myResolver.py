versione='1.0.0'
# Module: myResolve
# Author: TivuStream
# Created on: 10.04.2021
# Last update: 08.05.2021
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import re, requests, sys, logging
import xbmcplugin
import xbmcgui

PY3 = sys.version_info[0] == 3


def urlsolver(url):
    video_urls = []
    try:
        import resolveurl
    except:
        import urlresolver as resolveurl

    if resolveurl.HostedMediaFile(url).valid_url():
        resolved = resolveurl.resolve(url)
    else:
        dialog = xbmcgui.Dialog()
        mess = "Sorry, ResolveUrl does not support this domain."
        dialog.ok("TivuStream XxX", mess)
        resolved = ""
    logga('video_url '+resolved)
    video_urls.append((resolved, ""))
    return video_urls

def run (action, params=None):
    logging.warning('Run version '+versione)
    commands = {
        'risolvi': urlsolver
    }
    if action in commands:
        return commands[action](params)
    else:
        raise ValueError('Invalid command: {0}!'.action)