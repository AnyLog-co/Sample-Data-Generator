#----------------------------------------------------------------------------------------------------------------------#
# The following provides an example for pulling data via OPC-UA from Enterprise A (ProveIT 2026)
# The data consists of 2 parts: Utilities (Opto22) and content from 3 silos
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/opcua_enterprise_a.al

on error ignore

:set-params:
tags_file = !tmp_dir/opcua_tags.al
client_file = !tmp_dir/opcua_client.al

:define-tags:
on error call define-tags-err
is_file = file test !tags_file
if !is_file == true then goto process-tags

<get opcua struct where
    url = opc.tcp://172.233.108.122:4841/freeopcua/data-generator and
    node = "ns=2;i=1" and
    dbms = !default_dbms and
    format = policy and
    schema = true and
    class = variable and
    target = "local = true and master = !ledger_conn" and
    output = !tags_file>


:process-tags:
on error ignore

is_file = if test !tags_file
if not !is_file goto missing-file-tags
process !tags_file

:define-client:

:declare-client:
on error call declare-client-err
is_file = file test !client_file
if !is_file == true then goto process-client

<get opcua struct where
    url = opc.tcp://172.233.108.122:4841/freeopcua/data-generator and
    node = "ns=2;i=1" and
    dbms = !default_dbms and
    frequency = 5 and
    format = run_client  and
    class = variable and
    name=opcua-data-gen and
    output = !client_file>


:process-client:
on error ignore

is_file = if test !client_file
if not !is_file then goto missing-file-client
process !client_file


:end-script:
end-script

:missing-file-tags:
echo "Failed to create !file_opcua_tags file - cannot continue"
goto end-script

:missing-file-client:
echo "Failed to create !file_opcua_client file - cannot continue"
goto end-script
