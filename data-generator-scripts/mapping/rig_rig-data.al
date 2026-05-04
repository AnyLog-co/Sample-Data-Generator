#--------------------------------------------------------------------------------------------------------------------#
# Mapping policy for rig data
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/mapping/rig_rig-data.al


on error ignore

set create_policy = false

:check-policy:
is_policy = blockchain get (mapping, transform) where id = rig-data
if not !is_policy and !create_policy == false then goto declare-policy
else if !is_policy then goto end-script
else if not !is_policy and !create_policy == true then goto declare-policy-error


:declare-policy:
set new_policy = {}
<new_policy = {
    "mapping" : {
        "id" : "rig-data",
        "dbms" : !default_dbms,
        "table" : "bring [table]",
        "readings" : "",
        "schema" : {
            "timestamp" : {
                "type" : "timestamp",
                "default" : "now()",
                "bring" : "[timestamp]"
            },
            "rig_id" : {
                "type" : "string",
                "default" : "",
                "bring" : "[rig_id]"
            },
            "rig_name" : {
                "type" : "string",
                "default" : "",
                "bring" : "[rig_name]"
            },
            "location" : {
                "type" : "string",
                "default" : "",
                "bring" : "[location]"
            },
            "activity" : {
                "type" : "string",
                "default" : "",
                "bring" : "[activity]"
            },
            "measured_depth" : {
                "type" : "float",
                "bring" : "[measured_depth]"
            },
            "true_vertical_depth" : {
                "type" : "float",
                "bring" : "[true_vertical_depth]"
            },
            "rop" : {
                "type" : "float",
                "bring" : "[rop]"
            },
            "wob" : {
                "type" : "float",
                "bring" : "[wob]"
            },
            "rpm" : {
                "type" : "float",
                "bring" : "[rpm]"
            },
            "torque" : {
                "type" : "float",
                "bring" : "[torque]"
            },
            "standpipe_pressure" : {
                "type" : "float",
                "bring" : "[standpipe_pressure]"
            },
            "choke_pressure" : {
                "type" : "float",
                "bring" : "[choke_pressure]"
            },
            "flow_rate" : {
                "type" : "float",
                "bring" : "[flow_rate]"
            },
            "hookload" : {
                "type" : "float",
                "bring" : "[hookload]"
            },
            "bit_depth" : {
                "type" : "float",
                "bring" : "[bit_depth]"
            },
            "hole_depth" : {
                "type" : "float",
                "bring" : "[hole_depth]"
            },
            "mud_weight_in" : {
                "type" : "float",
                "bring" : "[mud_weight_in]"
            },
            "mud_weight_out" : {
                "type" : "float",
                "bring" : "[mud_weight_out]"
            },
            "mud_temp_in" : {
                "type" : "float",
                "bring" : "[mud_temp_in]"
            },
            "mud_temp_out" : {
                "type" : "float",
                "bring" : "[mud_temp_out]"
            },
            "total_gas" : {
                "type" : "float",
                "bring" : "[total_gas]"
            },
            "block_height" : {
                "type" : "float",
                "bring" : "[block_height]"
            },
            "status" : {
                "type" : "string",
                "default" : "",
                "bring" : "[status]"
            }
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
