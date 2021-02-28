import os
import sys
import sys,traceback
from os import listdir as os_listdir
#XBMCAddons_error_file="/tmp/XBMCAddons_error"
scripts = "/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/scripts"
if os.path.exists(scripts):
   for name in os_listdir(scripts):
       if "script." in name:
               fold = scripts + "/" + name + "/lib"
               sys.path.append(fold)
