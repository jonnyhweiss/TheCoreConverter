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
import os, sys

TRANSLATE = not "US" in sys.argv
ONLY_SEED = "LM" in sys.argv

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
GENERAL_KEYS = ['Music','Sound','PTT','DialogDismiss','MenuAchievements','MenuGame','MenuMessages','MenuSocial',
                'LeaderResources','LeaderIncome','LeaderSpending','LeaderUnits','LeaderUnitsLost','LeaderProduction','LeaderArmy',
                'LeaderAPM','LeaderCPM','ObserveAllPlayers','ObserveAutoCamera','ObserveClearSelection','ObservePlayer0','ObservePlayer1',
                'ObservePlayer2','ObservePlayer3','ObservePlayer4','ObservePlayer5','ObservePlayer6','ObservePlayer7','ObservePlayer8',
                'ObservePlayer9','ObservePlayer10','ObservePlayer11','ObservePlayer12','ObservePlayer13','ObservePlayer14','ObservePlayer15',
                'ObserveSelected','ObservePreview','ObserveStatusBars','StatPanelResources','StatPanelArmySupply','StatPanelUnitsLost','StatPanelAPM','StatPanelCPM',
                'ToggleWorldPanel', 'CinematicSkip','AlertRecall','CameraFollow','GameTooltipsOn','IdleWorker','MinimapColors','MinimapPing',
                'MinimapTerrain','PauseGame','QuickPing','QuickSave','ReplayPlayPause','ReplayRestart','ReplaySkipBack','ReplaySkipNext','ReplaySpeedDec',
                'ReplaySpeedInc','ReplayStop','ReplayHide','SelectionCancelDrag','SubgroupNext','SubgroupPrev','TeamResources','TownCamera','WarpIn',
                'Cancel','CancelCocoon','CancelMutateMorph','CancelUpgradeMorph','ChatCancel',
				'ChatAll','ChatDefault','ChatIndividual','ChatRecipient','ChatAllies',
				'CameraTurnLeft','CameraTurnRight','CameraCenter',
                'StatusAll','StatusOwner','StatusEnemy','StatusAlly','MenuHelp','NamePanel','ArmySelect','SelectBuilder', 'ToggleVersusModeSides']

EXCLUDE_MAPPING = ['AllowSetConflicts']

