#----------------------------------------------------------------------------------------------------------------------#
# AnyLog script to accept data associated with IBM's demo
#----------------------------------------------------------------------------------------------------------------------#
on error ignore

:preparre-policy:
policy_id = ibm-demo
policy = blockchain get mapping where id = !policy_id
if !policy then goto mqtt-call

# Conversion type - we support either base64 or OpenCV, if not set, will use bytesio
conversion_type = base64

:create-policy:
set new_policy = ""
set policy new_policy [mapping] = {}
set policy new_policy [mapping][id] = !policy_id
set policy new_policy [mapping][dbms] = "bring [dbms]"
set policy new_policy [mapping][table] = "bring [name]"
set policy new_policy [mapping][readings] = "bbox"

set policy new_policy [mapping][schema] = {}

set policy new_policy [mapping][schema][timestamp] = {}
set policy new_policy [mapping][schema][timestamp][type] = "timestamp"
set policy new_policy [mapping][schema][timestamp][default] = "now()"

set policy new_policy [mapping][schema][elapse_timestamp] = {}
set policy new_policy [mapping][schema][elapse_timestamp][type] = "float"
set policy new_policy [mapping][schema][elapse_timestamp][default] = "0"
set policy new_policy [mapping][schema][elapse_timestamp][bring] = "[elapseTime]"
set policy new_policy [mapping][schema][elapse_timestamp][root] = true.bool

set policy new_policy [mapping][schema][file_name] = {}
set policy new_policy [mapping][schema][file_name][type] = "string"
set policy new_policy [mapping][schema][file_name][bring] = "[file_name]"
set policy new_policy [mapping][schema][file_name][root] = true.bool

set policy new_policy [mapping][schema][file] = {}
set policy new_policy [mapping][schema][file][root] = true.bool
set policy new_policy [mapping][schema][file][blob] = true.bool
set policy new_policy [mapping][schema][file][bring] = "[file_content]"
set policy new_policy [mapping][schema][file][extension] = "jpg"
set policy new_policy [mapping][schema][file][hash] = "md5"
set policy new_policy [mapping][schema][file][type] = "varchar"
set policy new_policy [mapping][schema][file][apply] = "base64decoding"

set policy new_policy [mapping][schema][bbox] = {}
set policy new_policy [mapping][schema][bbox][type] = "string"
set policy new_policy [mapping][schema][bbox][bring] = "[detectionBox]"

set policy new_policy [mapping][schema][score] = {}
set policy new_policy [mapping][schema][score][type] = "float"
set policy new_policy [mapping][schema][score][bring] = "[detectedScore]"
set policy new_policy [mapping][schema][score][default] = "0"

set policy new_policy [mapping][schema][class] = {}
set policy new_policy [mapping][schema][class][type] = "string"
set policy new_policy [mapping][schema][class][bring] = "[detectedClass]"

set policy new_policy [mapping][schema][confidence] = {}
set policy new_policy [mapping][schema][confidence][type] = "int"
set policy new_policy [mapping][schema][confidence][default] = "0"
set policy new_policy [mapping][schema][confidence][bring] = "[confidentCutoff]"
set policy new_policy [mapping][schema][confidence][root] = true.bool

:declare-policy:
test_policy = json !mapping_policy test
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

