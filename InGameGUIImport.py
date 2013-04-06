##################################################
#
# Filename: InGameGUIImport.py
# Author: Jonny Weiss
# Description: Script to incorporate changes to the 4 *LM layouts into TheCoreSee.ini
# Change Log:
#   4/06/13 - Created
#
################################################## 
from configparser import SafeConfigParser
import os

seed_parser = SafeConfigParser()
seed_parser.optionxform=str
seed_parser.read('TheCoreSeed.ini')

settings_parser = SafeConfigParser()
settings_parser.optionxform=str
settings_parser.read('MapDefinitions.ini')

prefix = settings_parser.get("Filenames", "Prefix")
suffix = settings_parser.get("Filenames", "Suffix")
races = ["P","T","Z","R"]

class Hotkey:
    def __init__(self, name, P, T, Z, R, default):
        self.name = name
        self.P = P
        self.T = T
        self.Z = Z
        self.R = R
        self.default = default
        
    def __str__(self):
        if (self.P == self.T and self.P == self.Z and self.P == self.R):
            return self.name + "=" + self.P + "|"        
        return self.name + "=" + self.P + "|" + self.T + "|" + self.R + "|" + self.Z + "|" + self.default
 
def SaveSeedFile(hotkeys, commands):
    seed_file = open('TheCoreSeed.ini', 'w')
    seed_file.write("[Settings]\n")
    seed_file.write("AllowSetConflicts=1\n\n")
    seed_file.write("[Hotkeys]\n")
    for hotkey in hotkeys:
        seed_file.write(str(hotkey) + "\n")
    seed_file.write("\n[Commands]\n")
    for command in commands:
        seed_file.write(str(command) + "\n")
    seed_file.close()
    
def get_hotkey(pair):
    values = pair[1].split("|")
    length = len(values)
    P = values[0]
    T = Z = R = default = ""
    if length == 2:
        T = values[0]
        Z = values[0]
        R = values[0]
    if length > 2:
        Z = values[2]
    if length > 3:
        R = values[3]
    if length > 4:
        default = values[4]
    hotkey = Hotkey(name=pair[0],P=P,T=T,Z=Z,R=R,default=default)
    return hotkey

def ImportChanges():
    parsers = {}
    for r in races:
        hotkeyfile_parser = SafeConfigParser()
        hotkeyfile_parser.optionxform=str
        hotkeyfile_parser.read(prefix + " " + r + "LM " + suffix)
        parsers[r] = hotkeyfile_parser
    
    hotkeys = []
    for item_pair in seed_parser.items("Hotkeys"):
        hotkey = get_hotkey(item_pair)
        for r in races:
            value = hotkey.default
            if parsers[r].has_option("Hotkeys", hotkey.name):
                value = parsers[r].get("Hotkeys", hotkey.name)
            setattr(hotkey, r, value)
        hotkeys.append(hotkey)
    
    commands = []
    for item_pair in seed_parser.items("Commands"):
        hotkey = get_hotkey(item_pair)
        for r in races:
            if parsers[r].has_option("Commands", hotkey.name):
                value = parsers[r].get("Commands", hotkey.name)
                setattr(hotkey, r, value)
        commands.append(hotkey)
    
    SaveSeedFile(hotkeys, commands)
        
ImportChanges()