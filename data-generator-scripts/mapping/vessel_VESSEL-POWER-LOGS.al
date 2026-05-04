#--------------------------------------------------------------------------------------------------------------------#
# Mapping policy for vessel data
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/mapping/vessel_VESSEL-POWER-LOGS.al
on error ignore

set create_policy = false

:check-policy:
is_policy = blockchain get (mapping, transform) where id = VESSEL-POWER-LOGS
if not !is_policy and !create_policy == false then goto declare-policy
else if !is_policy then goto end-script
else if not !is_policy and !create_policy == true then goto declare-policy-error


:declare-policy:
<new_policy = {
    "mapping" : {
        "id" : "VESSEL-POWER-LOGS",
        "dbms" : !default_dbms,
        "table" : "vessel_power_logs",
        "readings" : "",
        "schema" : {
            "timestamp" : {
                "type" : "timestamp",
                "default" : "now()",
                "bring" : "[timestamp]"
            },
            "boat_name" : {
                "type" : "string",
                "bring" : "[boat_name]",
                "default" : ""
            },
            "side" : {
                "type" : "string",
                "bring" : "[side]",
                "default" : ""
            },
            "ip_index" : {
                "type" : "int",
                "bring" : "[ip_index]",
                "default" : Null
            },
            "motor_id" : {
                "type" : "int",
                "bring" : "[motor_id]",
                "default" : Null
            },
            "__start__" : {"script" : ["set VESSEL-POWER-LOGS_counter = 0"]
            },
            "hmiYear" : {
                "type" : "int",
                "bring" : "[hmiYear]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiYear] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "hmiMonth" : {
                "type" : "int",
                "bring" : "[hmiMonth]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiMonth] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "hmiDay" : {
                "type" : "int",
                "bring" : "[hmiDay]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiDay] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "hmiHour" : {
                "type" : "int",
                "bring" : "[hmiHour]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiHour] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "hmiMinute" : {
                "type" : "int",
                "bring" : "[hmiMinute]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiMinute] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "hmiSecond" : {
                "type" : "int",
                "bring" : "[hmiSecond]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hmiSecond] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "batteryStateOfChargePercent" : {
                "type" : "int",
                "bring" : "[batteryStateOfChargePercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [batteryStateOfChargePercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "hvBatteryCapacity" : {
                "type" : "float",
                "bring" : "[hvBatteryCapacity]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [hvBatteryCapacity] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "hvBatteryType" : {
                "type" : "string",
                "bring" : "[hvBatteryType]",
                "default" : "",
                "optional" : True,
                "script" : ["if [hvBatteryType] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "currentBatteryPower" : {
                "type" : "int",
                "bring" : "[currentBatteryPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [currentBatteryPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "maxBatteryPower" : {
                "type" : "int",
                "bring" : "[maxBatteryPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [maxBatteryPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "timeToFullMinute" : {
                "type" : "int",
                "bring" : "[timeToFullMinute]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [timeToFullMinute] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "timeBattery" : {
                "type" : "int",
                "bring" : "[timeBattery]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [timeBattery] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "starterBatteryVoltage" : {
                "type" : "float",
                "bring" : "[starterBatteryVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [starterBatteryVoltage] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "starterBatteryVoltagePercent" : {
                "type" : "float",
                "bring" : "[starterBatteryVoltagePercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [starterBatteryVoltagePercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "lvBatteryCapacity" : {
                "type" : "int",
                "bring" : "[lvBatteryCapacity]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [lvBatteryCapacity] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "lvBatteryMaxCapacity" : {
                "type" : "int",
                "bring" : "[lvBatteryMaxCapacity]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [lvBatteryMaxCapacity] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "lvBatteryStateOfChargePercent" : {
                "type" : "int",
                "bring" : "[lvBatteryStateOfChargePercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [lvBatteryStateOfChargePercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "lvBatteryType" : {
                "type" : "string",
                "bring" : "[lvBatteryType]",
                "default" : "",
                "optional" : True,
                "script" : ["if [lvBatteryType] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "lvBatteryVoltage" : {
                "type" : "int",
                "bring" : "[lvBatteryVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [lvBatteryVoltage] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "lvBatteryVoltagePercent" : {
                "type" : "int",
                "bring" : "[lvBatteryVoltagePercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [lvBatteryVoltagePercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "powerBalance" : {
                "type" : "float",
                "bring" : "[powerBalance]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [powerBalance] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "motorPowerCombined" : {
                "type" : "int",
                "bring" : "[motorPowerCombined]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [motorPowerCombined] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "motorPowerCombinedPercent" : {
                "type" : "int",
                "bring" : "[motorPowerCombinedPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [motorPowerCombinedPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "motorPowerLimit" : {
                "type" : "int",
                "bring" : "[motorPowerLimit]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [motorPowerLimit] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portMotorPower" : {
                "type" : "int",
                "bring" : "[portMotorPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portMotorPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portMotorPowerPercent" : {
                "type" : "int",
                "bring" : "[portMotorPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portMotorPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdMotorPower" : {
                "type" : "int",
                "bring" : "[stbdMotorPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdMotorPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdMotorPowerPercent" : {
                "type" : "int",
                "bring" : "[stbdMotorPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdMotorPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portRpmShaft" : {
                "type" : "int",
                "bring" : "[portRpmShaft]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portRpmShaft] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portRpmShaftPercent" : {
                "type" : "int",
                "bring" : "[portRpmShaftPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portRpmShaftPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdRpmShaft" : {
                "type" : "int",
                "bring" : "[stbdRpmShaft]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdRpmShaft] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdRpmShaftPercent" : {
                "type" : "int",
                "bring" : "[stbdRpmShaftPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdRpmShaftPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "acChargerPowerPercent" : {
                "type" : "float",
                "bring" : "[acChargerPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [acChargerPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portAcChargerPower" : {
                "type" : "int",
                "bring" : "[portAcChargerPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portAcChargerPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portAcChargerEnable" : {
                "type" : "int",
                "bring" : "[portAcChargerEnable]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portAcChargerEnable] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdAcChargerPower" : {
                "type" : "float",
                "bring" : "[stbdAcChargerPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdAcChargerPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdAcChargerEnable" : {
                "type" : "int",
                "bring" : "[stbdAcChargerEnable]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdAcChargerEnable] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "dcacPower" : {
                "type" : "int",
                "bring" : "[dcacPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [dcacPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "dcacPowerConfirmed" : {
                "type" : "int",
                "bring" : "[dcacPowerConfirmed]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [dcacPowerConfirmed] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "dcacPowerPercent" : {
                "type" : "int",
                "bring" : "[dcacPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [dcacPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "dcacEnable" : {
                "type" : "int",
                "bring" : "[dcacEnable]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [dcacEnable] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "dcdcPower" : {
                "type" : "int",
                "bring" : "[dcdcPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [dcdcPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "dcdcPowerConfirmed" : {
                "type" : "int",
                "bring" : "[dcdcPowerConfirmed]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [dcdcPowerConfirmed] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "dcdcPowerPercent" : {
                "type" : "int",
                "bring" : "[dcdcPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [dcdcPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "dcdcEnable" : {
                "type" : "int",
                "bring" : "[dcdcEnable]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [dcdcEnable] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "regenerationPower" : {
                "type" : "int",
                "bring" : "[regenerationPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [regenerationPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "regenerationPowerPercent" : {
                "type" : "int",
                "bring" : "[regenerationPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [regenerationPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "regenerationEnable" : {
                "type" : "int",
                "bring" : "[regenerationEnable]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [regenerationEnable] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "solarPower" : {
                "type" : "int",
                "bring" : "[solarPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [solarPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "solarPower_hv" : {
                "type" : "int",
                "bring" : "[solarPower_hv]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [solarPower_hv] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "elPtxPower" : {
                "type" : "int",
                "bring" : "[elPtxPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [elPtxPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "elPtxPowerConfirmed" : {
                "type" : "int",
                "bring" : "[elPtxPowerConfirmed]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [elPtxPowerConfirmed] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "elPtxPowerConfirmedPercent" : {
                "type" : "int",
                "bring" : "[elPtxPowerConfirmedPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [elPtxPowerConfirmedPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "elPtxPowerPercent" : {
                "type" : "float",
                "bring" : "[elPtxPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [elPtxPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "ptoPower" : {
                "type" : "int",
                "bring" : "[ptoPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [ptoPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "ptoPowerConfirmed" : {
                "type" : "int",
                "bring" : "[ptoPowerConfirmed]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [ptoPowerConfirmed] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "ptoPowerPercent" : {
                "type" : "int",
                "bring" : "[ptoPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [ptoPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portGenSetPower" : {
                "type" : "int",
                "bring" : "[portGenSetPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portGenSetPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portGenSetPowerPercent" : {
                "type" : "int",
                "bring" : "[portGenSetPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portGenSetPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "portGenSetFuelConsumption" : {
                "type" : "int",
                "bring" : "[portGenSetFuelConsumption]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [portGenSetFuelConsumption] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdGenSetPower" : {
                "type" : "int",
                "bring" : "[stbdGenSetPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdGenSetPower] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdGenSetPowerPercent" : {
                "type" : "int",
                "bring" : "[stbdGenSetPowerPercent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdGenSetPowerPercent] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "stbdGenSetFuelConsumption" : {
                "type" : "int",
                "bring" : "[stbdGenSetFuelConsumption]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [stbdGenSetFuelConsumption] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "runTimeGenset" : {
                "type" : "int",
                "bring" : "[runTimeGenset]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [runTimeGenset] then VESSEL-POWER-LOGS_counter = incr !VESSEL-POWER-LOGS_counter"]
            },
            "__end__" : {"script" : ["if !VESSEL-POWER-LOGS_counter == 0 then streaming data ignore event"]}
        }
   }
}>

:publish-policy:
process !local_scripts/node-deployment/policies/publish_policy.al
if not !error_code.int then
do set create_policy = true
goto check-policy

if !error_code == 1 then goto sign-policy-error
else if !error_code == 2 then goto prepare-policy-error
else if !error_code == 3 then goto declare-policy-error

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign mapping policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare mapping policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare mapping policy on blockchain"
goto terminate-scripts
