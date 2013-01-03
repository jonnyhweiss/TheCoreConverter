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
from configparser import SafeConfigParser
import os

GLOBAL = -1
LMM = 0
RMM = 1
RM = 2

SHOW_HOTS_MISSING = True
SHOW_DUPLICATES = False
VERIFY_ALL = False

CAMERA_KEYS = ['CameraSave0', 'CameraSave1', 'CameraSave2', 'CameraSave3', 'CameraSave4', 'CameraSave5', 'CameraSave6', 'CameraSave7',
               'CameraView0', 'CameraView1', 'CameraView2', 'CameraView3', 'CameraView4', 'CameraView5', 'CameraView6', 'CameraView7']

#ZERG_CONTROL_GROUP_SPECIAL = ['ControlGroupAssign7']

CONTROL_GROUP_KEYS = ['ControlGroupAppend0', 'ControlGroupAppend1', 'ControlGroupAppend2', 'ControlGroupAppend3', 'ControlGroupAppend4', 'ControlGroupAppend5', 'ControlGroupAppend6', 'ControlGroupAppend7', 'ControlGroupAppend8', 'ControlGroupAppend9', 
                      'ControlGroupAssign0', 'ControlGroupAssign1', 'ControlGroupAssign2', 'ControlGroupAssign3', 'ControlGroupAssign4', 'ControlGroupAssign5', 'ControlGroupAssign6', 'ControlGroupAssign7', 'ControlGroupAssign8', 'ControlGroupAssign9',
                      'ControlGroupRecall0', 'ControlGroupRecall1', 'ControlGroupRecall2', 'ControlGroupRecall3', 'ControlGroupRecall4', 'ControlGroupRecall5', 'ControlGroupRecall6', 'ControlGroupRecall7', 'ControlGroupRecall8', 'ControlGroupRecall9']

# Add to this please.
GENERAL_KEYS = ['Music','Sound','PTT','ChatCancel','DialogDismiss','MenuAchievements','MenuGame','MenuMessages',
                'LeaderResources','LeaderIncome','LeaderSpending','LeaderUnits','LeaderUnitsLost','LeaderProduction','LeaderArmy',
                'LeaderAPM','LeaderCPM','ObserveAllPlayers','ObserveAutoCamera','ObserveClearSelection','ObservePlayer0','ObservePlayer1',
                'ObservePlayer2','ObservePlayer3','ObservePlayer4','ObservePlayer5','ObservePlayer6','ObservePlayer7','ObservePlayer8',
                'ObservePlayer9','ObservePlayer10','ObservePlayer11','ObservePlayer12','ObservePlayer13','ObservePlayer14','ObservePlayer15',
                'ObserveSelected', 'ObserveStatusBars','StatPanelResources','StatPanelArmySupply','StatPanelUnitsLost','StatPanelAPM','StatPanelCPM',
                'ToggleWorldPanel', 'CinematicSkip','AlertRecall','CameraFollow','GameTooltipsOn','IdleWorker','MinimapColors','MinimapPing',
                'MinimapTerrain','PauseGame','QuickPing','QuickSave','ReplayPlayPause','ReplayRestart','ReplaySkipBack','ReplaySkipNext','ReplaySpeedDec',
                'ReplaySpeedInc','ReplayStop','ReplayHide','SelectionCancelDrag','SubgroupNext','SubgroupPrev','TeamResources','TownCamera','WarpIn',
                'Cancel','CancelCocoon','CancelMutateMorph','CancelUpgradeMorph',
                'StatusAll','StatusOwner','StatusEnemy','StatusAlly','MenuHelp','NamePanel','ArmySelect','SelectBuilder', 'ToggleVersusModeSides']
# 'ChatRecipient',

HAND_SHIFT_EXCLUDE = ['AllowSetConflicts']

