<run mqtt client where broker=local  and port=2450 and log=false and topic=(
    name=test and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.line=(type=int and value="bring [line]" and optional=true)  and
    column.component=(type=str and value="bring [component]" and optional=true) and
	column.version=(type=str and value="bring [version]" and optional=true) and
	column.info=(type=str and value="bring [info]" and optional=true) and
	column.target_namespace=(type=str and value="bring [target_namespace]" and optional=true) and
	column.release=(type=str and value="bring [release]" and optional=true) and
	column.app=(type=str and value="bring [app]" and optional=true) and
	column.app_release=(type=str and value="bring [app_release]" and optional=true) and
	column.source=(type=str and value="bring [source]" and optional=true) and
	column.system=(type=str and value="bring [system]" and optional=true) and
	column.pod_name=(type=str and value="bring [pod_name]" and optional=true) and
	column.namespace=(type=str and value="bring [namespace]" and optional=true) and
	column.app_component=(type=str and value="bring [app_component]" and optional=true) and
	column.container=(type=str and value="bring [container]" and optional=true) and
	column.location=(type=str and value="bring [location]" and optional=true) and
	column.node_id=(type=str and value="bring [node_id]" and optional=true) and
	column.remote_ip=(type=str and value="bring [remote_ip]" and optional=true) and
	column.remote_port=(type=int and value="bring [remote_port]" and optional=true) and
	column.message_id=(type=str and value="bring [message_id]" and optional=true) and
	column.source_input=(type=str and value="bring [source_input]" and optional=true) and
	column.source_node=(type=str and value="bring [source_node]" and optional=true) and
	column.resource=(type=str and value="bring [resource]" and optional=true) and
	column.helm_version=(type=str and value="bring [helm_version]" and optional=true) and
	column.using_post_renderer=(type=str and value="bring [using_post_renderer]" and optional=true) and
	column.action=(type=str and value="bring [action]" and optional=true) and
	column.phase=(type=str and value="bring [phase]" and optional=true) and
	column.checksum_updated=(type=str and value="bring [checksum_updated]" and optional=true) and
	column.error=(type=str and value="bring [error]" and optional=true) and
	column.warning=(type=str and value="bring [warning]" and optional=true) and
	column.succeeded=(type=str and value="bring [succeeded]" and optional=true) and
	column.revision=(type=str and value="bring [revision]" and optional=true) and
	column.kustomization_hook=(type=str and value="bring [kustomization_hook]" and optional=true) and
	column.kustomization_hook_path=(type=str and value="bring [kustomization_hook_path]" and optional=true) and
	column.kustomization_config=(type=str and value="bring [kustomization_config]" and optional=true) and
	column.kustomization_path=(type=str and value="bring [kustomization_path]" and optional=true) and
	column.msg=(type=str and value="bring [msg]" and optional=true) and
	column.latest=(type=str and value="bring [latest]" and optional=true) and
	column.url=(type=str and value="bring [url]" and optional=true) and
	column.exiting=(type=str and value="bring [exiting]" and optional=true) and
	column.name=(type=str and value="bring [name]" and optional=true) and
	column.loop=(type=str and value="bring [loop]" and optional=true) and
	column.err=(type=str and value="bring [err]" and optional=true)
)>

