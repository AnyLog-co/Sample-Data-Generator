from asyncua import ua, Server
import ast


class OpcuaServer:
    def __init__(self, host="0.0.0.0", port=4840):
        self.endpoint = f"opc.tcp://{host}:{port}/freeopcua/data-generator"

        self.server = Server()
        self.idx = None
        self.root = None

        self.folder_nodes = {}
        self.variable_nodes = {}
        self.variable_types = {}  # 🔒 path -> ua.VariantType

    # ---------------- Connection ----------------

    async def connect(self):
        await self.server.init()
        self.server.set_endpoint(self.endpoint)
        self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

        self.idx = await self.server.register_namespace("http://proveit.demo.opcua")
        self.root = self.server.nodes.objects

        await self.server.start()
        print(f"OPC-UA server started at {self.endpoint}")

    async def disconnect(self):
        await self.server.stop()

    # ---------------- Payload ----------------

    @staticmethod
    def parse_payload(payload):
        if isinstance(payload, dict):
            return payload.get("value", payload)
        try:
            parsed = ast.literal_eval(payload)
            if isinstance(parsed, dict):
                return parsed.get("value", parsed)
            return parsed
        except:
            return payload

    # ---------------- Type Handling ----------------

    @staticmethod
    def infer_type(value):
        if isinstance(value, bool):
            return ua.VariantType.Boolean
        if isinstance(value, int):
            return ua.VariantType.Int64
        if isinstance(value, float):
            return ua.VariantType.Double
        return ua.VariantType.String

    @staticmethod
    def cast_value(value, vartype):
        if vartype == ua.VariantType.Boolean:
            return bool(value)
        if vartype == ua.VariantType.Int64:
            return int(float(value))
        if vartype == ua.VariantType.Double:
            return float(value)
        return str(value)

    # ---------------- Node Creation ----------------

    async def _get_or_create_folder(self, parent, name, path):
        if path in self.folder_nodes:
            return self.folder_nodes[path]

        folder = await parent.add_object(self.idx, name)
        self.folder_nodes[path] = folder
        return folder

    async def _get_or_create_variable(self, parent, name, path, value):
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

    async def _build_tree(self, topic, value):
        parts = topic.split("/")
        parent = self.root
        path = ""

        for part in parts[:-1]:
            path += "/" + part
            parent = await self._get_or_create_folder(parent, part, path)

        full_path = path + "/" + parts[-1]
        return await self._get_or_create_variable(parent, parts[-1], full_path, value), full_path

    # ---------------- MQTT-style Publish ----------------

    async def publish_data(self, topic: str, payload):
        value = self.parse_payload(payload)
        var, path = await self._build_tree(topic, value)

        vartype = self.variable_types[path]
        safe_value = self.cast_value(value, vartype)

        try:
            await var.write_value(ua.Variant(safe_value, vartype))

        except ua.uaerrors.BadTypeMismatch:
            # 🔥 Recover safely by re-creating variable with stable type
            del self.variable_nodes[path]

            var = await self._get_or_create_variable(
                self.root,
                path.split("/")[-1],
                path,
                safe_value
            )
            await var.write_value(ua.Variant(safe_value, vartype))
