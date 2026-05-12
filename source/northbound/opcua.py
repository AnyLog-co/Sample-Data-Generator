import asyncio
import json

try:
    from asyncua import ua, Server
except ImportError:
    _missing_opcua = True
else:
    _missing_opcua = False
    

class OpcuaServer:
    """
    OPC-UA server wrapper that dynamically creates nodes based on MQTT-style topics
    and publishes values to the OPC-UA address space.

    Payload handling:
        - Scalars (bool, int, float, str) are written with inferred OPC-UA types
        - Dicts and lists are serialized to JSON and written as String nodes
        - Binary blobs (bytes/bytearray) are written as ByteString nodes
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 4840):
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
            self._init_lock:asyncio.Lock - guards lazy initialisation against concurrent callers
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

        self._init_lock = asyncio.Lock()

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
    def normalise_payload(payload):
        """
        Reduce any incoming payload to a scalar that OPC-UA can store.

        Rules:
            bool / int / float / str  →  kept as-is (type-inferred later)
            dict / list               →  serialized to a JSON string
            bytes / bytearray         →  kept as-is (written as ByteString)
            anything else             →  str()

        :args:
            payload:Any - raw incoming payload
        :return:
            bool | int | float | str | bytes | bytearray
        """
        if isinstance(payload, (bool, int, float, str, bytes, bytearray)):
            return payload
        if isinstance(payload, (dict, list)):
            return json.dumps(payload)
        return str(payload)

    # ---------------- Type Handling ----------------

    @staticmethod
    def infer_type(value) -> ua.VariantType:
        """
        Infer OPC-UA VariantType from a normalised Python value.

        Note: bool must be checked before int because bool is a subclass of int.

        :args:
            value:Any - normalised value
        :return:
            ua.VariantType
        """
        if isinstance(value, bool):
            return ua.VariantType.Boolean
        if isinstance(value, int):
            return ua.VariantType.Int64
        if isinstance(value, float):
            return ua.VariantType.Double
        if isinstance(value, (bytes, bytearray)):
            return ua.VariantType.ByteString
        return ua.VariantType.String

    @staticmethod
    def cast_value(value, vartype: ua.VariantType):
        """
        Cast a normalised value into the target OPC-UA type.

        :args:
            value:Any - normalised value
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
        if vartype == ua.VariantType.ByteString:
            return bytes(value)
        return str(value)

    # ---------------- Node Creation ----------------

    async def _ensure_connected(self):
        """
        Lazily connect the server, guarded by a lock so concurrent
        callers do not race through initialisation.

        :args:
            None
        :return:
            None
        """
        if self.root is None:
            async with self._init_lock:
                if self.root is None:  # double-checked inside the lock
                    await self.connect()

    async def _get_or_create_folder(self, parent, name: str, path: str):
        """
        Get existing folder node or create a new one.

        :args:
            parent:Node - parent OPC-UA node
            name:str - folder display name
            path:str - full folder path (cache key)
        :return:
            OPC-UA folder node
        """
        if path in self.folder_nodes:
            return self.folder_nodes[path]

        folder = await parent.add_object(self.idx, name)
        self.folder_nodes[path] = folder
        return folder

    async def _get_or_create_variable(self, parent, name: str, path: str, value):
        """
        Get existing variable node or create a new one under the given parent.

        The type is inferred once from the first value and locked for the
        lifetime of the node.  If the type later changes (BadTypeMismatch),
        the caller is responsible for dropping the cached node and recreating
        it via this method with a fresh value.

        :args:
            parent:Node - parent OPC-UA node
            name:str - variable display name
            path:str - full variable path (cache key)
            value:Any - initial (normalised) value
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

    async def _build_tree(self, topic: str, value):
        """
        Walk the topic path and return the leaf variable node together
        with its full path and direct parent node.

        Returning the parent fixes the orphan-on-recovery bug: if the
        variable needs to be recreated after a BadTypeMismatch, we re-attach
        it to the correct parent rather than hoisting it to self.root.

        :args:
            topic:str - MQTT-style topic (e.g., site/device/sensor)
            value:Any - normalised variable value
        :return:
            (variable_node, full_path, parent_node)
        """
        parts = topic.split("/")
        parent = self.root
        path = ""

        for part in parts[:-1]:
            path += "/" + part
            parent = await self._get_or_create_folder(parent, part, path)

        full_path = path + "/" + parts[-1]
        var = await self._get_or_create_variable(parent, parts[-1], full_path, value)
        return var, full_path, parent

    # ---------------- Publish ----------------

    async def publish_data(self, topic: str, payload):
        """
        Publish a value into the OPC-UA address space.

        Any payload type is accepted:
            - Scalars are written with inferred OPC-UA types.
            - Dicts / lists are JSON-serialised and written as String nodes.
            - Bytes are written as ByteString nodes.

        On a BadTypeMismatch (e.g., the first write was a string but the
        node is now receiving an int) the stale node is evicted from the
        cache and recreated under the correct parent with the new type.

        :args:
            topic:str - MQTT-style topic path
            payload:Any - raw value or structured payload
        :return:
            None
        """
        await self._ensure_connected()

        value = self.normalise_payload(payload)
        var, path, parent = await self._build_tree(topic, value)

        vartype = self.variable_types[path]
        safe_value = self.cast_value(value, vartype)

        try:
            await var.write_value(ua.Variant(safe_value, vartype))

        except ua.uaerrors.BadTypeMismatch:
            # Evict the stale node and recreate it under the correct parent
            # with the type inferred from the new value.
            del self.variable_nodes[path]
            del self.variable_types[path]

            var = await self._get_or_create_variable(
                parent,                  # correct parent, not self.root
                path.split("/")[-1],
                path,
                safe_value
            )
            await var.write_value(
                ua.Variant(safe_value, self.variable_types[path])
            )