SAME_CHECKS = [['Pylon/Probe','SupplyDepot/SCV','SupplyDepotDrop/SCV'],
               ['Assimilator/Probe','Extractor/Drone','Refinery/SCV','AutomatedRefinery/SCV'],
               ['Gateway/Probe','Barracks/SCV'],
               ['Nexus/Probe','Hatchery/Drone','CommandCenter/SCV','CommandCenterOrbRelay/SCV'],
               ['Forge/Probe','EvolutionChamber/Drone','EngineeringBay/SCV'],
               ['RoboticsFacility/Probe','Factory/SCV'],
               ['Stargate/Probe','Spire/Drone','Starport/SCV'],
               ['TwilightCouncil/Probe','Armory/SCV'],
               ['FleetBeacon/Probe','FusionCore/SCV'],
               ['ProtossGroundWeaponsLevel1/Forge','TerranInfantryWeaponsLevel1/EngineeringBay','TerranInfantryWeaponsUltraCapacitorsLevel1/EngineeringBay','TerranInfantryWeaponsUltraCapacitorsLevel2/EngineeringBay','TerranInfantryWeaponsUltraCapacitorsLevel3/EngineeringBay'],
               ['ProtossGroundArmorLevel1/Forge','TerranInfantryArmorLevel1/EngineeringBay','zerggroundarmor1/EvolutionChamber','TerranInfantryArmorVanadiumPlatingLevel1/EngineeringBay','TerranInfantryArmorVanadiumPlatingLevel2/EngineeringBay','TerranInfantryArmorVanadiumPlatingLevel3/EngineeringBay'],
               ['ProtossAirWeaponsLevel1/CyberneticsCore','TerranShipWeaponsLevel1/Armory','zergflyerattack1'],
               ['TerranShipWeaponsLevel1/Armory','TerranShipWeaponsUltraCapacitorsLevel1/Armory','TerranShipWeaponsUltraCapacitorsLevel2/Armory','TerranShipWeaponsUltraCapacitorsLevel3/Armory'],
               ['ProtossAirArmorLevel1/CyberneticsCore','TerranShipPlatingLevel1/Armory','zergflyerarmor1'],
               ['TerranShipPlatingLevel1/Armory','TerranShipPlatingVanadiumPlatingLevel1/Armory','TerranShipPlatingVanadiumPlatingLevel2/Armory','TerranShipPlatingVanadiumPlatingLevel3/Armory'],
               ['Stim','StimFirebat/Firebat','StimFirebat/DevilDog'],
               ['Heal/Medivac','BonesHeal/Stetmann','NanoRepair/ScienceVessel','MedicHeal/Medic','MercMedicHeal/MercMedic'],
               ['CloakOnBanshee','RogueGhostCloak/Spectre','WraithCloakOn/Wraith'],
               ['CloakOff','WraithCloakOff/Wraith'],
               ['WeaponsFree/Ghost','SpectreWeaponsFree/Spectre'],
               ['GhostHoldFire/Ghost','SpectreHoldFire/Spectre'],
               ['NukeArm/GhostAcademy','SpectreNukeArm/GhostAcademy'],
               ['NukeCalldown/Ghost','SpectreNukeCalldown/Spectre','HeroNukeCalldown/Nova','HeroNukeCalldown/Tosh','OdinNukeCalldown/Odin'],
               ['BunkerLoad','HerculesLoad/Hercules'],
               ['BunkerUnloadAll','HerculesUnloadAll/Hercules'],
               ['Reactor/Barracks','Reactor/BarracksFlying','Reactor/Factory','Reactor/FactoryFlying','Reactor/Starport','Reactor/StarportFlying'],
               ['TechLabBarracks/Barracks','TechLabBarracks/BarracksFlying','TechReactor/Barracks','TechReactor/BarracksFlying','TechLabFactory/Factory','BuildTechLabFactory/FactoryFlying','TechReactor/Factory','TechReactor/FactoryFlying','TechLabStarport/Starport','BuildTechLabStarport/StarportFlying','TechReactor/Starport','TechReactor/StarportFlying'],
               ['Ghost/Barracks','Spectre/Barracks'],
               ['Raven/Starport','BuildScienceVessel/Starport'],
               ['EMP/Ghost','UltrasonicPulse/Spectre'],
               ['Snipe/Ghost','NovaSnipe/Nova','Obliterate/Spectre'],
               ['Lair/Hatchery','Hive/Lair','LurkerDen/HydraliskDen'],
               ['MassRecall/Mothership','MassRecall/Artanis'],
               ['Vortex/Mothership','Vortex/Artanis'],
               ['Mothership/Nexus','MothershipCore/Nexus'],
               ['AutoTurret/Raven','BuildAutoTurret/Raven'],
               ['PointDefenseDrone/Raven','BuildPointDefenseDrone/Raven']]

