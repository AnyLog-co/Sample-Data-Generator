#-----------------------------------------------------------------------------------------------------------------------
# The following provides an example for accepting video data into MongoDB. The example uses REST broker process, but the
# same can be applied with MQTT, and the policy is similar to what EdgeX generates.
#
# :process:
#   1. declare params
#   2. connect to MongoDB
#   3. execute `run blobs archiver`
#   4. declare mapping policy
#   5. execute `run mqtt client`
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
# process !local_scripts/sample_code/mongodb_process.al

:declare-params:
on error ignore
param_error = false
set broker=rest
set port = !anylog_rest_port
set mqtt_log = false
mqtt_topic_name=anylogedgex-videos
set mqtt_topic_dbms = !default_dbms

on error goto declare-params-error
table_name=videos
mongo_db_ip = 127.0.0.1
mongo_db_port = 27017
mongo_db_user = admin
mongo_db_passwd = passwd

# A boolean value to determine if blobs database is used
set blobs_dbms=true
# A boolean value to determine if file is saved in a folder as f(date)
set blobs_folder=true
# A boolean value to determine if compression is applied
set blobs_compress=true

# connect to MongoDB database
:connect-dbms:
on error goto connect-dbms-error
if !mongo_db_user and !mongo_db_passwd then connect dbms !default_dbms where type=mongo and ip=!mongo_db_ip and port=!mongo_db_port and user=!mongo_db_user and password=!mongo_db_passwd
else connect dbms !default_dbms where type=mongo and ip=!mongo_db_ip and port=!mongo_db_port

:blobs-archiver:
on error call blobs-archiver-error
run blobs archiver where dbms=!blobs_dbms and folder=!blobs_folder and compress=!blobs_compress

# declare policy
:prepare-policy:
policy_id = video_mapping
policy = blockchain get mapping where id = !policy_id
if not !policy then
<do mapping_policy = {
    "mapping": {
        "id": !policy_id,
        "dbms": !default_dbms,
        "table": !table_name,
        "source": {
            "bring": "[deviceName]",
            "default": "12"
        },
        "readings": "readings",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]"
            },
            "start_ts": {
                "type": "timestamp",
                "bring": "[start_ts]"
            },
            "end_ts": {
                "type": "timestamp",
                "bring": "[end_ts]"
            },
            "file": {
                "blob": true,
                "bring": "[binaryValue]",
                "extension": "mp4",
                "apply": "base64decoding",
                "hash": "md5",
                "type": "varchar"
            },
            "file_type": {
                "bring": "[mediaType]",
                "type": "string"
            },
            "num_cars": {
                "bring": "[num_cars]",
                "type": "int"
            },
            "speed": {
                "bring": "[speed]",
                "type": "float"
            }
        }
    }
}>
do test_policy = json !mapping_policy test
do if !test_policy == false then goto json-policy-error

:declare-policy
on error call declare-policy-error
policy = blockchain mapping where id=!policy_id
if not !policy then
do blockchain prepare policy !mapping_policy
do blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn


:mqtt-call:
on error goto mqtt-error
<run mqtt client where broker=!broker and port=!port and user-agent=anylog and log=false and topic=(
    name=!mqtt_topic_name and
    policy=!policy_id
)>

:end-script:
end script

:declare-params-error:
echo "Failed to declare one or more policies. Cannot continue..."
goto end-script

:connect-dbms-error:
echo "Failed to connect to MongoDB logical database " !mongo_db_name ". Cannot continue..."
goto end-script

:blobs-archiver-error:
echo "Failed to enable blobs archiver"
return

:json-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:declare-policy-error:
echo "Failed to declare policy on blockchain"
return


:mqtt-error:
echo "Failed to deploy MQTT process"
goto end-script


