"""
Logic dictionaries used for mapping and referencing tables
"""

BASE_POLICY = {
    "mapping": {
        "id": None,
        "dbms": "bring [dbms]",
        "table": "bring [table]",
        "readings": "",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "default": "now()",
                "bring": "[timestamp]"
            }
        }
    }
}


RIG_INFO = {
    1: {
        'file': 'drilling_data_RIG-TX-001.csv',
        'name': 'Permian Basin',
        'region': 'West Texas',
        'loc': '31.5,-102.0',
    },
    7: {
        'file': 'drilling_data_RIG-TX-007.csv',
        'name': 'Eagle Ford',
        'region': 'South Texas',
        'loc': '28.0,-98.0'
    },
    12: {
        'file': 'drilling_data_RIG-ND-012.csv',
        'name': 'Bakken',
        'region': 'North Dakota',
        'loc': '47.5,-102.5'
    },
    23: {
        'file': 'drilling_data_RIG-GOM-023.csv',
        'name': 'Deepwater',
        'region': 'Gulf of Mexico',
        'loc': '26.0,-90.0'
    },
    31: {
        'file': 'drilling_data_RIG-TX-031.csv',
        'name': 'Delaware Basin',
        'region': 'West Texas',
        'loc': '31.5,-103.5'
    },
    44: {
        'file': 'drilling_data_RIG-OK-044.csv',
        'name': 'STACK',
        'region': 'Oklahoma',
        'loc': '35.5,-97.5'
    }
}


