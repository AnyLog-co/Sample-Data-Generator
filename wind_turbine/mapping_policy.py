import copy
import locale
locale.setlocale(locale.LC_NUMERIC, "de_DE.UTF-8") # configure code to use German formatting

from source.rest_calls import RestClient
from source.support import declare_policy

TABLES = {
    "identity": {  # identity / identification
        "turbine_id": "Anlage",
        "alias": "Alias",
        "timestamp": "Zeit"
    },

    "wind": {  # wind measurements
        "wind_avg": "Wind Ø [m/s]",
        "wind_max": "Wind max. [m/s]",
        "wind_min": "Wind min. [m/s]"
    },

    "rpm": {  # rotational speed
        "rpm_avg": "Drehzahl Ø [1/min]",
        "rpm_max": "Drehzahl max. [1/min]",
        "rpm_min": "Drehzahl min. [1/min]"
    },

    "power_output": {  # power output
        "power_avg": "Leistung Ø [kW]",
        "power_max": "Leistung max. [kW]",
        "power_min": "Leistung min. [kW]"
    },

    "available_power": {  # available power
        "avail_wind": "Leistung Verfügb. Wind Ø [kW]",
        "avail_tech": "Leistung Verfügb. techn. Ø [kW]",
        "avail_force_majeure": "Leistung Verfügb. force maj. Ø [kW]",
        "avail_external": "Leistung Verfügb. ext. Ø [kW]"
    },

    "reactive_power": {  # reactive power
        "reactive_avg": "Blindleistung Ø [kvar]",
        "reactive_max": "Blindleistung max. [kvar]",
        "reactive_min": "Blindleistung min. [kvar]"
    },

    "energy": {  # energy produced
        "energy_kwh": "Energie prod. [kWh]"
    },

    "blade_pitch": {  # blade pitch angle
        "pitch_avg": "Blattwinkel Ø [°]"
    },

    "precipitation": {  # rainfall / precipitation
        "precip_avg": "Niederschlag Ø [mm/min]",
        "precip_max": "Niederschlag max. [mm/min]",
        "precip_min": "Niederschlag min. [mm/min]"
    },

    "visibility": {  # visibility
        "visibility_avg": "Sichtweite Ø [km]",
        "visibility_max": "Sichtweite max. [km]",
        "visibility_min": "Sichtweite min. [km]"
    },

    "ambient_light": {  # ambient brightness
        "ambient_avg": "Umfeldhelligkeit Ø [Lux]"
    },

    "ice_detection": {  # ice detection
        "ice_amplitude_avg": "Labko Eis Amplitude Ø [%]",
        "icing_rate_avg": "Eisans. timer Ø [°C/min]"
    },

    "atmosphere": {  # atmospheric conditions
        "pressure_avg": "Luftdruck Ø [mBar]",
        "humidity_avg": "Luftfeuchtigkeit Ø [%]"
    },

    "operations": {  # operational runtime
        "operating_hours": "Betriebsstunden",
        "nacelle_position": "Gondelposition [°]"
    }
}

MAPPING_POLICY = {
    "mapping": {
        "id": "",
        "dbms": "wind_turbine",
        "table": "wind_turbine",
        "readings": "",
        "schema": {
            "turbine_id": { # turbine_id
                "type": "int",
                "bring": "[Anlage]"
            },
            "timestamp": { # timestamp
                "type": "timestamp",
                "bring": "[Zeit]",
                "default": "now()"
            },
            "alias": { # turbine_alias
                "type": "string",
                "bring": "[Alias]"
            }
        }
    }
}

# def __read_line(read_file:str):
#     if not read_file:
#         raise FileNotFoundError("Failed to locate file to generate policies from")
#
#     # extract line
#     try:
#         sample_data = None
#         with open(read_file, mode='r', encoding="utf-8-sig") as f:
#             for line in f:
#                 line = line.strip()
#                 if not line:
#                     continue
#                 return json.loads(line)
#         if not sample_data:
#             raise ValueError(f"No valid JSON found in {read_file}")
#     except Exception as error:
#         raise Exception(f"Failed to read content in file {read_file} (Error: {error})")

def generate_mapping_policy(conn:RestClient=None):
    """
    Declare mapping policy for wind turbine data

    1. read first row in JSON
    2. declare tables and MQTT policy
    3. declare uns policies
    """
    policies = []

    # Generate mapping policies and print table columns
    for table in TABLES:
        mapping_policy = copy.deepcopy(MAPPING_POLICY)
        mapping_policy["mapping"]["id"] = table.replace("_", "-")
        mapping_policy["mapping"]["table"] = table

        print(f"\nTable: {table}")
        for column in TABLES[table]:
            column_name = column.split(' Ø ')[0].split('[')[0].strip().lower().replace('.','').replace(' ', '_')
            mapping_policy["mapping"]["schema"][column_name] = {
                "type": "float",
                "bring": f"[{TABLES.get(table).get(column)}]"
            }

        declare_policy(conn=conn, policy=mapping_policy)
        # print(json.dumps(mapping_policy, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    generate_mapping_policy(conn=None)


