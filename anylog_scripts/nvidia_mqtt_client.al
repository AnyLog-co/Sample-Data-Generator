<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=nvidia-data and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.component=(type=str and value="bring [component]") and
    column.version=(type=str and value="bring [version]") and
    column.caller=(type=str and value="bring [caller]") and
    column.info=(type=str and value="bring [info]") and
    column.targetNamespace=(type=str and value="bring [targetNamespace]") and
    column.release=(type=str and value="bring [release]") and
    column.app=(type=str and value="bring [app]") and
    column.message_size=(type=float and value="bring [message_size]") and
    column.ip=(type=str and value="bring [ip]") and
    column.port=(type=int and value="bring [port]") and
    column.streams=(type=str and value="bring [streams]") and
    column.message_id=(type=str and value="bring [message_id]") and
    column.source=(type=str and value="bring [source]") and
    column.source_input=(type=str and value="bring [source_input]") and
    column.pod=(type=str and value="bring [pod]") and
    column.namespace=(type=str and value="bring [namespace]") and
    column.system=(type=str and value="bring [system]") and
    column.container_name=(type=str and value="bring [container_name]") and
    column.location=(type=str and value="bring [location]") and
    column.source_node=(type=str and value="bring [source_node]") and
    column.id=(type=str and value="bring [id]")
)>

<run mqtt client where broker=broker and port=!anylog_broker_port and log=false and topic=(
    name=nvidia-data and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.component=(type=str and value="bring [component]") and
    column.version=(type=str and value="bring [version]") and
    column.caller=(type=str and value="bring [caller]") and
    column.info=(type=str and value="bring [info]") and
    column.targetNamespace=(type=str and value="bring [targetNamespace]") and
    column.release=(type=str and value="bring [release]") and
    column.app=(type=str and value="bring [app]") and
    column.message_size=(type=float and value="bring [message_size]") and
    column.ip=(type=str and value="bring [ip]") and
    column.port=(type=int and value="bring [port]") and
    column.streams=(type=str and value="bring [streams]") and
    column.message_id=(type=str and value="bring [message_id]") and
    column.source=(type=str and value="bring [source]") and
    column.source_input=(type=str and value="bring [source_input]") and
    column.pod=(type=str and value="bring [pod]") and
    column.namespace=(type=str and value="bring [namespace]") and
    column.system=(type=str and value="bring [system]") and
    column.container_name=(type=str and value="bring [container_name]") and
    column.location=(type=str and value="bring [location]") and
    column.source_node=(type=str and value="bring [source_node]") and
    column.id=(type=str and value="bring [id]")
)>
