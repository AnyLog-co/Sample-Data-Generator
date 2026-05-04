#--------------------------------------------------------------------------------------------------------------------#
# Mapping policy for wind turbine data
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/mapping/wind_turbine_reactive-power.al
on error ignore

set create_policy = false

:check-policy:
is_policy = blockchain get (mapping, transform) where id = reactive-power
if not !is_policy and !create_policy == false then goto declare-policy
else if !is_policy then goto end-script
else if not !is_policy and !create_policy == true then goto declare-policy-error


:declare-policy:
<new_policy = {
    "mapping" : {
        "id" : "reactive-power",
        "dbms" : !default_dbms,
        "table" : "reactive_power",
        "readings" : "",
        "schema" : {
            "timestamp" : {
                "type" : "timestamp",
                "default" : "now()",
                "bring" : "[timestamp]"
            },
            "turbine_id" : {
                "type" : "int",
                "bring" : "[turbine_id]"
            },
            "alias" : {
                "type" : "string",
                "default" : "",
                "bring" : "[alias]"
            },
            "reactive_avg" : {
                "type" : "int",
                "bring" : "[reactive_avg]"
            },
            "reactive_max" : {
                "type" : "int",
                "bring" : "[reactive_max]"
            },
            "reactive_min" : {
                "type" : "int",
                "bring" : "[reactive_min]"
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
