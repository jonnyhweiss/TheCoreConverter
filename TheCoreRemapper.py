##################################################
#
# Filename: TheCoreRemapper.py
# Author: Jonny Weiss
# Description: Script to take the LM layouts of TheCore and generate the other 44 layouts.
# Change Log:
#   9/25/12 - Created
#   9/26/12 - Finished initial functionality
#
################################################## 
from ConfigParser import SafeConfigParser

GLOBAL = -1
LMM = 0
RMM = 1
RM = 2

CAMERA_KEYS = ['CameraSave0', 'CameraSave1', 'CameraSave2', 'CameraSave3', 'CameraSave4', 'CameraSave5', 'CameraSave6', 'CameraSave7',
               'CameraView0', 'CameraView1', 'CameraView2', 'CameraView3', 'CameraView4', 'CameraView5', 'CameraView6', 'CameraView7']

CONTROL_GROUP_KEYS = ['ControlGroupAppend0', 'ControlGroupAppend1', 'ControlGroupAppend2', 'ControlGroupAppend3', 'ControlGroupAppend4', 'ControlGroupAppend5', 'ControlGroupAppend6', 'ControlGroupAppend7', 'ControlGroupAppend8', 'ControlGroupAppend9', 
                      'ControlGroupAssign0', 'ControlGroupAssign1', 'ControlGroupAssign2', 'ControlGroupAssign3', 'ControlGroupAssign4', 'ControlGroupAssign5', 'ControlGroupAssign6', 'ControlGroupAssign7', 'ControlGroupAssign8', 'ControlGroupAssign9',
                      'ControlGroupRecall0', 'ControlGroupRecall1', 'ControlGroupRecall2', 'ControlGroupRecall3', 'ControlGroupRecall4', 'ControlGroupRecall5', 'ControlGroupRecall6', 'ControlGroupRecall7', 'ControlGroupRecall8', 'ControlGroupRecall9']

# Add to this please.
GENERAL_KEYS = ['Music','Sound','PTT','ChatCancel','ChatRecipient','DialogDismiss','MenuAchievements','MenuGame','MenuMessages',
                'LeaderResources','LeaderIncome','LeaderSpending','LeaderUnits','LeaderUnitsLost','LeaderProduction','LeaderArmy',
                'LeaderAPM','LeaderCPM','ObserveAllPlayers','ObserveAutoCamera','ObserveClearSelection','ObservePlayer0','ObservePlayer1',
                'ObservePlayer2','ObservePlayer3','ObservePlayer4','ObservePlayer5','ObservePlayer6','ObservePlayer7','ObservePlayer8',
                'ObservePlayer9','ObservePlayer10','ObservePlayer11','ObservePlayer12','ObservePlayer13','ObservePlayer14','ObservePlayer15',
                'ObserveSelected', 'ObserveStatusBars','StatPanelResources','StatPanelArmySupply','StatPanelUnitsLost','StatPanelAPM','StatPanelCPM',
                'ToggleWorldPanel', 'CinematicSkip','AlertRecall','CameraFollow','GameTooltipsOn','IdleWorker','MinimapColors','MinimapPing',
                'MinimapTerrain','PauseGame','QuickPing','QuickSave','ReplayPlayPause','ReplayRestart','ReplaySkipBack','ReplaySkipNext','ReplaySpeedDec',
                'ReplaySpeedInc','ReplayStop','ReplayHide','SelectionCancelDrag','SubgroupNext','SubgroupPrev','TeamResources','TownCamera','WarpIn',
                'Cancel', 'Rally', 'Move', 'RallyEgg']

HAND_SHIFT_EXCLUDE = ['AllowSetConflicts']

SAME_CHECKS = [['Pylon/Probe','SupplyDepot/SCV'],
              ['Gateway/Probe','SpawningPool/Drone','Barracks/SCV'],
              ['Assimilator/Probe','Extractor/Drone','Refinery/SCV'],
              ['PhotonCannon/Probe','SpineCrawler/Drone','Bunker/SCV'],
              ['Nexus/Probe','Hatchery/Drone','CommandCenter/SCV'],
              ['Forge/Probe','EvolutionChamber/Drone','EngineeringBay/SCV']]

# Read the settings
settings_parser = SafeConfigParser()
settings_parser.optionxform=str
settings_parser.read('MapDefinitions.ini')

race_dict = {"P": 0,
             "T": 1,
             "Z": 2,
             "R": 3}

prefix = settings_parser.get("Filenames", "Prefix")
suffix = settings_parser.get("Filenames", "Suffix")
races = ["R","T","Z","P"]
layouts = ["LMM", "RMM", "RM"]
layoutIndices = {"LMM": 0,
                 "RMM": 1,
                 "RM": 2}

