# -*- coding: utf-8 -*-
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
import sys
from xml.dom import minidom
import resources.lib.utils as utils

PY3 = sys.version_info.major >= 3

if PY3:
    import urllib.request as urllib2
else:
    import urllib2


class TGR:
    _baseurl = "http://www.tgr.rai.it"
    
    def getProgrammes(self):
        url = "http://www.tgr.rai.it/dl/tgr/mhp/home.xml"
        try:
            xmldata = urllib2.urlopen(url).read()
            xmldata = utils.checkStr(xmldata)
            dom = minidom.parseString(xmldata)

            programmes = []
            for node in dom.getElementsByTagName('item'):
                item = {}
                # behaviour = {region, select, list}
                item["behaviour"] = node.attributes["behaviour"].value
                item["title"] = node.getElementsByTagName('label')[0].childNodes[0].data
                for url in  node.getElementsByTagName('url'):
                    if url.attributes["type"].value == "image":
                        item["image"] = self._baseurl + url.childNodes[0].data
                    elif url.attributes["type"].value == "list":
                        item["url"] = self._baseurl + url.childNodes[0].data
                programmes.append(item)

            return programmes
        
        except urllib2.HTTPError:
            return []
     
    def getList(self, url):
        
        try:
            xmldata = urllib2.urlopen(url).read()
            xmldata = utils.checkStr(xmldata)
            dom = minidom.parseString(xmldata)

            items = []
            for node in dom.getElementsByTagName('item'):
                item = {}
                # behaviour = {list, video}
                item["behaviour"] = node.attributes["behaviour"].value
                item["title"] = node.getElementsByTagName('label')[0].childNodes[0].data
                for url in  node.getElementsByTagName('url'):
                    foundUrl = False
                    if url.attributes["type"].value == "list":
                        item["url"] = self._baseurl + url.childNodes[0].data
                        foundUrl = True
                    elif url.attributes["type"].value == "video":
                        if url.attributes["type"].value == "video":
                            item["url"] = url.childNodes[0].data
                            foundUrl = True
                    if foundUrl:
                        items.append(item)

            return items

        except urllib2.HTTPError:
            return []
        
