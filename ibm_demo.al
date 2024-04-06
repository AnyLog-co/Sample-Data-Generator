#----------------------------------------------------------------------------------------------------------------------#
# AnyLog script to accept data associated with IBM's demo
#----------------------------------------------------------------------------------------------------------------------#
policy_id = ibm-demo

policy = blockchain get mapping where id = !policy_id
if !policy then goto mqtt-call

# Conversion type - we support either base64 or OpenCV, if not set, will use bytesio
conversion_type = base64

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
set policy new_policy [mapping][schema][elapse_timestamp][type] = "int"
set policy new_policy [mapping][schema][elapse_timestamp][default] = "0"
set policy new_policy [mapping][schema][elapse_timestamp][bring] = "[elapseTime]"
set policy new_policy [mapping][schema][elapse_timestamp][root] = true.bool

set policy new_policy [mapping][schema][file_name] = {}
set policy new_policy [mapping][schema][file_name][type] = "string"
set policy new_policy [mapping][schema][file_name][bring] = "[file_name]"
set policy new_policy [mapping][schema][file_name][default] = ""
set policy new_policy [mapping][schema][file][root] = true.bool

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
set policy new_policy [mapping][schema][bbox][default] = ""

set policy new_policy [mapping][schema][score] = {}
set policy new_policy [mapping][schema][score][type] = "float"
set policy new_policy [mapping][schema][score][bring] = "[detectedScore]"
set policy new_policy [mapping][schema][score][default] = "0"

set policy new_policy [mapping][schema][class] = {}
set policy new_policy [mapping][schema][class][type] = "string"
set policy new_policy [mapping][schema][class][bring] = "[detectedClass]"
set policy new_policy [mapping][schema][class][default] = ""

set policy new_policy [mapping][schema][confidence] = {}
set policy new_policy [mapping][schema][confidence][type] = "int"
set policy new_policy [mapping][schema][confidence][default] = "0"
set policy new_policy [mapping][schema][confidence][bring] = "[confidentCutoff]"
set policy new_policy [mapping][schema][confidence][root] = true.bool