CONFLICT_CHECKS = [['Probe/Nexus','TimeWarp/Nexus','MothershipCore/Nexus'],#__Town Halls__ #Nexus
                   ['Probe/Nexus','TimeWarp/Nexus','Mothership/Nexus'],
                   ['SelectBuilder','Cancel','Lift','Rally','CommandCenterLoad','CommandCenterUnloadAll','SCV','OrbitalCommand/CommandCenter','UpgradeToPlanetaryFortress/CommandCenter'],#CC
                   ['Cancel','Lift','Rally','SCV','CalldownMULE/OrbitalCommand','SupplyDrop/OrbitalCommand','Scan/OrbitalCommand'],#OC
                   ['Cancel','Rally','CommandCenterLoad','CommandCenterUnloadAll','Attack','StopPlanetaryFortress/PlanetaryFortress','SCV'],#PF
                   ['EvolveVentralSacks','Lair/Hatchery','Larva','overlordspeed','Queen','Rally','RallyEgg','ResearchBurrow'],#Hatch/Lair/Hive
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','GatherProt','ReturnCargo','ProtossBuild/Probe','ProtossBuildAdvanced/Probe'],#__Harvesters__ #Probe
                   ['Assimilator/Probe','CyberneticsCore/Probe','Forge/Probe','Gateway/Probe','Nexus/Probe','PhotonCannon/Probe','Pylon/Probe'],
                   ['DarkShrine/Probe','FleetBeacon/Probe','RoboticsBay/Probe','RoboticsFacility/Probe','Stargate/Probe','TemplarArchive/Probe','TwilightCouncil/Probe'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Repair','GatherProt','ReturnCargo','TerranBuild/SCV','TerranBuildAdvanced/SCV'],#SCV
                   ['Barracks/SCV','Bunker/SCV','CommandCenter/SCV','EngineeringBay/SCV','HiveMindEmulator/SCV','MissileTurret/SCV','PerditionTurret/SCV','Refinery/SCV','SensorTower/SCV','SupplyDepot/SCV'],
                   ['Armory/SCV','Factory/SCV','FusionCore/SCV','GhostAcademy/SCV','MercCompound/SCV','Starport/SCV'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','GatherProt','ReturnCargo','BurrowDown','ZergBuild/Drone','ZergBuildAdvanced/Drone'],#Drone
                   ['BanelingNest/Drone','EvolutionChamber/Drone','Extractor/Drone','Hatchery/Drone','RoachWarren/Drone','SpawningPool/Drone','SporeCrawler/Drone','SpineCrawler/Drone'],
                   ['HydraliskDen/Drone','InfestationPit/Drone','NydusNetwork/Drone','Spire/Drone','UltraliskCavern/Drone'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','Interceptor/Carrier'],#__Protoss Units__ #Carrier
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','PsiStorm/HighTemplar','Feedback/HighTemplar','AWrp'],#HighTemplar
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MassRecall/Mothership','Vortex/Mothership'],#Mothership
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','ResourceStun/Oracle','OracleRevelation/Oracle','PhaseShield/Oracle'],#Oracle
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','GravitonBeam/Phoenix'],#Phoenix
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','ForceField/Sentry','GuardianShield/Sentry','Hallucination/Sentry'],#Sentry
                   ['ArchonHallucination/Sentry','ColossusHallucination/Sentry','HighTemplarHallucination/Sentry','ImmortalHallucination/Sentry','OracleHallucination/Sentry','PhoenixHallucination/Sentry','ProbeHallucination/Sentry','StalkerHallucination/Sentry','VoidRayHallucination/Sentry','WarpPrismHallucination/Sentry','ZealotHallucination/Sentry'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','Blink/Stalker'],#Stalker
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BunkerLoad','BunkerUnloadAll','PhasingMode/WarpPrism','TransportMode/WarpPrism'],#WarpPrism
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','Charge/Zealot'],#Zealot
                   ['ProtossAirWeaponsLevel1/CyberneticsCore','ProtossAirArmorLevel1/CyberneticsCore','ResearchWarpGate/CyberneticsCore','ResearchHallucination/CyberneticsCore'],#__Protoss Buildings__ #CyberneticsCore
                   ['AnionPulseCrystals/FleetBeacon','ResearchInterceptorLaunchSpeedUpgrade/FleetBeacon','ResearchVoidRaySpeedUpgrade/FleetBeacon','SpeedUpgrade/FleetBeacon'],#FleetBeacon
                   ['ProtossGroundWeaponsLevel1/Forge','ProtossGroundArmorLevel1/Forge','ProtossShieldsLevel1/Forge'],#Forge
                   ['Rally','Zealot','Stalker','Sentry','HighTemplar','DarkTemplar','UpgradeToWarpGate/Gateway'],#Gateway
                   ['Rally','Zealot','Stalker','Sentry','HighTemplar','DarkTemplar','MorphBackToGateway/WarpGate'],
                   ['ResearchGraviticDrive/RoboticsBay','ResearchExtendedThermalLance/RoboticsBay','ResearchGraviticBooster/RoboticsBay'],#RoboticsBay
                   ['Rally','Immortal/RoboticsFacility','Colossus/RoboticsFacility','Observer/RoboticsFacility','WarpPrism/RoboticsFacility'],#RoboticsFacility
                   ['Rally','Tempest/Stargate','VoidRay/Stargate','Phoenix/Stargate','Oracle/Stargate','Carrier/Stargate','WarpInScout/Stargate'],#Stargate
                   ['ResearchHighTemplarEnergyUpgrade/TemplarArchive','ResearchPsiStorm/TemplarArchive'],#TemplarArchive
                   ['ResearchCharge/TwilightCouncil','ResearchStalkerTeleport/TwilightCouncil'],#TwilightCouncil
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','CloakOnBanshee','CloakOff'],#__Terran units__ #Banshee
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','YamatoGun','MissilePods/Battlecruiser','DefensiveMatrix/Battlecruiser'],#Battlecruiser
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','StimFirebat/Firebat','IncineratorNozzles/Firebat'],#Firebat
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','CloakOnBanshee','CloakOff','EMP/Ghost','Snipe/Ghost','NukeCalldown/Ghost','GhostHoldFire/Ghost','WeaponsFree/Ghost'],#Ghost
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MorphToHellionTank/Hellion','MorphToHellion/Hellion'],#Hellion
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','HerculesLoad/Hercules','HerculesUnloadAll/Hercules'],#Hercules
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Stim'],#Marine
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MedicHeal/Medic'],#Medic
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Heal/Medivac','BunkerLoad','BunkerUnloadAll'],#Medivac
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','AutoTurret/Raven','PointDefenseDrone/Raven','HunterSeekerMissile/Raven'],#Raven
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','D8Charge/Reaper'],#Reaper
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','NanoRepair/ScienceVessel','Irradiate/ScienceVessel'],#Science Vessel
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SiegeMode','Unsiege'],#Siege Tank
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','RogueGhostCloak/Spectre','CloakOff','Obliterate/Spectre','UltrasonicPulse/Spectre','SpectreNukeCalldown/Spectre','SpectreWeaponsFree/Spectre','SpectreHoldFire/Spectre'],#Spectre
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','250mmStrikeCannons/Thor'],#Thor
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','AssaultMode','FighterMode'],#Viking
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SpiderMine/Vulture','SpiderMineReplenish/Vulture'],#Vulture
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','WraithCloakOn/Wraith','WraithCloakOff/Wraith'],#Wraith
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Cancel','NovaSnipe/Nova','Domination/Nova','ReleaseMinion/Nova','HeroNukeCalldown/Nova'],#__Heroes__ #Nova
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Cancel','OdinBarrage/Odin','OdinNukeCalldown/Odin'],#Odin
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','ExperimentalPlasmaGun/Raynor','PlantC4Charge/Raynor','TheMorosDevice/Raynor','TossGrenade/Raynor'],#Raynor
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','RaynorSnipe/RaynorCommando'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BonesHeal/Stetmann'],#Stetmann
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','DutchPlaceTurret/Swann'],#Swann
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MindBlast/Tosh','VoodooShield/Tosh','Consumption/Tosh','HeroNukeCalldown/Tosh'],#Tosh
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','TossGrenadeTychus/TychusCommando'],#Tychus
                   ['SelectBuilder','Halt','Cancel','TerranShipPlatingLevel1/Armory','TerranShipWeaponsLevel1/Armory','TerranVehiclePlatingLevel1/Armory','TerranVehicleWeaponsLevel1/Armory'],#__Terran Buildings__ #Armory
                   ['SelectBuilder','Cancel','Lift','Rally','Marine/Barracks','Marauder/Barracks','Reaper/Barracks','Ghost/Barracks','Medic/Barracks','Firebat/Barracks','TechLabBarracks/Barracks','Reactor/Barracks','TechReactorAI/Barracks'],#Barracks
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Land','TechLabBarracks/BarracksFlying','Reactor/BarracksFlying'],
                   ['SelectBuilder','Cancel','Salvage/Bunker','SetBunkerRallyPoint/Bunker','BunkerLoad','BunkerUnloadAll','Stim','Stop','Attack'],#Bunker
                   ['SelectBuilder','Halt','Cancel','TerranInfantryArmorLevel1/EngineeringBay','TerranInfantryWeaponsLevel1/EngineeringBay','ResearchHiSecAutoTracking/EngineeringBay','ResearchNeosteelFrame/EngineeringBay','UpgradeBuildingArmorLevel1/EngineeringBay'],#Engineering Bay
                   ['SelectBuilder','Cancel','Lift','Rally','Hellion/Factory','WidowMine/Factory','SiegeTank/Factory','Thor/Factory','TechLabFactory/Factory','Reactor/Factory','TechReactorAI/Factory'],#Factory
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Land','BuildTechLabFactory/FactoryFlying','Reactor/FactoryFlying'],
                   ['ResearchBattlecruiserEnergyUpgrade/FusionCore','ResearchBattlecruiserSpecializations/FusionCore'],#Fusion Core
                   ['NukeArm/GhostAcademy','ResearchGhostEnergyUpgrade/GhostAcademy','ResearchPersonalCloaking/GhostAcademy'],#Ghost Academy
                   ['SelectBuilder','Cancel','Lift','Rally','VikingFighter/Starport','Medivac/Starport','Raven/Starport','Banshee/Starport','Battlecruiser/Starport','Wraith/Starport','BuildHercules/Starport','TechLabStarport/Starport','Reactor/Starport','TechReactorAI/Starport'],#Starport
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Land','BuildTechLabStarport/StarportFlying','Reactor/StarportFlying'],
                   ['SelectBuilder','Halt','Cancel','Lower/SupplyDepot'],#Supply Depot
                   ['ResearchShieldWall/BarracksTechLab','Stimpack/BarracksTechLab','ResearchPunisherGrenades/BarracksTechLab','ReaperSpeed/BarracksTechLab'],#Tech Labs/Reactors
                   ['ResearchShieldWall/BarracksTechReactor','Stimpack/BarracksTechReactor','ReaperSpeed/BarracksTechReactor'],
                   ['ResearchHighCapacityBarrels/FactoryTechLab','ResearchSiegeTech/FactoryTechLab','ResearchStrikeCannons/FactoryTechLab'],
                   ['ResearchHighCapacityBarrels/FactoryTechReactor','ResearchSiegeTech/FactoryTechReactor'],
                   ['ResearchMedivacEnergyUpgrade/StarportTechLab','ResearchBansheeCloak/StarportTechLab','ResearchDurableMaterials/StarportTechLab','ResearchSeekerMissile/StarportTechLab','ResearchRavenEnergyUpgrade/StarportTechLab'],
                   ['ResearchMedivacEnergyUpgrade/StarportTechReactor','ResearchBansheeCloak/StarportTechReactor','ResearchDurableMaterials/StarportTechReactor','ResearchSeekerMissile/StarportTechReactor','ResearchRavenEnergyUpgrade/StarportTechReactor','WraithCloak/StarportTechReactor'],
                   ['Corruptor/Larva','Drone/Larva','Hydralisk/Larva','Infestor/Larva','Mutalisk/Larva','Overlord/Larva','Roach/Larva','SwarmHostMP/Larva','Ultralisk/Larva','Viper/Larva','Zergling/Larva'],#__Zerg Units__ #Larva
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','DisableBuildingAttack/Baneling','EnableBuildingAttack/Baneling','Explode/Baneling'],#Baneling
                   ['Attack','Explode/BanelingBurrowed','BurrowUp'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BroodLord/Corruptor','CorruptionAbility/Corruptor'],#Corruptor
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','NeuralParasite/Infestor','FungalGrowth/Infestor','InfestedTerrans/Infestor'],#Infestor
                   ['Attack','InfestedTerrans/InfestorBurrowed','BurrowUp'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BunkerLoad','BunkerUnloadAll','GenerateCreep/Overlord','StopGenerateCreep/Overlord','MorphToOverseer/Overlord'],#Overlord
                   ['Move','Stop','MoveHoldPosition','MovePatrol','SpawnChangeling/Overseer','Contaminate/Overseer'],#Overseer
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','MorphMorphalisk/Queen','BuildCreepTumor/Queen','Transfusion/Queen'],#Queen
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','Baneling/Zergling'],#Zergling
                   ['zerggroundarmor1/EvolutionChamber','zergmeleeweapons1/EvolutionChamber','zergmissileweapons1/EvolutionChamber'],#__Zerg Buildings__ #Evolution Chamber
                   ['LurkerDen/HydraliskDen','MuscularAugments/HydraliskDen','hydraliskspeed/HydraliskDen'],#Hydralisk Den
                   ['ResearchLocustLifetimeIncrease/InfestationPit','EvolveInfestorEnergyUpgrade/InfestationPit','ResearchNeuralParasite/InfestationPit'],#Infestation Pit
                   ['Stop','BunkerLoad','BunkerUnloadAll','Rally','SummonNydusWorm/NydusNetwork'],#Nydus Network
                   ['EvolveTunnelingClaws/RoachWarren','EvolveGlialRegeneration/RoachWarren'],#Roach Warren
                   ['zerglingattackspeed/SpawningPool','zerglingmovementspeed/SpawningPool'],#Spawning Pool
                   ['Stop','Attack','SpineCrawlerUproot/SpineCrawler'],#Spine Crawler
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SpineCrawlerRoot/SpineCrawlerUprooted'],
                   ['zergflyerattack1','zergflyerarmor1','GreaterSpire/Spire'],#Spire
                   ['Stop','Attack','SporeCrawlerUproot/SporeCrawler'],#Spore Crawler
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SporeCrawlerRoot/SporeCrawlerUprooted']]

#Check these ones please
#['Move','Stop','MoveHoldPosition','MovePatrol','Attack','WidowMineAttack/WidowMine','WidowMineBurrow/WidowMine','WidowMineUnburrow/WidowMine'],#Window Mine
#['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SwarmHost/SwarmHostBurrowedMP','SwarmHost/SwarmHostMP','SwarmHostBurrowDown'],#Swarm Host
#['Attack','SwarmHostBurrowUp'],
#['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowProtector/Viper','FaceEmbrace/Viper','ViperConsume/Viper'],#Viper
#['EvolveBurrowCharge/UltraliskCavern','EvolveChitinousPlating/UltraliskCavern'],#UltraliskCavern

# Read the settings
settings_parser = SafeConfigParser()
settings_parser.optionxform=str
settings_parser.read('MapDefinitions.ini')

I18N_parser = SafeConfigParser()
I18N_parser.optionxform=str
I18N_parser.read('KeyboardLayouts.ini')

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
righty_index = {0: False,
                1: True,
                2: True}

def verify_file(filename):
    hotkeys_file = open(filename, 'r')
    all_items = settings_parser.items('MappingTypes')
    dict = {}
    for item in all_items:
        dict[item[0]] = [False, "", item[0], item[1]]
    for line in hotkeys_file:
        line = line.strip()
        if len(line) == 0 or line[0] == "[":
            continue
        pair = line.split("=")
        key = pair[0]
        if key in dict:
            dict[key] = [True, pair[1], key, dict[key][3]]
        else:
            dict[key] = [True, pair[1], key, ""]
        
    count = 0
    for item in dict:
        if not dict[item][0]:
            if "HOTS" in dict[item][3]:
                if SHOW_HOTS_MISSING:
                    count += 1
            else:
                count += 1
    if count > 0:        
        print(filename + " is missing " + str(count) + " hotkeys: ")
        #print "NOTE: Capitalization is not correct. Check settings.ini for correct capitalization."
        for item in dict:
            if not dict[item][0]:
                if "HOTS" in dict[item][3]:
                    if SHOW_HOTS_MISSING:
                        print("HOTS: " + dict[item][2])
                else:
                    print(dict[item][2])
    else:
        print(filename + " contains all hotkeys.")

    # Check for duplicates
    if SHOW_DUPLICATES:
        verify_parser = SafeConfigParser()
        verify_parser.optionxform=str
        dup_dict = {}
        verify_parser.read(filename)
        gen_items = verify_parser.items('Hotkeys')
        for pair in gen_items:
            if pair[1] in dup_dict:
                dup_dict[pair[1]].append(pair[0])
            else:
                dup_dict[pair[1]] = [pair[0]]
        for key in dup_dict:
            array = dup_dict[key]
            if len(array) > 1:
                print("============================")
                print(key + "    DUPLICATES")
                for a in array:
                    print(a)

    for same_set in SAME_CHECKS:
        mismatched = False
        value = dict[same_set[0]][1]
        for item in same_set:
            if not dict[item][1] == value:
                mismatched = True
        if mismatched:
            print("---- Mismatched values ----")
            for item in same_set:
                print(item + " = " + dict[item][1])

    for conflict_set in CONFLICT_CHECKS:
        hotkeys = []
        count_hotkeys = {}
        for item in conflict_set:
            hotkeys.append(dict[item][1])
        for key in hotkeys:
            if not key in count_hotkeys:
                count_hotkeys[key] = 1
            else:
                count_hotkeys[key] = count_hotkeys[key] + 1
        for count in count_hotkeys:
            if count_hotkeys[count] > 1:
                print("---- Conflict of hotkeys ----")
                for item in conflict_set:
                    key = dict[item][1]
                    if count_hotkeys[key] > 1:
                        print(item + " = " + key)
                #print(conflict_set)
    print("")

def parse_pair(parser, key, values, map_name, index, altgr):
    parsed = ""
    first = True
    for value in values:
        bits = value.split("+")
        if not first:
            parsed += ","
        if bits[0] == "Alt" and altgr == 1:
            bits[0] = "Control+Alt"
        last_bit = bits[len(bits)-1]
        try:
            if index < 0:
                bits[len(bits)-1] = parser.get(map_name, last_bit)
            else:
                bits[len(bits)-1] = parser.get(map_name, last_bit).split(",")[index]
        except:
            last_bit = last_bit # Do nothing
        #if is_rl_shift and "|" in bits[len(bits)-1]:
        #    try:
        #        unused = parser.get("MappingTypes", key).split(",")
        #        bits[len(bits)-1] = bits[len(bits)-1].split("|")[0]
        #    except:
        #        bits[len(bits)-1] = bits[len(bits)-1].split("|")[1]
        #    if not bits[len(bits)-1] == "":
        #        parsed += "+".join(bits)
        if not bits[len(bits)-1] == "":
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
                output += parse_pair(settings_parser, key, values, 'GlobalMaps', GLOBAL, 0)
            else:
                output += pair[1]
        #elif race == "Z" and "MM" in layout and key in ZERG_CONTROL_GROUP_SPECIAL:
        #    output += parse_pair(settings_parser, key, values, race + 'SCGMaps', layoutIndex, 0)
        elif key in CONTROL_GROUP_KEYS:
            output += parse_pair(settings_parser, key, values, race + 'CGMaps', layoutIndex, 0)
        elif key in GENERAL_KEYS:
            if "R" in layout:
                output += parse_pair(settings_parser, key, values, 'GlobalMaps', GLOBAL, 0)
            else:
                output += pair[1]
        else:
            try:
                maptypes = settings_parser.get("MappingTypes", key).split(",")
                output += parse_pair(settings_parser, key, values, race + maptypes[race_dict[race]] + "Maps", layoutIndex, 0)
            except:
                output += pair[1]
        output += "\n"
    hotkeys_file.close()
    newfilename = filename.replace("LM", layout)
    fileio = open(newfilename, 'w')
    fileio.write(output)
    fileio.close()
    if VERIFY_ALL:
        verify_file(newfilename)
    return newfilename

def shift_hand_size(filename, shift_right, hand_size, is_righty):
    hotkeys_file = open(filename, 'r')
    output = ""
    if is_righty:
        map_prefix = "R"
    else:
        map_prefix = "L"
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
            output += parse_pair(settings_parser, key, values, map_prefix + 'ShiftRightMaps', GLOBAL, 0)
        else:
            output += parse_pair(settings_parser, key, values, map_prefix + 'ShiftLeftMaps', GLOBAL, 0)        
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
    if VERIFY_ALL:
        verify_file(newfilename)
    return newfilename

def translate_file(filename, is_righty):
    layouts = I18N_parser.sections()
    for l in layouts:
        hotkeys_file = open(filename, 'r')
        output = ""
        if is_righty:
            altgr = int(I18N_parser.get(l, "AltGr"))
        else:
            altgr = 0
    
        for line in hotkeys_file:
            line = line.strip()
            if len(line) == 0 or line[0] == "[":
                output += line + "\n"
                continue
            pair = line.split("=")
            key = pair[0]
            values = pair[1].split(",")
            output += key + "="
            
            output += parse_pair(I18N_parser, key, values, l, GLOBAL, altgr)        
            output += "\n"

        hotkeys_file.close()
        newfilename = l + "/" + filename
        if not os.path.isdir(l):
            os.makedirs(l)
        fileio = open(newfilename, 'w')
        fileio.write(output)
        fileio.close()
    
# Main part of the script. For each race, generate each layout, and translate that layout for large and small hands.
for race in races:
    filename = prefix + " " + race + "LM " + suffix
    verify_file(filename)
    translate_file(filename, False)
    translate_file(shift_hand_size(filename, True, "L", False), False)
    translate_file(shift_hand_size(filename, False, "S", False), False)
    for layout in layouts:
        index = layoutIndices[layout]
        layout_filename = generate_layout(filename, race, layout, index)
        translate_file(layout_filename, righty_index[index])
        if righty_index[index]:
            translate_file(shift_hand_size(layout_filename, True, "S", True), True)
            translate_file(shift_hand_size(layout_filename, False, "L", True), True)
        else:
            translate_file(shift_hand_size(layout_filename, True, "L", False), False)
            translate_file(shift_hand_size(layout_filename, False, "S", False), False)

#Quick test to see if 4 seed files are error free
#	Todo:	expand this to every single file in every directory
#			expand both SAME_CHECKS and CONFLICT_CHECKS
#for race in races:
#    filename = prefix + " " + race + "LM " + suffix
#    verify_file(filename)

