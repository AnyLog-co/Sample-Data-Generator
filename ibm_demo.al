#----------------------------------------------------------------------------------------------------------------------#
# AnyLog script to accept data associated with IBM"s demo
#----------------------------------------------------------------------------------------------------------------------#
# process $EDGELAKE_PATH/deployment-scripts/demo-scripts/ibm_demo.al

on error ignore

:preparre-policy:
policy_id = ibm-demo
policy = blockchain get mapping where id = !policy_id
if !policy then goto mqtt-call

# Conversion type - we support either base64 or OpenCV, if not set, will use bytesio
conversion_type = base64

:create-policy:
<new_policy={"mapping": {
    "id": !policy_id,
    "dbms": "bring [dbms]",
    "table": "bring [table]",
    "readings": "bbox",
    "schema": {
        "timestamp": {
            "type": "timestamp", 
            "default": "now()",
            "bring": "[timestamp]"
        },
        "elapse_timestamp": {
            "type": "float", 
            "default": 0,
            "bring": "[elapseTime]",
            "root": true
        },
        "file_name": {
            "type": "string", 
            "bring": "[file_name]",
            "root": true, 
            "default": "UNKNOWN"
        },
        "file": {
            "root": true,
            "blob": true,
            "bring": "[file_content]",
            "extension": "jpg",
            "hash": "md5",
            "type": "varchar",
            "apply": "base64decoding"
        },
        "bbox": {
            "type": "string", 
            "bring": "[detectedBox]",
            "default": ""
        },
        "score": {
            "type": "float",
            "bring": "[detectedScore]",
            "default": "0"
        },
        "class": {
            "type": "string",
            "bring": "[detectedClass]",
            "default": ""
        },
        "confidence": {
            "type": "int",
            "bring": "[confidentCutoff]",
            "root": true
        }
    }
}}>


:declare-policy:
test_policy = json !new_policy test
if !test_policy == false then goto json-policy-error
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn


:mqtt-call:
on error goto mqtt-error
if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>
else if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and user-agent=anylog and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>
else if not !anylog_broker_port then
<do run msg client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
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

