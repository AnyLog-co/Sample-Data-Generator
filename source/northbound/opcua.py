from asyncua import ua, Server
import ast


class OpcuaServer:
    """
    OPC-UA server wrapper that dynamically creates nodes based on MQTT-style topics
    and publishes values to the OPC-UA address space.
    """

    def __init__(self, host:str="0.0.0.0", port:int=4840):
        """
        Initialize OPC-UA server configuration

        :args:
            host:str - host IP address to bind OPC-UA server
            port:int - port to bind OPC-UA server (default: 4840)
        :params:
            self.endpoint:str - OPC-UA endpoint URL
            self.server:Server - asyncua server instance
            self.idx:int|None - namespace index
            self.root:Node|None - root objects node
            self.folder_nodes:dict - cached folder nodes by path
            self.variable_nodes:dict - cached variable nodes by path
            self.variable_types:dict - stored variable types by path
        :return:
            None
        """
        self.endpoint = f"opc.tcp://{host}:{port}/freeopcua/data-generator"

        self.server = Server()
        self.idx = None
        self.root = None

        self.folder_nodes = {}
        self.variable_nodes = {}
        self.variable_types = {}

    # ---------------- Connection ----------------

    async def connect(self):
        """
        Start OPC-UA server and register namespace

        :args:
            None
        :params:
            self.idx:int - namespace index
            self.root:Node - root object node
        :return:
            None
        """
        await self.server.init()
        self.server.set_endpoint(self.endpoint)
        self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

        self.idx = await self.server.register_namespace("http://proveit.demo.opcua")
        self.root = self.server.nodes.objects

        await self.server.start()
        print(f"OPC-UA server started at {self.endpoint}")

    async def disconnect(self):
        """
        Stop OPC-UA server

        :args:
            None
        :return:
            None
        """
        await self.server.stop()

    # ---------------- Payload ----------------

    @staticmethod
    def parse_payload(payload:str|dict):
        """
        Extract value from payload
        :args:
            payload:str|dict - incoming MQTT-style payload
        :params:
            parsed:Any - parsed literal value
        :return:
            Parsed value or original payload
        """
        if isinstance(payload, dict):
            return payload.get("value", payload)

        try:
            parsed = ast.literal_eval(payload)
            if isinstance(parsed, dict):
                return parsed.get("value", parsed)
            return parsed
        except Exception:
            return payload

    # ---------------- Type Handling ----------------

    @staticmethod
    def infer_type(value):
        """
        Infer OPC-UA VariantType from Python value

        :args:
            value:Any - value to inspect
        :return:
            ua.VariantType
        """
        if isinstance(value, bool):
            return ua.VariantType.Boolean
        if isinstance(value, int):
            return ua.VariantType.Int64
        if isinstance(value, float):
            return ua.VariantType.Double
        return ua.VariantType.String

    @staticmethod
    def cast_value(value, vartype:ua.VariantType):
        """
        Cast value into OPC-UA compatible type

        :args:
            value:Any - original value
            vartype:ua.VariantType - target OPC-UA type
        :return:
            Casted value
        """
        if vartype == ua.VariantType.Boolean:
            return bool(value)
        if vartype == ua.VariantType.Int64:
            return int(float(value))
        if vartype == ua.VariantType.Double:
            return float(value)
        return str(value)

    # ---------------- Node Creation ----------------

    async def _get_or_create_folder(self, parent, name:str, path:str):
        """
        Get existing folder node or create new one

        :args:
            parent:Node - parent OPC-UA node
            name:str - folder name
            path:str - full folder path
        :return:
            OPC-UA folder node
        """
        if path in self.folder_nodes:
            return self.folder_nodes[path]

        folder = await parent.add_object(self.idx, name)
        self.folder_nodes[path] = folder
        return folder

    async def _get_or_create_variable(self, parent, name:str, path:str, value):
        """
        Get existing variable node or create new one

        :args:
            parent:Node - parent OPC-UA node
            name:str - variable name
            path:str - full variable path
            value:Any - initial value
        :params:
            vartype:ua.VariantType - inferred OPC-UA type
        :return:
            OPC-UA variable node
        """
        if path in self.variable_nodes:
            return self.variable_nodes[path]

        vartype = self.infer_type(value)
        self.variable_types[path] = vartype

        var = await parent.add_variable(
            self.idx,
            name,
            ua.Variant(self.cast_value(value, vartype), vartype)
        )
        await var.set_writable()

        self.variable_nodes[path] = var
        return var

    async def _build_tree(self, topic:str, value):
        """
        Build OPC-UA node tree based on topic path

        :args:
            topic:str - MQTT-style topic (e.g., site/device/value)
            value:Any - variable value
        :return:
            (variable_node, full_path)
        """
        parts = topic.split("/")
        parent = self.root
        path = ""

        for part in parts[:-1]:
            path += "/" + part
            parent = await self._get_or_create_folder(parent, part, path)

        full_path = path + "/" + parts[-1]
        return await self._get_or_create_variable(parent, parts[-1], full_path, value), full_path

    # ---------------- Publish ----------------

    async def publish_data(self, topic:str, payload):
        """
        Publish value into OPC-UA address space

        :args:
            topic:str - MQTT-style topic path
            payload:Any - value or structured payload
        :params:
            vartype:ua.VariantType - stored OPC-UA type
            safe_value:Any - casted value
        :return:
            None
        """
        if self.root is None:
            await self.connect()

        value = self.parse_payload(payload)
        var, path = await self._build_tree(topic, value)

        vartype = self.variable_types[path]
        safe_value = self.cast_value(value, vartype)

        try:
            await var.write_value(ua.Variant(safe_value, vartype))

        except ua.uaerrors.BadTypeMismatch:
            # Recover by recreating variable with stable type
            del self.variable_nodes[path]

            var = await self._get_or_create_variable(
                self.root,
                path.split("/")[-1],
                path,
                safe_value
            )
            await var.write_value(ua.Variant(safe_value, vartype))