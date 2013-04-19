Pre-Requisites: You must have Python 3.0+ installed to run this script.

Brief Overview of Important Files:

1. TheCoreSeed.ini - The single file used to generate all layouts of TheCore. It is structured very similarly to a .SC2Hotkeys file,
with some notable exceptions. Each line can take on 1 of 3 forms. P, T, R, and Z stand for Protoss, Terran, Random, and Zerg, and indicate 
the key used in the left-handed, medium size layout of TheCore. D stands for the Standard default key used for a command. The line formats are:
   a. CommandName=P|T|R|Z|D
   b. CommandName=SharedKey|D (if the keys are the same for each race, don't list them 4 times, just list them once)
   c. CommandName=CommandNameToCopy (useful for campaign keys, this means the keys will be copied from another command)

2. MapDefinitions.ini - This file stores the mappings that are used to convert the left-handed medium layouts to the other layouts. 

  [GlobalMaps] are of the form L = R, and are used for mapping the global hotkeys
     L is the key in the left-handed medium layouts.
     R is the key in the right-handed medium layouts.

  [ShiftLeftMaps] and [ShiftRightMaps] are of the form B = A, and are used for shifting the medium layout one key to the left or right to generate
  the large and small layouts.
     B is the key before the shift.
     A is the key after the shift (the key that is mapped to)

  All of the other maps are of the form LM = LMM,RMM,RM (As of April 2013, LMM and RMM are obsolete)
     It is a mapping from LM to the other 3 layouts.
     [P/T/Z/R CGMaps] are the control group maps.
     [P/T/Z/R AMaps] are the unit ability maps.
     (Obsolete as of April 2013) [P/T/Z/R A/I/BB/MF/TP Maps] are the maps that are referenced in [MappingTypes]

3. KeyboardLayouts.ini - This file stores mappings for alternative keyboard layouts. TheCoreSeed.ini and MapDefinitions.ini store values designed for QWERTY keyboards.
The mappings stored in this file are applied to map from the US QWERTY version of a layout to a different keyboard layout. Each keyboard type layout takes on the form:

   [KeyboardTypeName]
   QWERTYKey=KeyboardTypeKey

The generated layouts get put in a separate folder with the name of the KeyboardType (e.g. USDvorak).

4. InGameGUIImport.py - This file will import changes made to PLM,ZLM,TLM, and RLM into TheCoreSeed.ini. The workflow is:
   a. Copy and paste the *LM.SC2Hotkeys file into your Starcraft 2 Hotkey folder.
   b. Load up SC2 and edit the layouts in game.
   c. Copy and paste the edited files back into TheCoreConverter directory, overwriting the existing ones.
   d. Run python InGameGUIImport.
   e. Verify that the changes made to TheCoreSeed.ini are accurate.
   
The important thing to note about editing files with the in-game editor is that any overlaps between the edited files and the SC2 Standard hotkey layout will be stripped from the file.
This is why TheCoreSeed.ini stores the default Standard layout hotkeys, so that it can fill these back in when you run the InGameGUIImport.

5. TheCoreRemapper.py - This is the script that makes the magic happen. Once you have made appropriate changes to TheCoreSeed.ini (either by using the InGameGUIImport method above or
by editing the text file directly), you can run python TheCoreRemapper.py, and it will generate all layouts of TheCore, and check them for errors.