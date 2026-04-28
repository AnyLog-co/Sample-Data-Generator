#-----------------------------------------------------------------------------------------------------------------------
# The following provides an example for accepting video data into MongoDB. The example uses REST broker process, but the
# same can be applied with MQTT, and the policy is similar to what EdgeX generates. When deploying script on a publisher
# node, make sure the default logical database (!default_dbms) is set to an existing logical database.
#
# For the data generator associated with this script please reach out to Roy Shadmon (roy@anylog.co)
#
# :AnyLog process:
#   0. Connect to (NoSQL) logical database
#   1. Set parameters
#   2. declare mapping policy
#   3. execute `run msg client`
#   4. From the outside deploy data generator
#       python3 $HOME/Sample-Data-Generator/data_generator_file_processing.py ~/Downloads/sample_data/videos/ ${REST_CONN_INFO} post \
#           --topic video-mapping \
#           --dbms test \
#           --table videos \
#           --enable-timezone-range \
#           --exception
#
# :sample data coming in:
# {
#   "apiVersion": "v2",
#   "id": "6b055b44-6eae-4f5d-b2fc-f9df19bf42cf",
#   "deviceName": "anylog-data-generator",
#   "origin": 1660163909,
#   "profileName": "anylog-video-generator",
#   "readings": [{
#       "start_ts": "2022-01-01 00:00:00",
#       "end_ts": "2022-01-01 00:00:05",
#       "binaryValue": "AAAAHGZ0eXBtcDQyAAAAAWlzb21tcDQxbXA0MgADWChtb292AAAAbG12aGQAAAAA3xnEUt8ZxFMAAHUwAANvyQABAA",
#       "mediaType": "video/mp4",
#       "origin": 1660163909,
#       "profileName": "traffic_data",
#       "resourceName": "OnvifSnapshot",
#       "valueType": "Binary",
#       "num_cars": 5,
#       "speed": 65.3
#   }],
#   "sourceName": "OnvifSnapshot"
# }
#
# :documents:
#   - Generic MQTT script: !local_scripts/deployment_scripts/mqtt.al
#   - Documentation: https://github.com/AnyLog-co/documentation/blob/master/image%20mapping.md
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/data-generator/drone_telemetry.al

on error ignore

# declare policy
:prepare-policy:
policy_id = drone-telemetry # used also as the mqtt topic name
process !local_scripts/data-generator/mapping/drone_mapping.al


:msg-call:
if !is_demo == true then goto end-script
on error goto msg-error
<run msg client where broker=rest and log=false and user-agent=anylog and topic=(
    name=!policy_id and
    policy=!policy_id
)>

:end-script:
end script

:terminate-scripts:
exit scripts

:test-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:sign-policy-error:
print "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare cluster policy on blockchain"
goto terminate-scripts

:policy-error:
print "Failed to publish policy for an unknown reason"
goto terminate-scripts


:msg-error:
echo "Failed to deploy MQTT process"
goto end-script
