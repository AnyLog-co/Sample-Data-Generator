#--------------------------------------------------------------------------------------------------------------------#
# Mapping policy for vessel data
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/mapping/vessel_CHARGER-LOGS.al
on error ignore

set create_policy = false

:check-policy:
is_policy = blockchain get (mapping, transform) where id = CHARGER-LOGS
if not !is_policy and !create_policy == false then goto declare-policy
else if !is_policy then goto end-script
else if not !is_policy and !create_policy == true then goto declare-policy-error


:declare-policy:
<new_policy = {
    "mapping" : {
        "id" : "CHARGER-LOGS",
        "dbms" : !default_dbms,
        "table" : "charger_logs",
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
            "__start__" : {"script" : ["set CHARGER-LOGS_counter = 0"]
            },
            "gActAcCurrent" : {
                "type" : "float",
                "bring" : "[gActAcCurrent]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gActAcCurrent] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gActAcVoltage" : {
                "type" : "float",
                "bring" : "[gActAcVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gActAcVoltage] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gActAcFrequency" : {
                "type" : "float",
                "bring" : "[gActAcFrequency]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gActAcFrequency] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gCommandAcCurrentLimitPP" : {
                "type" : "int",
                "bring" : "[gCommandAcCurrentLimitPP]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gCommandAcCurrentLimitPP] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gParamMaxAcCurrentPP" : {
                "type" : "int",
                "bring" : "[gParamMaxAcCurrentPP]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gParamMaxAcCurrentPP] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gActDcPower" : {
                "type" : "float",
                "bring" : "[gActDcPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gActDcPower] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gActDcVoltage" : {
                "type" : "float",
                "bring" : "[gActDcVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gActDcVoltage] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gCommandDcPowerLimit" : {
                "type" : "int",
                "bring" : "[gCommandDcPowerLimit]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gCommandDcPowerLimit] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gCommandMaxDcVoltage" : {
                "type" : "float",
                "bring" : "[gCommandMaxDcVoltage]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gCommandMaxDcVoltage] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gMaxDcPower" : {
                "type" : "float",
                "bring" : "[gMaxDcPower]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gMaxDcPower] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gActElectronicTemperature" : {
                "type" : "int",
                "bring" : "[gActElectronicTemperature]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gActElectronicTemperature] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gCoolingPolicy" : {
                "type" : "string",
                "bring" : "[gCoolingPolicy]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gCoolingPolicy] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gState" : {
                "type" : "string",
                "bring" : "[gState]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gState] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gCommand" : {
                "type" : "string",
                "bring" : "[gCommand]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gCommand] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gError" : {
                "type" : "string",
                "bring" : "[gError]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gError] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gDisableReason" : {
                "type" : "string",
                "bring" : "[gDisableReason]",
                "default" : "",
                "optional" : True,
                "script" : ["if [gDisableReason] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gIsSlave" : {
                "type" : "int",
                "bring" : "[gIsSlave]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gIsSlave] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gWake" : {
                "type" : "int",
                "bring" : "[gWake]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gWake] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "gSimConnectedPhaseCount" : {
                "type" : "int",
                "bring" : "[gSimConnectedPhaseCount]",
                "default" : Null,
                "optional" : True,
                "script" : ["if [gSimConnectedPhaseCount] then CHARGER-LOGS_counter = incr !CHARGER-LOGS_counter"]
            },
            "__end__" : {"script" : ["if !CHARGER-LOGS_counter == 0 then streaming data ignore event"]}
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
