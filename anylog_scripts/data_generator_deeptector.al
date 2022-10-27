#-----------------------------------------------------------------------------------------------------------------------
# The following demonstrate receiving data from EdgeX against a single topic with multiple types of data, using policies
# function. For the demonstrating we are using both the Random-Integer-Generator01  & Modbus TCP test device. The example
# expects receiving data via MQTT, with params preset by the configuration file when deploying the AnyLog instance.
#
# :process:
#   1. Set parameters
#   2. Add mapping policies to blockchain (if they don't already exist)
#   3. `run mqtt client` command
#
# :sample data coming in:
#    {
#        "id": "f85b2ddc-761d-88da-c524-12283fbb0f21",
#        "dbms": "ntt",
#        "table": "deeptector",
#        "file_name": "20200306202533614.jpeg",
#        "file_type": "image/jpeg",
#        "file_content": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD",
#        "detection": [
#                {"class": "kizu", "bbox": [666, 275, 682, 291], "score": 0.83249},
#                {"class": "kizu", "bbox": [669, 262, 684, 277], "score": 0.83249},
#                {"class": "kizu", "bbox": [688, 261, 706,276], "score": 0.72732},
#                {"class": "kizu", "bbox": [698, 277, 713, 292], "score": 0.72659},
#        ],
#        "status": "ok"
#    }
# :documents:
#   - Generic MQTT script: !local_scripts/deployment_scripts/mqtt.al
#   - Documentation: https://github.com/AnyLog-co/documentation/blob/master/mapping%20data%20to%20tables.md
#   - Deploying EdgeX: https://github.com/AnyLog-co/lfedge-code/tree/main/edgex
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/sample_code/deeptector.al

:declare-params:
on error ignore
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
run blobs archiver where dbms = true and folder = false and compress=false and reuse_blobs = true
#run blobs archiver where dbms=!blobs_dbms and folder=!blobs_folder and compress=!blobs_compress


:preparre-policy:
policy_id = deeptector
policy = blockchain get mapping where id = !policy_id
if not !policy then
<do mapping_policy = {
    "mapping": {
        "id": !policy_id,
        "dbms": !default_dbms,
        "table": "bring [table]",
	"readings": "detection",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "default": "now()"
            },
            "file": {
                "root" : true,
                "blob" : true,
                "bring" : "[file_content]",
                "extension" : "jpeg",
                "apply" : "base64decoding",
                "hash" : "md5",
                "type" : "varchar"
            },
            "class": {
                "type": "string",
                "bring": "[class]",
		"default": ""
            },
            "bbox": {
                "type": "string",
                "bring": "[bbox]",
                "default": ""
            },
            "score": {
                "type": "float",
                "bring": "[score]",
                "default": -1
            },
            "status": {
                "root": true,
                "type": "string",
                "bring": "[status]",
                "default": ""
            }
	}
    }
}>
do test_policy = json !mapping_policy test
do if !test_policy == false then goto json-policy-error

on error call declare-policy-error
if not !poliicy then 
do blockchain prepare policy !mapping_policy
do blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn


:mqtt-call:
on error goto mqtt-error
<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=!policy_id and
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