def parse_pair(key, values, map_name, index):
    parsed = ""
    first = True
    for value in values:
        bits = value.split("+")
        if not first:
            parsed += ","
        last_bit = bits[len(bits)-1]
        try:
            if index < 0:
                bits[len(bits)-1] = settings_parser.get(map_name, last_bit)
            else:
                bits[len(bits)-1] = settings_parser.get(map_name, last_bit).split(",")[index]
        except:
            last_bit = last_bit # Do nothing
        parsed += "+".join(bits)
        first = False
    return parsed

def generate_layout(filename, race, layout, layoutIndex):
    hotkeys_file = open(filename, 'r')
    output = ""
    for line in hotkeys_file:
        line = line.strip()
        if len(line) == 0 or line[0] == "[":
            output += line + "\n"
            continue
        pair = line.split("=")
        key = pair[0]
        values = pair[1].split(",")
        output += key + "="
        
        if key in CAMERA_KEYS:
            if "R" in layout:
                output += parse_pair(key, values, 'GlobalMaps', GLOBAL)
            else:
                output += pair[1]
        elif key in CONTROL_GROUP_KEYS:
            output += parse_pair(key, values, race + 'CGMaps', layoutIndex)
        elif key in GENERAL_KEYS:
            if "R" in layout:
                output += parse_pair(key, values, 'GlobalMaps', GLOBAL)
            else:
                output += pair[1]
        else:
            try:
                maptypes = settings_parser.get("MappingTypes", key).split(",")
                output += parse_pair(key, values, race + maptypes[race_dict[race]] + "Maps", layoutIndex)
            except:
                output += pair[1]
        output += "\n"
    hotkeys_file.close()
    newfilename = filename.replace("LM", layout)
    fileio = open(newfilename, 'w')
    fileio.write(output)
    fileio.close()
    return newfilename

def shift_hand_size(filename, shift_right, hand_size):
    hotkeys_file = open(filename, 'r')
    output = ""
    for line in hotkeys_file:
        line = line.strip()
        if len(line) == 0 or line[0] == "[":
            output += line + "\n"
            continue
        pair = line.split("=")
        key = pair[0]
        values = pair[1].split(",")
        output += key + "="
        
        if key in HAND_SHIFT_EXCLUDE:
            output += pair[1]
        elif shift_right:
            output += parse_pair(key, values, 'ShiftRightMaps', GLOBAL)
        else:
            output += parse_pair(key, values, 'ShiftLeftMaps', GLOBAL)        
        output += "\n"
    hotkeys_file.close()
    newfilename = ""
    if "MM " in filename:
        newfilename = filename.replace("MM ", hand_size + "M ")
    else:
        newfilename = filename.replace("M ", hand_size + " ")
    fileio = open(newfilename, 'w')
    fileio.write(output)
    fileio.close()
    return newfilename

def verify_file(filename):
    hotkeys_file = open(filename, 'r')
    all_items = settings_parser.items('MappingTypes')
    dict = {}
    for item in all_items:
        dict[item[0]] = [False, "", item[0]]
    for line in hotkeys_file:
        line = line.strip()
        if len(line) == 0 or line[0] == "[":
            continue
        pair = line.split("=")
        key = pair[0]
        dict[key] = [True, pair[1], key]
        
    count = 0
    for item in dict:
        if not dict[item][0]:
            count += 1
    if count > 0:        
        print filename + " is missing " + str(count) + " hotkeys: "
        #print "NOTE: Capitalization is not correct. Check settings.ini for correct capitalization."
        for item in dict:
            if not dict[item][0]:
                print dict[item][2]
    else:
        print filename + " contains all hotkeys."
    for same_set in SAME_CHECKS:
        mismatched = False
        value = dict[same_set[0]][1]
        for item in same_set:
            if not dict[item][1] == value:
                mismatched = True
        if mismatched:
            print "---- Mismatched values ----"
            for item in same_set:
                print item + " = " + dict[item][1]
    print ""
# Main part of the script. For each race, generate each layout, and translate that layout for large and small hands.
for race in races:
    filename = prefix + " " + race + "LM " + suffix
    verify_file(filename)
    shift_hand_size(filename, True, "L")
    shift_hand_size(filename, False, "S")
    for layout in layouts:
        index = layoutIndices[layout]
        layout_filename = generate_layout(filename, race, layout, index)
        if "R" in layout:
            shift_hand_size(layout_filename, True, "S")
            shift_hand_size(layout_filename, False, "L")
        else:
            shift_hand_size(layout_filename, True, "L")
            shift_hand_size(layout_filename, False, "S")