#----------------------------------------------------------------------------------------------------------------------#
# Using a column for table / column  vessel data example - demonstrate aggregations with data being stored
# Table: battery_pack_logs | column: gcurrent used for aggregatioon
# :process:
#   1. connect to aggregation logical database
#   2. set aggregation
#   3. set aggregation encoding
#   4. set aggregation ingest
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/data-generator/vessel_aggregation_demo.al

on error ignore

:set-param:
agg_dbms = agg_ + !default_dbms

:connect-dbms:
on error goto connect-dbms-err
connect dbms !agg_dbms where type=sqlite

:set-aggregation:
on error goto aggregation-err
<set aggregation where
    dbms = !default_dbms and
    table = battery_pack_logs and
    target_dbms =  !agg_dbms and
    target_table = battery_pack_logs_gcurrent and
    intervals = 10 and
    time = 1 minute and
    time_column = timestamp and
    value_column = gcurrent>

on error goto aggregation-encoding-err
<set aggregation encoding where
    dbms = !default_dbms and
    table = battery_pack_logs and
    value_column = gcurrent and
    encoding = bounds and
    tolerance = 0>

on error goto aggregation-ingest-err
<set aggregation ingest where
    dbms = !default_dbms  and
    table = battery_pack_logs and
    source = true and
    derived = true>

:end-script:
end script

:connect-dbms-err:
echo "Failed to connect to " !agg_dbms
goto end-script

:aggregation-err:
echo "Failed to execute `set aggregation`"
goto end-script

:aggregation-encoding-err:
echo "Failed to execute `set aggregation encoding`"
goto end-script


:aggregation-ingest-err:
echo "Failed to execute `set aggregation ingest`"
goto end-script