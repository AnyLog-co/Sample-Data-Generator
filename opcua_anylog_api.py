import argparse
import requests


NAMESPACE = {
    "large": 2,
    "ping": [3, 1],
    "percentagecpu": [3, 2],
    "rand": [4, 1],
    "r_50": [5, 1]
}

def rest_command(conn:str, cmd_type:str, command:str, struct_attributes:str=None):
    headers = {
        "command": command.replace("\n", "").replace("<", "").replace(">", "").replace("\r", ""),
        "User-Agent": "AnyLog/1.23"
    }

    output = None
    try:
        if cmd_type.lower() == 'get':
            r = requests.get(url=f"http://{conn}", headers=headers)
        elif cmd_type.lower() == 'post':
            r = requests.post(url=f"http://{conn}", headers=headers)
    except Exception as error:
        raise Exception(f"Failed to execute {cmd_type.upper()} against {conn} (Error: {error})")
    else:
        if not 200 <= int(r.status_code) < 300:
            raise ConnectionError(f"Failed to execute {cmd_type.upper()} against {conn} (Error: {r.status_code})")
        elif 'get opcua values' in r.text:
            cmd = r.text
            if struct_attributes is not None:
                 cmd = cmd.replace(">", f" and include={struct_attributes}")
            output = rest_command(conn=conn, cmd_type='GET', command=cmd)
        elif 'get opcua values' in command:
            print(headers['command'])
            output = r.text
        else:
            rest_command(conn=conn, cmd_type='POST', command=r.text)

    return output

def execute_process(conn:str, namespace:str, opcua_conn:str, struct_class:str, struct_format:str, struct_frequency,
                    table_count:int, disable_validate:bool, struct_attributes:str):
    if namespace != 'large':
        index = NAMESPACE[namespace][1]
        namespace = NAMESPACE[namespace][0]
    else:
        namespace = NAMESPACE[namespace]
        index = "%s"

    node = f'"ns={namespace};i={index}"'

    command = f"""<get opcua struct where
      url = opc.tcp://{opcua_conn}/freeopcua/data-generator and
      node={node} and
      class = {struct_class} and
      format = {struct_format} and
      frequency = {struct_frequency} and
      validate = {str(disable_validate).lower()}>
    """
    if namespace == 2:
        for id in range(1, table_count+1):
            output = rest_command(conn=conn, cmd_type='GET', command=command % id, struct_attributes=struct_attributes)
            if struct_format == 'get_value':
                print(output)
    else:
        output = rest_command(conn=conn, cmd_type='GET', command=command, struct_attributes=struct_attributes)
    if struct_format == 'get_value':
        print(output)


def main():
    namespace_options = list(NAMESPACE.keys())
    namespace_options.append('all')
    parse = argparse.ArgumentParser()
    parse.add_argument('conn',       type=str, default='127.0.0.1:32149', help='REST connection information')
    parse.add_argument('db_name',    type=str, default='new_company',     help='logical database name')
    parse.add_argument('opcua_conn', type=str, default='127.0.0.1:4840',  help='OPC-UA IP and Port')
    parse.add_argument('namespace',  type=str, default='rand',            choices=namespace_options,
                       help='service to get data from')
    parse.add_argument('--struct-class', type=str, default='variable', choices=['variable', 'object'],
                       help='Filter the Tree traversal to show only nodes in the listed class.')
    parse.add_argument('--struct-format', type=str, default='get_value', choices=['get_value', 'run_client'],
                       help='The format of the output')
    parse.add_argument('--struct-frequency', type=str, default='10 hz',
                       help='If output generates "run_client" - the frequency of the "run client" command')
    parse.add_argument('--struct-disable-validate', type=bool, nargs='?', const=False, default=True,
                       help='A boolean value. If set to True, the value from each visited node is read ')
    parse.add_argument('--struct-attributes', type=str, default=None, choices=[None, '*', 'all'],
                       help='Attribute names to consider or * for all')
    parse.add_argument('--table-count', type=int,  default=10, help='number of tables in `large`')
    args = parse.parse_args()

    if args.namespace == 'all':
        for namespace in NAMESPACE:
            execute_process(namespace=namespace, conn=args.conn, opcua_conn=args.opcua_conn, struct_class=args.struct_class,
                            struct_format=args.struct_format, struct_frequency=args.struct_frequency,
                            table_count=args.table_count, disable_validate=args.struct_disable_validate,
                            struct_attributes=args.struct_attributes)
    else:
        execute_process(namespace=args.namespace, conn=args.conn, opcua_conn=args.opcua_conn, struct_class=args.struct_class,
                        struct_format=args.struct_format, struct_frequency=args.struct_frequency,
                        disable_validate=args.struct_disable_validate, struct_attributes=args.struct_attributes)


if __name__ == '__main__':
    main()