SAME_CHECKS = [['Pylon/Probe','SupplyDepot/SCV','SupplyDepotDrop/SCV'],
               ['Assimilator/Probe','Extractor/Drone','Refinery/SCV','AutomatedRefinery/SCV','AutomatedExtractor/Drone'],
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
#               ['WeaponsFree/Ghost','SpectreWeaponsFree/Spectre'], thanks to HotS Spectre key now unbinds if set to same as HoldFire, Ghost HoldFire & weapons free toggle works correctly
               ['GhostHoldFire/Ghost','SpectreHoldFire/Spectre'],
               ['NukeArm/GhostAcademy','SpectreNukeArm/GhostAcademy'],
               ['NukeCalldown/Ghost','SpectreNukeCalldown/Spectre','HeroNukeCalldown/Nova','HeroNukeCalldown/Tosh','OdinNukeCalldown/Odin'],
               ['BunkerLoad','HerculesLoad/Hercules'],
               ['BunkerUnloadAll','HerculesUnloadAll/Hercules'],
               ['Reactor/Barracks','Reactor/BarracksFlying','Reactor/Factory','Reactor/FactoryFlying','Reactor/Starport','Reactor/StarportFlying'],
               ['TechLabBarracks/Barracks','TechLabBarracks/BarracksFlying','TechReactor/Barracks','TechReactor/BarracksFlying','TechLabFactory/Factory','BuildTechLabFactory/FactoryFlying','TechReactor/Factory','TechReactor/FactoryFlying','TechLabStarport/Starport','BuildTechLabStarport/StarportFlying','TechReactor/Starport','TechReactor/StarportFlying'],
#               ['Ghost/Barracks','Spectre/Barracks'], thanks to HotS campaign these can no longer be on the same key
               ['Raven/Starport','BuildScienceVessel/Starport'],
               ['EMP/Ghost','UltrasonicPulse/Spectre'],
               ['Snipe/Ghost','NovaSnipe/Nova','Obliterate/Spectre'],
               ['Lair/Hatchery','Hive/Lair','LurkerDen/HydraliskDen','ImpalerDen/HydraliskDen'],
               ['MassRecall/Mothership','MassRecall/Artanis','MothershipMassRecall/Mothership','MothershipCoreMassRecall/MothershipCore'],
               ['Vortex/Mothership','Vortex/Artanis'],
               ['Mothership/Nexus','MothershipCore/Nexus'],
               ['AutoTurret/Raven','BuildAutoTurret/Raven'],
               ['PointDefenseDrone/Raven','BuildPointDefenseDrone/Raven'],
               ['ResearchShieldWall/BarracksTechLab','ResearchShieldWall/BarracksTechReactor'],
               ['Stimpack/BarracksTechLab','Stimpack/BarracksTechReactor'],
               ['ResearchPunisherGrenades/BarracksTechLab','ResearchPunisherGrenades/BarracksTechReactor','ResearchJackhammerConcussionGrenade/BarracksTechLab','ResearchJackhammerConcussionGrenade/BarracksTechReactor'],
               ['ReaperSpeed/BarracksTechLab','ReaperSpeed/BarracksTechReactor','ResearchG4Charge/BarracksTechLab','ResearchG4Charge/BarracksTechReactor'],
               ['ResearchIncineratorNozzles/BarracksTechLab','ResearchIncineratorNozzles/BarracksTechReactor'],
               ['ResearchStabilizerMedPacks/BarracksTechLab','ResearchStabilizerMedPacks/BarracksTechReactor'],
               ['ResearchCerberusMines/FactoryTechLab','ResearchCerberusMines/FactoryTechReactor'],
               ['ResearchHighCapacityBarrels/FactoryTechLab','ResearchHighCapacityBarrels/FactoryTechReactor'],
               ['ResearchMultiLockTargetingSystem/FactoryTechLab','ResearchMultiLockTargetingSystem/FactoryTechReactor'],
               ['ResearchRegenerativeBioSteel/FactoryTechLab','ResearchRegenerativeBioSteel/FactoryTechReactor'],
               ['ResearchStrikeCannons/FactoryTechLab','ResearchStrikeCannons/FactoryTechReactor'],
               ['ResearchSiegeTech/FactoryTechLab','ResearchSiegeTech/FactoryTechReactor','ResearchShapedBlast/FactoryTechLab','ResearchShapedBlast/FactoryTechReactor'],
               ['ResearchMedivacEnergyUpgrade/StarportTechLab','ResearchMedivacEnergyUpgrade/StarportTechReactor'],
               ['ResearchBansheeCloak/StarportTechLab','ResearchBansheeCloak/StarportTechReactor'],
               ['ResearchDurableMaterials/StarportTechLab','ResearchDurableMaterials/StarportTechReactor'],
               ['ResearchSeekerMissile/StarportTechLab','ResearchSeekerMissile/StarportTechReactor'],
               ['ResearchRavenEnergyUpgrade/StarportTechLab','ResearchRavenEnergyUpgrade/StarportTechReactor'],
               ['WraithCloak/StarportTechLab','WraithCloak/StarportTechReactor'],
               ['Baneling/Zergling','Baneling/Zergling2','Baneling/HotSRaptor','Baneling/HotSSwarmling','MorphtoHunter/HotSRaptor','MorphtoHunter/HotSSwarmling','MorphtoSplitterling/HotSRaptor','MorphtoSplitterling/HotSSwarmling'],
               ['DisableBuildingAttack/Baneling','DisableBuildingAttack/baneling','DisableBuildingAttack/baneling2','DisableBuildingAttack/HotSHunter','DisableBuildingAttack/HotSSplitterlingBig'],
               ['EnableBuildingAttack/Baneling','EnableBuildingAttack/baneling','EnableBuildingAttack/baneling2','EnableBuildingAttack/HotSHunter','EnableBuildingAttack/HotSSplitterlingBig'],
               ['Explode/Baneling','Explode/BanelingBurrowed','Explode/baneling','Explode/baneling2','Explode/HotSSplitterlingBig','Explode/HotSSplitterlingBigBurrowed','Explode/HotSHunter','Explode/HotSHunterBurrowed'],
               ['ForceField/Sentry','ForceField2/Sentry2'],
               ['FungalGrowth/Infestor','FungalGrowth/Infestor2'],
               ['GuardianShield/Sentry','GuardianShield/Sentry2'],
               ['Hallucination/Sentry','Hallucination/Sentry2'],
               ['Heal/Medivac','Heal/Medivac2'],
               ['InfestedTerrans/Infestor','InfestedTerrans/Infestor2'],
               ['NeuralParasite/Infestor','NeuralParasite/Infestor2','NPSwarm/Infestor'],
               ['Baneling/Zergling','Baneling/Zergling2','Baneling/HotSRaptor','Baneling/HotSSwarmling'],
               ['Apocalypse/K5Kerrigan','K5DropPods/K5Kerrigan','K5Leviathan/K5Kerrigan'],
               ['MindBolt/K5Kerrigan','MindBolt/KerriganGhostLab','PrimalSlash/K5Kerrigan'],
               ['PrimalHeal/K5Kerrigan','SpawnBanelings/K5Kerrigan','WildMutation/K5Kerrigan'],
               ['PsiStrike/K5Kerrigan','PsionicLift/K5Kerrigan','PsionicLift/KerriganGhostLab'],
               ['YamatoGun','SJHyperionYamato/SJHyperion'],
               ['Hydralisk/Larva','MorphToHydraliskImpaler/Larva','MorphToHydraliskLurker/Larva'],
               ['Infestor/Larva','MorphtoDefiler/Larva'],
               ['Mutalisk/Larva','MorphToMutaliskBroodlord/Larva','MorphToMutaliskViper/Larva'],
               ['Roach/Larva','MorphToVile/Larva','MorphToCorpser/Larva'],
               ['SwarmHostMP/Larva','MorphToSwarmHostSplitA/Larva','MorphToSwarmHostSplitB/Larva'],
               ['Ultralisk/Larva','MorphToHotSNoxious/Larva','MorphToHotSTorrasque/Larva'],
               ['Viper/Larva','Aberration/Larva'],
               ['Zergling/Larva','MorphToSwarmling/Larva','MorphToRaptor/Larva'],
               ['LocustLaunch/SwarmHostBurrowed','LocustFlyingLaunch/SwarmHostSplitABurrowed','LocustFlyingLaunch/SwarmHostSplitARooted','LocustLaunch/SwarmHostRooted','LocustLaunchCreeper/SwarmHostSplitBBurrowed','LocustLaunchCreeper/SwarmHostSplitBRooted'],
               ['BurrowDown','BurrowHydraliskImpalerDown','BurrowHydraliskLurkerDown','ImpalerBurrowDown','LurkerBurrowDown'],
               ['BurrowUp','BurrowHydraliskImpalerUp','BurrowHydraliskLurkerUp','ImpalerBurrowUp','LurkerBurrowUp'],#'SwarmHostUprootUnburrow/SwarmHostBurrowed','SwarmHostUprootUnburrow/SwarmHostSplitABurrowed','SwarmHostUprootUnburrow/SwarmHostSplitBBurrowed'
               ['SwarmHostDeepBurrow/SwarmHostSplitB','SwarmHostDeepBurrow/SwarmHostSplitBBurrowed','SwarmHostDeepBurrow/SwarmHostSplitBRooted'],
               ['SwarmHostRoot/SwarmHost','SwarmHostRoot/SwarmHostSplitA','SwarmHostRoot/SwarmHostSplitB'],
               ['SwarmHostUproot/SwarmHostRooted','SwarmHostUproot/SwarmHostSplitARooted','SwarmHostUproot/SwarmHostSplitBRooted'],
               ['HydraliskFrenzy/Hydralisk','HydraliskFrenzy/HydraliskImpaler','HydraliskFrenzy/HydraliskLurker'],
               ['Impaler/HydraliskImpaler','Lurker/HydraliskLurker'],
               ['BroodLord/Corruptor','BroodLord/MutaliskBroodlord','Viper/MutaliskViper'],
               ['BlindingCloud/Viper','DisablingCloud/Viper'],
               ['ViperConsume/Viper','ViperConsumption/Viper'],
               ['BurrowChargeMP/Ultralisk','BurrowChargeCampaign/Ultralisk','BurrowChargeCampaign/HotSTorrasque','BurrowChargeCampaignNoxious/HotSNoxious'],
               ['Transfusion/Queen','Transfusion/Queen2','QueenBurstHeal/Queen'],
               ['GrowHugeQueen/LargeSwarmQueen','GrowLargeQueen/SwarmQueen','GrowSwarmQueen/LarvalQueen'],
               ['SwarmQueenHydralisk/HugeSwarmQueen','SwarmQueenHydralisk/SwarmQueenEgg','SwarmQueenHydraliskImpaler/HugeSwarmQueen','SwarmQueenHydraliskImpaler/LargeSwarmQueen','SwarmQueenHydraliskImpaler/SwarmQueen','SwarmQueenHydraliskLurker/HugeSwarmQueen','SwarmQueenHydraliskLurker/LargeSwarmQueen','SwarmQueenHydraliskLurker/SwarmQueen'],
               ['ParasiticInvasion/LarvalQueen','SwarmQueenParasiticInvasion/HugeSwarmQueen','SwarmQueenParasiticInvasion/LargeSwarmQueen','SwarmQueenParasiticInvasion/SwarmQueen'],
               ['SwarmQueenCorpser/LargeSwarmQueen','SwarmQueenCorpser/HugeSwarmQueen','SwarmQueenCorpser/SwarmQueen','SwarmQueenRoach/HugeSwarmQueen','SwarmQueenRoach/LargeSwarmQueen','SwarmQueenRoach/SwarmQueenEgg','SwarmQueenVile/HugeSwarmQueen','SwarmQueenVile/LargeSwarmQueen','SwarmQueenVile/SwarmQueen'],
               ['SwarmQueenRaptor/HugeSwarmQueen','SwarmQueenRaptor/LargeSwarmQueen','SwarmQueenRaptor/SwarmQueen','SwarmQueenSwarmling/HugeSwarmQueen','SwarmQueenSwarmling/LargeSwarmQueen','SwarmQueenSwarmling/SwarmQueen','SwarmQueenZergling/HugeSwarmQueen','SwarmQueenZergling/LargeSwarmQueen','SwarmQueenZergling/SwarmQueen','SwarmQueenZergling/SwarmQueenEgg'],
               ['GreaterSpire/Spire','GreaterSpireBroodlord/Spire'],
               ['RespawnZergling/Hatchery','RespawnZergling/Hive','RespawnZergling/Lair']]
               #['GenerateCreep/Overlord','StopGenerateCreep/Overlord']]
               