WIND_TURBINE_TABLES = {
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

VESSEL_INFO = {

    # ------------------------------------------------------------------
    # Metadata (ALWAYS included in every payload)
    # ------------------------------------------------------------------
    "general": {
        "vessel_name": "string",
        "boat_side": "string",
        "ip_index": "int",
        "motor_id": "int",
        "device": "string"
    },

    # ------------------------------------------------------------------
    # Battery Telemetry
    # ------------------------------------------------------------------
    "battery_telemetry": [
        "batteryStateOfChargePercent",
        "gStateOfCharge",
        "actualSoc",
        "gStateOfHealth",
        "gEnergyRemaining",
        "maxCapacity",
        "hvBatteryCapacity",
        "hvBatteryType",
        "lvBatteryCapacity",
        "lvBatteryMaxCapacity",
        "lvBatteryStateOfChargePercent",
        "lvBatteryType",
        "currentBatteryPower",
        "maxBatteryPower",
        "timeBattery",
        "timeToFullMinute",
        "starterBatteryVoltage",
        "starterBatteryVoltagePercent",
        "cellBalance",
        "gCellBalance",
        "gPowerLimitCharge",
        "gPowerLimitDischarge"
    ],

    # ------------------------------------------------------------------
    # Navigation Telemetry
    # ------------------------------------------------------------------
    "navigation_telemetry": [
        "currentPositionLatitude",
        "currentPositionLongitude",
        "speedOverGround",
        "speedOverGroundFixed",
        "speedThroughWater",
        "trip",
        "distanceHome",
        "distanceDestination",
        "sogValid",
        "currentHeading",
        "headingDestination",
        "headingHome"
    ],

    # ------------------------------------------------------------------
    # Charger Telemetry
    # ------------------------------------------------------------------
    "charger_telemetry": [
        "acChargerPowerPercent",
        "portAcChargerPower",
        "portAcChargerEnable",
        "stbdAcChargerPower",
        "stbdAcChargerEnable",
        "dcacEnable",
        "dcacPower",
        "dcacPowerPercent",
        "dcdcEnable",
        "dcdcPower",
        "dcdcPowerPercent",
        "elPtxPower",
        "elPtxPowerPercent",
        "regenerationPower",
        "regenerationPowerPercent",
        "availablePowerChargeLong",
        "availablePowerChargeShort",
        "availablePowerDischargeLong",
        "availablePowerDischargeShort",
        "maxCurrentCharge",
        "maxCurrentDischarge"
    ],

    # ------------------------------------------------------------------
    # Engine Telemetry
    # ------------------------------------------------------------------
    "engine_telemetry": [
        "motorPowerCombined",
        "motorPowerCombinedPercent",
        "motorPowerLimit",
        "portMotorPower",
        "portMotorPowerPercent",
        "stbdMotorPower",
        "stbdMotorPowerPercent",
        "portRpmShaft",
        "portRpmShaftPercent",
        "stbdRpmShaft",
        "stbdRpmShaftPercent",
        "throttle",
        "drive",
        "powerBalance",
        "maxPower",
        "maxSpeed",
        "selectSystemMode",
        "vesselState",
        "systemState"
    ],

    # ------------------------------------------------------------------
    # AC Power Telemetry
    # ------------------------------------------------------------------
    "ac_power_telemetry": [
        "gActAcCurrent",
        "gActAcVoltage",
        "gActAcFrequency",
        "gCommandAcCurrentLimitPP",
        "gParamMaxAcCurrentPP",
        "gMaxDcPower"
    ],

    # ------------------------------------------------------------------
    # DC Power Telemetry
    # ------------------------------------------------------------------
    "dc_power_telemetry": [
        "gActDcPower",
        "gActDcVoltage",
        "gCommandDcPowerLimit",
        "gCommandMaxDcVoltage"
    ],

    # ------------------------------------------------------------------
    # Thermal Telemetry
    # ------------------------------------------------------------------
    "thermal_telemetry": [
        "gActElectronicTemperature",
        "gAverageTemperature",
        "gMaxCellTemperature",
        "gMinCellTemperature",
        "actualTempBattery",
        "actualTempBatteryMax",
        "actualTempBatteryMin",
        "actualTempHeatexchanger",
        "gCoolingPolicy",
        "coolingRequested",
        "coolingType"
    ],

    # ------------------------------------------------------------------
    # Control State
    # ------------------------------------------------------------------
    "control_state": [
        "gCommand",
        "gState",
        "gWake",
        "gIsSlave",
        "gError",
        "gDisableReason",
        "gSimConnectedPhaseCount",
        "deviceState",
        "systemState"
    ]
}

BASE_VESSEL_FILES = {
    "DLB": {
        "Helios_DLB_BCL25_700_8_CH_IP_3_ID_65": [
            "2024-08-15_Helios_DLB_BCL25_700_8_CH_IP_3_ID_65.json",
            "2024-08-15_Helios_DLB_BCL25_700_8_CH_IP_3_ID_65_DEVICE.json"
        ],
        "Helios_DLB_BCL25_700_8_CH_IP_4_ID_65": [
            "2024-08-15_Helios_DLB_BCL25_700_8_CH_IP_4_ID_65.json",
            "2024-08-15_Helios_DLB_BCL25_700_8_CH_IP_4_ID_65_DEVICE.json"
        ],
        "Helios_DLB_BMWix_IP_3_ID_33": [
            "2024-08-15_Helios_DLB_BMWix_IP_3_ID_33.json",
            "2024-08-15_Helios_DLB_BMWix_IP_3_ID_33_DEVICE.json"
        ],
        "Helios_DLB_BMWix_IP_3_ID_49": [
            "2024-08-15_Helios_DLB_BMWix_IP_3_ID_49.json",
            "2024-08-15_Helios_DLB_BMWix_IP_3_ID_49_DEVICE.json"
        ],
        "Helios_DLB_BMWix_IP_3_ID_81": [
            "2024-08-15_Helios_DLB_BMWix_IP_3_ID_81.json",
            "2024-08-15_Helios_DLB_BMWix_IP_3_ID_81_DEVICE.json"
        ],
        "Helios_DLB_BMWix_IP_4_ID_49": [
            "2024-08-15_Helios_DLB_BMWix_IP_4_ID_49.json",
            "2024-08-15_Helios_DLB_BMWix_IP_4_ID_49_DEVICE.json"
        ],
        "Helios_DLB_vessel": [
            "2024-08-15_Helios_DLB_vessel.json"
        ]
    },

    "DLT": {
        "Helios_DLT_BCL25_700_8_CH_IP_3_ID_65": [
            "2024-08-15_Helios_DLT_BCL25_700_8_CH_IP_3_ID_65.json",
            "2024-08-15_Helios_DLT_BCL25_700_8_CH_IP_3_ID_65_DEVICE.json"
        ],
        "Helios_DLT_BMWix_IP_3_ID_33": [
            "2024-08-15_Helios_DLT_BMWix_IP_3_ID_33.json",
            "2024-08-15_Helios_DLT_BMWix_IP_3_ID_33_DEVICE.json"
        ],
        "Helios_DLT_BMWix_IP_3_ID_49": [
            "2024-08-15_Helios_DLT_BMWix_IP_3_ID_49.json",
            "2024-08-15_Helios_DLT_BMWix_IP_3_ID_49_DEVICE.json"
        ],
        "Helios_DLT_BMWix_IP_3_ID_81": [
            "2024-08-15_Helios_DLT_BMWix_IP_3_ID_81.json",
            "2024-08-15_Helios_DLT_BMWix_IP_3_ID_81_DEVICE.json"
        ],
        "Helios_DLT_BMWix_IP_4_ID_49": [
            "2024-08-15_Helios_DLT_BMWix_IP_4_ID_49.json",
            "2024-08-15_Helios_DLT_BMWix_IP_4_ID_49_DEVICE.json"
        ],
        "Helios_DLT_vessel": [
            "2024-08-15_Helios_DLT_vessel.json"
        ]
    }
}



# VESSEL_INFO = {
#     "anotherpeak-tier1": {
#         "file_id": "vessel.json",
#         "tables": {
#             "battery_telemetry": [
#                 "batteryStateOfChargePercent",
#                 "hvBatteryCapacity",
#                 "hvBatteryType",
#                 "lvBattery*",
#                 "currentBatteryPower",
#                 "maxBatteryPower",
#                 "timeBattery",
#                 "timeToFullMinute",
#                 "starterBatteryVoltage"
#                 "starterBatteryVoltagePercent"
#             ],
#             "navigation_telemetry": [
#                 "currentPositionLatitude",
#                 "currentPositionLongitude",
#                 "speedOverGround",
#                 "speedOverGroundFixed",
#                 "speedThroughWater",
#                 "heading*",
#                 "distance*",
#                 "trip",
#                 "sogValid"
#             ],
#             "charger_telemetry": [
#                 "acChargerPowerPercent",
#                 "portAcCharger*",
#                 "stbdAcCharger*",
#                 "elPtx*",
#                 "dcac*",
#                 "dcdc*",
#                 "regeneration*"
#             ],
#             "engine_telemetry": [
#             "motor*",
#             "rpm*",
#             "throttle*",
#             "drive*",
#             "powerBalance",
#             "maxPower",
#             "maxSpeed",
#             "selectSystemMode",
#             "vesselState",
#             "systemState"
#         ],
#         },
#     },
#     "anotherpeak-tier2": {
#         "file_id": "ID_65.json",
#         "tables": {
#             "ac_power_telemetry": [
#                 "gActAcCurrent",
#                 "gActAcVoltage",
#                 "gActAcFrequency",
#                 "gCommandAcCurrentLimitPP",
#                 "gMaxDcPower",
#                 "gParamMaxAcCurrentPP"
#             ],
#             "dc_power_telemetry": [
#                 "gActDcPower",
#                 "gActDcVoltage",
#                 "gCommandDcPowerLimit",
#                 "gCommandMaxDcVoltage"
#             ],
#             "thermal_telemetry": [
#                 "gActElectronicTemperature",
#                 "gCoolingPolicy"
#             ],
#             "control_state": [
#             "gCommand",
#             "gState",
#             "gWake",
#             "gIsSlave",
#             "gError",
#             "gDisableReason",
#             "gSimConnectedPhaseCount"
#         ]
#         }
#     }
# }
