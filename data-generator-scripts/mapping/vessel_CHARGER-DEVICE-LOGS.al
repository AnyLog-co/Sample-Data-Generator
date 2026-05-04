#--------------------------------------------------------------------------------------------------------------------#
# Mapping policy for vessel data
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/mapping/vessel_CHARGER-DEVICE-LOGS.al
on error ignore

set create_policy = false

:check-policy:
is_policy = blockchain get (mapping, transform) where id = CHARGER-DEVICE-LOGS
if not !is_policy and !create_policy == false then goto declare-policy
else if !is_policy then goto end-script
else if not !is_policy and !create_policy == true then goto declare-policy-error


:declare-policy:
<new_policy = {
    "mapping" : {
        "id" : "CHARGER-DEVICE-LOGS",
        "dbms" : !default_dbms,
        "table" : "charger_device_logs",
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
            "__start__" : {"script" : ["set CHARGER-DEVICE-LOGS_counter = 0"]
            },
            "currentL1" : {
                "type" : "float",
                "bring" : "[currentL1]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [currentL1] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "currentL2" : {
                "type" : "float",
                "bring" : "[currentL2]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [currentL2] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "currentL3" : {
                "type" : "float",
                "bring" : "[currentL3]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [currentL3] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "voltageL1" : {
                "type" : "float",
                "bring" : "[voltageL1]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [voltageL1] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "voltageL2" : {
                "type" : "float",
                "bring" : "[voltageL2]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [voltageL2] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "voltageL3" : {
                "type" : "float",
                "bring" : "[voltageL3]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [voltageL3] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "inputFrequency" : {
                "type" : "float",
                "bring" : "[inputFrequency]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [inputFrequency] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "acCurrentLim" : {
                "type" : "int",
                "bring" : "[acCurrentLim]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [acCurrentLim] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "batteryCurrent" : {
                "type" : "float",
                "bring" : "[batteryCurrent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [batteryCurrent] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "batteryCurrentLim" : {
                "type" : "float",
                "bring" : "[batteryCurrentLim]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [batteryCurrentLim] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "batteryVoltage" : {
                "type" : "float",
                "bring" : "[batteryVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [batteryVoltage] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "batteryVoltageLim" : {
                "type" : "float",
                "bring" : "[batteryVoltageLim]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [batteryVoltageLim] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "chgIbatMaxAvail" : {
                "type" : "float",
                "bring" : "[chgIbatMaxAvail]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [chgIbatMaxAvail] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "invTempAmb" : {
                "type" : "int",
                "bring" : "[invTempAmb]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [invTempAmb] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "bbTempAmb" : {
                "type" : "int",
                "bring" : "[bbTempAmb]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [bbTempAmb] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "externalTemp" : {
                "type" : "int",
                "bring" : "[externalTemp]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [externalTemp] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "signalTempAmb" : {
                "type" : "int",
                "bring" : "[signalTempAmb]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [signalTempAmb] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "signalTempChassis" : {
                "type" : "int",
                "bring" : "[signalTempChassis]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [signalTempChassis] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "inverterState" : {
                "type" : "string",
                "bring" : "[inverterState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [inverterState] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "inverterShutDownReason" : {
                "type" : "string",
                "bring" : "[inverterShutDownReason]",
                "default" : "",
                "optional" : True,
                "script" : ["if [inverterShutDownReason] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "buckBoostState" : {
                "type" : "string",
                "bring" : "[buckBoostState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [buckBoostState] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "buckBoostShutDownReason" : {
                "type" : "string",
                "bring" : "[buckBoostShutDownReason]",
                "default" : "",
                "optional" : True,
                "script" : ["if [buckBoostShutDownReason] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "shutDownReason" : {
                "type" : "string",
                "bring" : "[shutDownReason]",
                "default" : "",
                "optional" : True,
                "script" : ["if [shutDownReason] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "powerStage" : {
                "type" : "string",
                "bring" : "[powerStage]",
                "default" : "",
                "optional" : True,
                "script" : ["if [powerStage] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "signalState" : {
                "type" : "string",
                "bring" : "[signalState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [signalState] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "signalConnection" : {
                "type" : "string",
                "bring" : "[signalConnection]",
                "default" : "",
                "optional" : True,
                "script" : ["if [signalConnection] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "cmdEnable" : {
                "type" : "string",
                "bring" : "[cmdEnable]",
                "default" : "",
                "optional" : True,
                "script" : ["if [cmdEnable] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "cmdMode" : {
                "type" : "string",
                "bring" : "[cmdMode]",
                "default" : "",
                "optional" : True,
                "script" : ["if [cmdMode] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "mode" : {
                "type" : "string",
                "bring" : "[mode]",
                "default" : "",
                "optional" : True,
                "script" : ["if [mode] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "evseStatus" : {
                "type" : "string",
                "bring" : "[evseStatus]",
                "default" : "",
                "optional" : True,
                "script" : ["if [evseStatus] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "evseType" : {
                "type" : "string",
                "bring" : "[evseType]",
                "default" : "",
                "optional" : True,
                "script" : ["if [evseType] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "evseTypeStatus" : {
                "type" : "int",
                "bring" : "[evseTypeStatus]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [evseTypeStatus] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "contrPilotImp" : {
                "type" : "string",
                "bring" : "[contrPilotImp]",
                "default" : "",
                "optional" : True,
                "script" : ["if [contrPilotImp] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "proximityState" : {
                "type" : "string",
                "bring" : "[proximityState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [proximityState] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "lockState" : {
                "type" : "int",
                "bring" : "[lockState]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [lockState] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "pilotDuty" : {
                "type" : "int",
                "bring" : "[pilotDuty]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [pilotDuty] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "pilotFreq" : {
                "type" : "int",
                "bring" : "[pilotFreq]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [pilotFreq] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "lV_Vbat" : {
                "type" : "float",
                "bring" : "[lV_Vbat]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [lV_Vbat] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "lvBattUVlim" : {
                "type" : "float",
                "bring" : "[lvBattUVlim]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [lvBattUVlim] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "deviceMode" : {
                "type" : "string",
                "bring" : "[deviceMode]",
                "default" : "",
                "optional" : True,
                "script" : ["if [deviceMode] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "deviceEnableSetting" : {
                "type" : "string",
                "bring" : "[deviceEnableSetting]",
                "default" : "",
                "optional" : True,
                "script" : ["if [deviceEnableSetting] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "deviceSeen" : {
                "type" : "int",
                "bring" : "[deviceSeen]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [deviceSeen] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "deviceCantStart" : {
                "type" : "string",
                "bring" : "[deviceCantStart]",
                "default" : "",
                "optional" : True,
                "script" : ["if [deviceCantStart] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "error" : {
                "type" : "string",
                "bring" : "[error]",
                "default" : "",
                "optional" : True,
                "script" : ["if [error] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "errorStatus" : {
                "type" : "string",
                "bring" : "[errorStatus]",
                "default" : "",
                "optional" : True,
                "script" : ["if [errorStatus] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "BBuCVersion" : {
                "type" : "int",
                "bring" : "[BBuCVersion]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [BBuCVersion] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "INVuCVersion" : {
                "type" : "int",
                "bring" : "[INVuCVersion]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [INVuCVersion] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "signaluCVersion" : {
                "type" : "int",
                "bring" : "[signaluCVersion]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [signaluCVersion] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "hwRev" : {
                "type" : "string",
                "bring" : "[hwRev]",
                "default" : "",
                "optional" : True,
                "script" : ["if [hwRev] then CHARGER-DEVICE-LOGS_counter = incr !CHARGER-DEVICE-LOGS_counter"]
            },
            "__end__" : {"script" : ["if !CHARGER-DEVICE-LOGS_counter == 0 then streaming data ignore event"]}
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
