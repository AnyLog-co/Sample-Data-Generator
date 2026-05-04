#--------------------------------------------------------------------------------------------------------------------#
# Mapping policy for vessel data
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/mapping/vessel_BATTERY-PACK-LOGS.al
on error ignore

set create_policy = false

:check-policy:
is_policy = blockchain get (mapping, transform) where id = BATTERY-PACK-LOGS
if not !is_policy and !create_policy == false then goto declare-policy
else if !is_policy then goto end-script
else if not !is_policy and !create_policy == true then goto declare-policy-error


:declare-policy:
<new_policy = {
    "mapping" : {
        "id" : "BATTERY-PACK-LOGS",
        "dbms" : !default_dbms,
        "table" : "battery_pack_logs",
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
            "__start__" : {"script" : ["set BATTERY-PACK-LOGS_counter = 0"]
            },
            "gStateOfCharge" : {
                "type" : "float",
                "bring" : "[gStateOfCharge]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gStateOfCharge] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gStateOfHealth" : {
                "type" : "float",
                "bring" : "[gStateOfHealth]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gStateOfHealth] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gEnergyRemaining" : {
                "type" : "float",
                "bring" : "[gEnergyRemaining]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gEnergyRemaining] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gParamMaxCapacity" : {
                "type" : "float",
                "bring" : "[gParamMaxCapacity]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gParamMaxCapacity] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gParamMaxChargeVoltage" : {
                "type" : "float",
                "bring" : "[gParamMaxChargeVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gParamMaxChargeVoltage] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gPackVoltage" : {
                "type" : "float",
                "bring" : "[gPackVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gPackVoltage] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gBusVoltage" : {
                "type" : "float",
                "bring" : "[gBusVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gBusVoltage] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gCurrent" : {
                "type" : "float",
                "bring" : "[gCurrent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gCurrent] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gCellBalance" : {
                "type" : "float",
                "bring" : "[gCellBalance]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gCellBalance] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gPowerLimitCharge" : {
                "type" : "float",
                "bring" : "[gPowerLimitCharge]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gPowerLimitCharge] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gPowerLimitDischarge" : {
                "type" : "int",
                "bring" : "[gPowerLimitDischarge]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gPowerLimitDischarge] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gAverageTemperature" : {
                "type" : "int",
                "bring" : "[gAverageTemperature]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gAverageTemperature] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gMaxCellTemperature" : {
                "type" : "int",
                "bring" : "[gMaxCellTemperature]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gMaxCellTemperature] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gMinCellTemperature" : {
                "type" : "int",
                "bring" : "[gMinCellTemperature]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gMinCellTemperature] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gCoolingPolicy" : {
                "type" : "string",
                "bring" : "[gCoolingPolicy]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gCoolingPolicy] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gTimeToFullMinute" : {
                "type" : "int",
                "bring" : "[gTimeToFullMinute]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gTimeToFullMinute] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gState" : {
                "type" : "string",
                "bring" : "[gState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gState] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gCommand" : {
                "type" : "string",
                "bring" : "[gCommand]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gCommand] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gError" : {
                "type" : "string",
                "bring" : "[gError]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gError] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gDisableReason" : {
                "type" : "string",
                "bring" : "[gDisableReason]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gDisableReason] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "gBalancingState" : {
                "type" : "string",
                "bring" : "[gBalancingState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gBalancingState] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "batteryErrorCode" : {
                "type" : "int",
                "bring" : "[batteryErrorCode]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [batteryErrorCode] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "batteryErrorListEraseState" : {
                "type" : "string",
                "bring" : "[batteryErrorListEraseState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [batteryErrorListEraseState] then BATTERY-PACK-LOGS_counter = incr !BATTERY-PACK-LOGS_counter"]
            },
            "__end__" : {"script" : ["if !BATTERY-PACK-LOGS_counter == 0 then streaming data ignore event"]}
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
