Pre-Requisites: You must have Python installed to run this script.

Instructions for Use:

1. Make sure MapDefinitions.ini is configured properly

  a. Make sure the filename suffix matches the version number.

  b. Make any changes to the mappings, as necessary. The [MappingTypes] map
     individual unit commands to the types of mapping used for each race, as in the
     More Maps tab of the Data Document. Note the format of the mappings.

  [MappingTypes] are of the form BlizzardCommand = P,T,Z,R
     P,T,Z,R are one of A (Ability), I (Integrated), BB (Build Basic), MF (MF Unit Ability), TP (Terran Unit Production)
     P,T,Z,R correspond to the mappings to be used for each race.

  [GlobalMaps] are of the form L = R
     L is the key in the left-handed layouts.
     R is the key in the right-handed layouts.

  [ShiftLeftMaps] and [ShiftRightMaps] are of the form B = A
     B is the key before the shift.
     A is the key after the shift (the key that is mapped to)

  All of the other maps are of the form LM = LMM,RMM,RM
     It is a mapping from LM to the other 3 layouts.
     [P/T/Z/RCGMaps] are the control group maps.
     [P/T/Z/R A/I/BB/MF/TP Maps] are the maps that are referenced in [MappingTypes]

2. Make sure that the 4 LM hotkey files are in the same folder as the script.

3. Open a command prompt and run:

   python TheCoreRemapper.py

   The script will generate all of the new hotkey files, and also alert you if your seed files were missing some commands.
   If the files were missing commands, this means that the commands are the same as the Blizzard defaults, and must be added
   to the hotkey files to make the script function properly (only hotkeys actually in the .SC2Hotkeys seed files will be remapped)

4. ...

5. Profit!

<3 JDub