CONFLICT_CHECKS = [['Cancel','Stop','Rally','Probe/Nexus','TimeWarp/Nexus','Mothership/Nexus'],
                   ['Cancel','Stop','Attack','Rally','Probe/Nexus','TimeWarp/Nexus','MothershipCore/Nexus'],#Nexus HotS
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
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','PsiStorm/HighTemplar','Feedback/HighTemplar','AWrp'],#High Templar
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MassRecall/Mothership','Vortex/Mothership'],#Mothership WoL
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MothershipMassRecall/Mothership','TemporalField/Mothership'],#Mothership HotS
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MothershipCoreWeapon/MothershipCore','MothershipCoreMassRecall/MothershipCore','TemporalField/MothershipCore','MorphToMothership/MothershipCore'],#Mothership Core
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','OracleRevelation/Oracle','OracleWeaponOff/Oracle','OracleWeaponOn/Oracle','LightofAiur/Oracle'],#Oracle
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','GravitonBeam/Phoenix'],#Phoenix
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','ForceField/Sentry','GuardianShield/Sentry','Hallucination/Sentry'],#Sentry
                   ['ArchonHallucination/Sentry','ColossusHallucination/Sentry','HighTemplarHallucination/Sentry','ImmortalHallucination/Sentry','OracleHallucination/Sentry','PhoenixHallucination/Sentry','ProbeHallucination/Sentry','StalkerHallucination/Sentry','VoidRayHallucination/Sentry','WarpPrismHallucination/Sentry','ZealotHallucination/Sentry'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','Blink/Stalker'],#Stalker
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','VoidRaySwarmDamageBoost/VoidRay'],#VoidRay
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BunkerLoad','BunkerUnloadAll','PhasingMode/WarpPrism','TransportMode/WarpPrism'],#Warp Prism
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Rally','Charge/Zealot'],#Zealot
                   ['ProtossAirWeaponsLevel1/CyberneticsCore','ProtossAirArmorLevel1/CyberneticsCore','ResearchWarpGate/CyberneticsCore','ResearchHallucination/CyberneticsCore'],#__Protoss Buildings__ #Cybernetics Core
                   ['AnionPulseCrystals/FleetBeacon','ResearchInterceptorLaunchSpeedUpgrade/FleetBeacon','ResearchVoidRaySpeedUpgrade/FleetBeacon'],#Fleet Beacon
                   ['ProtossGroundWeaponsLevel1/Forge','ProtossGroundArmorLevel1/Forge','ProtossShieldsLevel1/Forge'],#Forge
                   ['Rally','Zealot','Stalker','Sentry','HighTemplar','DarkTemplar','UpgradeToWarpGate/Gateway'],#Gateway
                   ['Rally','Zealot','Stalker','Sentry','HighTemplar','DarkTemplar','MorphBackToGateway/WarpGate'],
                   ['ResearchGraviticDrive/RoboticsBay','ResearchExtendedThermalLance/RoboticsBay','ResearchGraviticBooster/RoboticsBay'],#Robotics Bay
                   ['Rally','Immortal/RoboticsFacility','Colossus/RoboticsFacility','Observer/RoboticsFacility','WarpPrism/RoboticsFacility'],#Robotics Facility
                   ['Rally','Tempest/Stargate','VoidRay/Stargate','Phoenix/Stargate','Oracle/Stargate','Carrier/Stargate','WarpInScout/Stargate'],#Stargate
                   ['ResearchHighTemplarEnergyUpgrade/TemplarArchive','ResearchPsiStorm/TemplarArchive'],#Templar Archives
                   ['ResearchCharge/TwilightCouncil','ResearchStalkerTeleport/TwilightCouncil'],#TwilightCouncil
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','CloakOnBanshee','CloakOff'],#__Terran units__ #Banshee
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','YamatoGun','MissilePods/Battlecruiser','DefensiveMatrix/Battlecruiser'],#Battlecruiser
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','StimFirebat/Firebat','IncineratorNozzles/Firebat'],#Firebat
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','CloakOnBanshee','CloakOff','EMP/Ghost','Snipe/Ghost','NukeCalldown/Ghost','GhostHoldFire/Ghost'],#Ghost
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MorphToHellionTank/Hellion','MorphToHellion/Hellion'],#Hellion
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','HerculesLoad/Hercules','HerculesUnloadAll/Hercules'],#Hercules
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Stim'],#Marine
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MedicHeal/Medic'],#Medic
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Heal/Medivac','MedivacSpeedBoost/Medivac','BunkerLoad','BunkerUnloadAll'],#Medivac
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','AutoTurret/Raven','PointDefenseDrone/Raven','HunterSeekerMissile/Raven'],#Raven
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','D8Charge/Reaper'],#Reaper
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','NanoRepair/ScienceVessel','Irradiate/ScienceVessel'],#Science Vessel
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SiegeMode','Unsiege'],#Siege Tank
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','RogueGhostCloak/Spectre','CloakOff','Obliterate/Spectre','UltrasonicPulse/Spectre','SpectreNukeCalldown/Spectre','SpectreHoldFire/Spectre'],#Spectre
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','250mmStrikeCannons/Thor'],#Thor
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','ExplosiveMode','ArmorpiercingMode'],#Thor HotS
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','AssaultMode','FighterMode'],#Viking
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SpiderMine/Vulture','SpiderMineReplenish/Vulture'],#Vulture
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','WidowMineBurrow/WidowMine','WidowMineUnburrow/WidowMine'],#Widow Mine                   
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','WraithCloakOn/Wraith','WraithCloakOff/Wraith'],#Wraith
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Cancel','NovaSnipe/Nova','Domination/Nova','ReleaseMinion/Nova','HeroNukeCalldown/Nova'],#__Heroes__ #Nova
                   ['SJHyperionBlink/SJHyperion','SJHyperionFighters/SJHyperion','SJHyperionFightersRecall/SJHyperion','SJHyperionLightningStorm/SJHyperion','SJHyperionYamato/SJHyperion'],#Hyperion HotS
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','Cancel','OdinBarrage/Odin','OdinNukeCalldown/Odin'],#Odin
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','ExperimentalPlasmaGun/Raynor','PlantC4Charge/Raynor','TheMorosDevice/Raynor','TossGrenade/Raynor'],#Raynor
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','RaynorSnipe/RaynorCommando'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BonesHeal/Stetmann'],#Stetmann
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','DutchPlaceTurret/Swann'],#Swann
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','MindBlast/Tosh','VoodooShield/Tosh','Consumption/Tosh','HeroNukeCalldown/Tosh'],#Tosh
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','TossGrenadeTychus/TychusCommando'],#Tychus
                   ['SelectBuilder','Halt','Cancel','TerranShipPlatingLevel1/Armory','TerranShipWeaponsLevel1/Armory','TerranVehiclePlatingLevel1/Armory','TerranVehicleWeaponsLevel1/Armory'],#__Terran Buildings__ #Armory WoL
                   ['SelectBuilder','Halt','Cancel','TerranShipWeaponsLevel1/Armory','TerranVehicleAndShipPlatingLevel1/Armory','TerranVehicleWeaponsLevel1/Armory'],#Armory HotS
                   ['SelectBuilder','Cancel','Lift','Rally','Marine/Barracks','Marauder/Barracks','Reaper/Barracks','Ghost/Barracks','Medic/Barracks','Firebat/Barracks','TechLabBarracks/Barracks','Reactor/Barracks','TechReactorAI/Barracks'],#Barracks WoL
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Land','TechLabBarracks/BarracksFlying','Reactor/BarracksFlying'],
                   ['SelectBuilder','Cancel','Lift','Rally','Marine/Barracks','Marauder/Barracks','Reaper/Barracks','Ghost/Barracks','Medic/Barracks','Firebat/Barracks','Spectre/Barracks','MengskUnits/Barracks','TechLabBarracks/Barracks','Reactor/Barracks','TechReactorAI/Barracks'],#Barracks HotS Campaign
                   ['SelectBuilder','Cancel','Lift','Rally','Marine/Barracks','Marauder/Barracks','Reaper/Barracks','Medic/Barracks','Firebat/Barracks','HireKelmorianMiners/Barracks','HireHammerSecurities/Barracks','HireDevilDogs/Barracks','MercReaper/Barracks','MercMedic/Barracks'],#Barracks HotS Campaign 2
                   ['SelectBuilder','Cancel','Salvage/Bunker','SetBunkerRallyPoint/Bunker','BunkerLoad','BunkerUnloadAll','Stim','Stop','Attack'],#Bunker
                   ['SelectBuilder','Halt','Cancel','TerranInfantryArmorLevel1/EngineeringBay','TerranInfantryWeaponsLevel1/EngineeringBay','ResearchHiSecAutoTracking/EngineeringBay','ResearchNeosteelFrame/EngineeringBay','UpgradeBuildingArmorLevel1/EngineeringBay'],#Engineering Bay
                   ['SelectBuilder','Cancel','Lift','Rally','Hellion/Factory','WidowMine/Factory','SiegeTank/Factory','HellionTank/Factory','Thor/Factory','TechLabFactory/Factory','Reactor/Factory'],#Factory
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Land','BuildTechLabFactory/FactoryFlying','Reactor/FactoryFlying'],
                   ['SelectBuilder','Cancel','Lift','Rally','Hellion/Factory','SiegeTank/Factory','Thor/Factory','Vulture/Factory','Goliath/Factory','Diamondback/Factory','Predator/Factory','TechLabFactory/Factory','Reactor/Factory','TechReactorAI/Factory'],#Factory WoL Campaign
                   ['SelectBuilder','Cancel','Lift','Rally','Hellion/Factory','SiegeTank/Factory','WarHound/Factory','CampaignVehicles/Factory','TechLabFactory/Factory','Reactor/Factory','TechReactorAI/Factory'],#Factory HotS Campaign
                   ['SelectBuilder','Cancel','Lift','Rally','Vulture/Factory','Predator/Factory','Diamondback/Factory','Goliath/Factory','MicroBot/Factory','Thor/Factory','Hellion/Factory'],#Factory HotS Campaign 2
                   ['SelectBuilder','Cancel','Lift','Rally','Hellion/Factory','Goliath/Factory','SiegeTank/Factory','Diamondback/Factory','Thor/Factory','MercHellion/Factory','HireSpartanCompany/Factory','HireSiegeBreakers/Factory'],#Factory HotS Campaign 3
                   ['ResearchBattlecruiserEnergyUpgrade/FusionCore','ResearchBattlecruiserSpecializations/FusionCore'],#Fusion Core
                   ['NukeArm/GhostAcademy','ResearchGhostEnergyUpgrade/GhostAcademy','ResearchPersonalCloaking/GhostAcademy'],#Ghost Academy
                   ['SelectBuilder','Halt','Cancel','Rally','HireKelmorianMiners/MercCompound','HireDevilDogs/MercCompound','HireHammerSecurities/MercCompound','HireSpartanCompany/MercCompound','HireSiegeBreakers/MercCompound','HireHelsAngels/MercCompound','HireDuskWing/MercCompound','HireDukesRevenge/MercCompound','ReaperSpeed/MercCompound','MercHellion/MercCompound','MercMedic/MercCompound','MercReaper/MercCompound'],#Merc Compound
                   ['ResearchHellion/ScienceFacility','ResearchSiegeTank/ScienceFacility','ResearchReaper/ScienceFacility','ResearchMedic/ScienceFacility','ResearchFirebat/ScienceFacility','ResearchGoliath/ScienceFacility','ResearchBunkerUpgrade/ScienceFacility','ResearchPerditionTurret/ScienceFacility','ResearchFireSuppression/ScienceFacility','ResearchTechReactor/ScienceFacility'],#Science Facility
                   ['SelectBuilder','Cancel','Lift','Rally','VikingFighter/Starport','Medivac/Starport','Raven/Starport','Banshee/Starport','Battlecruiser/Starport','Wraith/Starport','BuildHercules/Starport','TechLabStarport/Starport','Reactor/Starport','TechReactorAI/Starport'],#Starport WoL Campaign
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Land','BuildTechLabStarport/StarportFlying','Reactor/StarportFlying'],
                   ['SelectBuilder','Cancel','Lift','Rally','VikingFighter/Starport','Medivac/Starport','Raven/Starport','Banshee/Starport','Battlecruiser/Starport','CampaignVehicles/Starport','TechLabStarport/Starport','Reactor/Starport','TechReactorAI/Starport'],#Starport HotS Campaign
                   ['SelectBuilder','Cancel','Lift','Rally','Wraith/Starport','BuildHercules/Starport','BuildScienceVessel/Starport','Battlecruiser/Starport'],#Starport HotS Campaign 2
                   ['SelectBuilder','Cancel','Lift','Rally','VikingFighter/Starport','Banshee/Starport','Wraith/Starport','Battlecruiser/Starport','HireDuskWing/Starport','HireHelsAngels/Starport','HireDukesRevenge/Starport'],#Starport HotS Campaign 3
                   ['SelectBuilder','Halt','Cancel','Lower/SupplyDepot'],#Supply Depot
                   ['ResearchShieldWall/BarracksTechLab','Stimpack/BarracksTechLab','ResearchPunisherGrenades/BarracksTechLab','ReaperSpeed/BarracksTechLab'],#TechLab Barracks WoL
                   ['Stimpack/BarracksTechLab','ResearchJackhammerConcussionGrenade/BarracksTechLab','ResearchG4Charge/BarracksTechLab','ResearchStabilizerMedPacks/BarracksTechLab','ResearchIncineratorNozzles/BarracksTechLab'],#TechLab Barracks Left2Die
                   ['ResearchHighCapacityBarrels/FactoryTechLab','ResearchSiegeTech/FactoryTechLab','ResearchStrikeCannons/FactoryTechLab'],#TechLab Factory WoL
                   ['ResearchHighCapacityBarrels/FactoryTechLab','ResearchDrillClaws/FactoryTechLab','ResearchTransformationServos/FactoryTechLab'],#TechLab Factory HotS
                   ['ResearchHighCapacityBarrels/FactoryTechLab','ResearchShapedBlast/FactoryTechLab','ResearchCerberusMines/FactoryTechLab','ResearchMultiLockTargetingSystem/FactoryTechLab','ResearchRegenerativeBioSteel/FactoryTechLab'],#TechLab Factory Left2Die
                   ['ResearchMedivacEnergyUpgrade/StarportTechLab','ResearchBansheeCloak/StarportTechLab','ResearchDurableMaterials/StarportTechLab','ResearchSeekerMissile/StarportTechLab','ResearchRavenEnergyUpgrade/StarportTechLab','WraithCloak/StarportTechLab'],#TechLab Starport WoL
                   ['ResearchMedivacEnergyUpgrade/StarportTechLab','ResearchBansheeCloak/StarportTechLab','ResearchDurableMaterials/StarportTechLab','ResearchRavenEnergyUpgrade/StarportTechLab','WraithCloak/StarportTechLab'],#TechLab Starport HotS
                   ['Corruptor/Larva','Drone/Larva','Hydralisk/Larva','Infestor/Larva','Mutalisk/Larva','Overlord/Larva','Roach/Larva','SwarmHostMP/Larva','Ultralisk/Larva','Viper/Larva','Zergling/Larva'],#__Zerg Units__ #Larva
                   ['Aberration/Larva','Drone/Larva','Hydralisk/Larva','Infestor/Larva','Mutalisk/Larva','Overlord/Larva','Roach/Larva','MorphToSwarmHostSplitA/Larva','Ultralisk/Larva','Zergling/Larva'],#Larva HotS Campaign
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','DisableBuildingAttack/Baneling','EnableBuildingAttack/Baneling','Explode/Baneling'],#Baneling
                   ['Attack','Explode/BanelingBurrowed','BurrowUp'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BroodLord/Corruptor','CorruptionAbility/Corruptor'],#Corruptor
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','NeuralParasite/Infestor','FungalGrowth/Infestor','InfestedTerrans/Infestor'],#Infestor
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','NPSwarm/Infestor','FungalGrowth/Infestor','InfestorConsumption/Infestor'],#Infestor HotS Campaign
                   ['Attack','InfestedTerrans/InfestorBurrowed','BurrowUp'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BunkerLoad','BunkerUnloadAll','GenerateCreep/Overlord','MorphToOverseer/Overlord'],#Overlord
                   ['Move','Stop','MoveHoldPosition','MovePatrol','SpawnChangeling/Overseer','Contaminate/Overseer'],#Overseer
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','MorphMorphalisk/Queen','BuildCreepTumor/Queen','Transfusion/Queen'],#Queen
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SwarmHost/SwarmHostMP','SwarmHostBurrowDown'],#Swarm Host
                   ['Attack','SetRallyPointSwarmHost/SwarmHostBurrowedMP','SwarmHost/SwarmHostBurrowedMP','SwarmHostBurrowUp'],#Swarm Host Burrowed
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SwarmHostDeepBurrow/SwarmHostSplitB','SwarmHostBurrowDown'],#Swarm Host HotS Campaign
                   ['Stop','Attack','SwarmHostDeepBurrow/SwarmHostSplitB','SwarmHostBurrowUp','LocustLaunchCreeper/SwarmHostSplitBBurrowed'],#Swarm Host HotS Campaign Burrowed
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BlindingCloud/Viper','FaceEmbrace/Viper','ViperConsume/Viper'],#Viper
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','Baneling/Zergling'],#Zergling
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','K5Leviathan/K5Kerrigan','MindBolt/K5Kerrigan','PsionicLift/K5Kerrigan','WildMutation/K5Kerrigan'],#__Zerg Heroes Kerrigan
                   ['K5Leviathan/K5KerriganBurrowed','MindBolt/K5KerriganBurrowed','PsionicLift/K5KerriganBurrowed','WildMutation/K5KerriganBurrowed','BurrowUp'],
                   ['SwarmQueenParasiticInvasion/LargeSwarmQueen','SwarmQueenZergling/LargeSwarmQueen','SwarmQueenRoach/LargeSwarmQueen','GrowHugeQueen/LargeSwarmQueen'],#Niadra
                   ['SwarmQueenParasiticInvasion/HugeSwarmQueen','SwarmQueenZergling/HugeSwarmQueen','SwarmQueenRoach/HugeSwarmQueen','SwarmQueenHydralisk/HugeSwarmQueen'],
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','BurrowDown','Drag/Dehaka','DehakaHeal/Dehaka','DehakaMirrorImage/Dehaka'],#Dehaka
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
                   ['Move','Stop','MoveHoldPosition','MovePatrol','Attack','SporeCrawlerRoot/SporeCrawlerUprooted'],
                   ['Cancel','EvolveChitinousPlating/UltraliskCavern']]#Ultralisk Cavern

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
races = ["P", "T", "R", "Z"]
layouts = ["RM"]
layoutIndices = {"LMM": 0,
                 "RMM": 1,
                 "RM": 2}
righty_index = {0: False,
                1: True,
                2: True}

def verify_file(filename):
    hotkeys_file = open(filename, 'r')
    dict = {}
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
        
        # No need to distinguish between map types anymore. Just use GlobalMaps
        if key in EXCLUDE_MAPPING:
            output += pair[1]
        else:
            try:
                output += parse_pair(settings_parser, key, values, 'GlobalMaps', GLOBAL, 0)
            except:
                output += pair[1]
            
        # if key in CAMERA_KEYS:
            # if "R" in layout:
                # output += parse_pair(settings_parser, key, values, 'GlobalMaps', GLOBAL, 0)
            # else:
                # output += pair[1]
        # #elif race == "Z" and "MM" in layout and key in ZERG_CONTROL_GROUP_SPECIAL:
        # #    output += parse_pair(settings_parser, key, values, race + 'SCGMaps', layoutIndex, 0)
        # elif key in CONTROL_GROUP_KEYS:
            # output += parse_pair(settings_parser, key, values, race + 'CGMaps', layoutIndex, 0)
        # elif key in GENERAL_KEYS:
            # if "R" in layout:
                # output += parse_pair(settings_parser, key, values, 'GlobalMaps', GLOBAL, 0)
            # else:
                # output += pair[1]
        # else:
            # try:
                # #maptypes = settings_parser.get("MappingTypes", key).split(",")
                # maptypes = ["A","A","A","A"] # Only use ability maps
                # output += parse_pair(settings_parser, key, values, race + maptypes[race_dict[race]] + "Maps", layoutIndex, 0)
            # except:
                # output += pair[1]
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
        
        if key in EXCLUDE_MAPPING:
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
    if not TRANSLATE:
        return
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

# NEW - Generate the file from TheCoreSeed.ini
def generate_seed_files():
    theseed_parser = SafeConfigParser()
    theseed_parser.optionxform=str
    theseed_parser.read('TheCoreSeed.ini')
    
    theseed = open("TheCoreSeed.ini", 'r')
    outputs = ["","","",""]
    for line in theseed:
        line = line.strip()
        if len(line) == 0 or line[0] == "[":
            for i in range(4):
                outputs[i] += line + "\n"
            continue    

        pair = line.split("=")
        key = pair[0]
        values = pair[1].split("|")
        numvals = len(values)
        if numvals == 1:
            # it is a copy of another value
            if theseed_parser.has_option("Hotkeys", values[0]):
                values = theseed_parser.get("Hotkeys", values[0]).split("|")
            elif theseed_parser.has_option("Commands", values[0]):
                values = theseed_parser.get("Commands", values[0]).split("|")
            else:
                values = [values[0],values[0],values[0],values[0]]
            numvals = len(values)
        if numvals == 2:
            values = [values[0],values[0],values[0],values[0]] # all layouts are the same
        for i in range(4):
            outputs[i] += key + "=" + values[i] + "\n"
    i = 0
    for r in races:
        filename = prefix + " " + r + "LM " + suffix
        fileio = open(filename, 'w')
        fileio.write(outputs[i])
        fileio.close()
        i += 1

def generate_other_files():
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

generate_seed_files()
if not ONLY_SEED:
    generate_other_files()

#Quick test to see if 4 seed files are error free
#	Todo:	expand this to every single file in every directory
#			expand both SAME_CHECKS and CONFLICT_CHECKS
#for race in races:
#    filename = prefix + " " + race + "LM " + suffix
#    verify_file(filename)

