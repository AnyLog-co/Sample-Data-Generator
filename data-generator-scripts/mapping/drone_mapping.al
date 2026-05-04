#--------------------------------------------------------------------------------------------------------------------#
# Mapping policy for drone data
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/mapping/drone_mapping.al


on error ignore

set create_policy = false

:check-policy:
is_policy = blockchain get (mapping, transform) where id = !policy_id
if not !is_policy and !create_policy == false then goto declare-policy
else if !is_policy then goto end-script
else if not !is_policy and !create_policy == true then goto declare-policy-error


:declare-policy:
set new_policy = ""
<new_policy = {
    "mapping": {
        "id": !policy_id,
        "dbms": !default_dbms,
        "table": "bring [table]",
        "schema": {
            "drone_id": {
                "type": "string",
                "bring": "[drone_id]"
            },
            "role": {
                "type": "string",
                "bring": "[role]"
            },
            "leader_id": {
                "type": "string",
                "bring": "[leader_id]"
            },
            "latitude": {
                "type": "float",
                "bring": "[latitude]"
            },
            "longitude": {
                "type": "float",
                "bring": "[longitude]"
            },
            "altitude_m": {
                "type": "float",
                "bring": "[altitude_m]"
            },
            "heading_deg": {
                "type": "float",
                "bring": "[heading_deg]"
            },
            "speed_mps": {
                "type": "float",
                "bring": "[speed_mps]"
            },
            "velocity_mps": {
                "type": "float",
                "bring": "[velocity_mps]"
            },
            "battery_pct": {
                "type": "float",
                "bring": "[battery_pct]"
            },
            "time_in_flight_s": {
                "type": "float",
                "bring": "[time_in_flight_s]"
            },
            "status": {
                "type": "string",
                "bring": "[status]"
            },
            "sequence": {
                "type": "int",
                "bring": "[sequence]"
            },
            "timestamp": {
                "type": "timestamp",
                "default": "now()"
            },
            "estimated_leader_latitude": {
                "type": "float",
                "bring": "[estimated_leader_latitude]"
            },
            "estimated_leader_longitude": {
                "type": "float",
                "bring": "[estimated_leader_longitude]"
            },
            "estimated_leader_altitude_m": {
                "type": "float",
                "bring": "[estimated_leader_altitude_m]"
            },
            "estimated_distance_to_leader_m": {
                "type": "float",
                "bring": "[estimated_distance_to_leader_m]"
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
