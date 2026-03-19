"""
Logic dictionaries used for mapping and referencing tables
"""
# Base
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


# Oil Rigs
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

# Wind Turbine
# Wind Turbine
WIND_TURBINE_TABLES = {

    "identity": {
        "turbine_id": "Anlage",
        "alias": "Alias",
        "timestamp": "Zeit"
    },

    "wind": {
        "wind_avg": "Wind Ø [m/s]",
        "wind_max": "Wind max. [m/s]",
        "wind_min": "Wind min. [m/s]"
    },

    "rpm": {
        "rpm_avg": "Drehzahl Ø [1/min]",
        "rpm_max": "Drehzahl max. [1/min]",
        "rpm_min": "Drehzahl min. [1/min]"
    },

    "power_output": {
        "power_avg": "Leistung Ø [kW]",
        "power_max": "Leistung max. [kW]",
        "power_min": "Leistung min. [kW]"
    },

    "available_power": {
        "avail_wind": "Leistung Verfügb. Wind Ø [kW]",
        "avail_tech": "Leistung Verfügb. techn. Ø [kW]",
        "avail_force_majeure": "Leistung Verfügb. force maj. Ø [kW]",
        "avail_external": "Leistung Verfügb. ext. Ø [kW]"
    },

    "reactive_power": {
        "reactive_avg": "Blindleistung Ø [kvar]",
        "reactive_max": "Blindleistung max. [kvar]",
        "reactive_min": "Blindleistung min. [kvar]"
    },

    "energy": {
        "energy_kwh": "Energie prod. [kWh]"
    },

    "blade_pitch": {
        "pitch_avg": "Blattwinkel Ø [°]"
    },

    "precipitation": {
        "precip_avg": "Niederschlag Ø [mm/min]",
        "precip_max": "Niederschlag max. [mm/min]",
        "precip_min": "Niederschlag min. [mm/min]"
    },
    # FIX 1: visibility fields (previously ignored)
    "visibility": {
        "visibility_avg": "Sichtweite Ø [km]",
        "visibility_max": "Sichtweite max. [km]",
        "visibility_min": "Sichtweite min. [km]"
    },
    "ambient_light": {
        "ambient_avg": "Umfeldhelligkeit Ø [Lux]"
    },

    # FIX 2: ice amplitude field (missing before)
    "ice_detection": {
        "ice_amplitude_avg": "Labko Eis Amplitude Ø [%]",
        "icing_rate_avg": "Eisans. timer Ø [°C/min]"
    },

    "atmosphere": {
        "pressure_avg": "Luftdruck Ø [mBar]",
        "humidity_avg": "Luftfeuchtigkeit Ø [%]"
    },

    "operations": {
        "operating_hours": "Betriebsstunden",
        "nacelle_position": "Gondelposition [°]"
    }
}

WIND_TURBINE_MAPPING = {
    # ── Status ──────────────────────────────────────────────────────────────
    "WT1 - Status a [-]":                                                  "STATUS_A",
    "WT1 - Status b [-]":                                                  "STATUS_B",
    # ── Bearing temperatures ────────────────────────────────────────────────
    "WT1 - Temperature 1 - spinner (SPINNER) [°C]":                        "TEMP_SPINNER",
    "WT1 - Temperature 2 - front rotor bearing (FRONT BEAR) [°C]":         "TEMP_FRONT_BEAR",
    "WT1 - Temperature 3 - rear rotor bearing (REAR BEAR) [°C]":           "TEMP_REAR_BEAR",
    # ── Pitch motor temperatures ────────────────────────────────────────────
    "WT1 - Temperature 4 - motor of blade A (PITCH MOTOR TEMP A) [°C]":    "TEMP_PITCH_MOTOR_A",
    "WT1 - Temperature 5 - motor of blade B (PITCH MOTOR TEMP B) [°C]":    "TEMP_PITCH_MOTOR_B",
    "WT1 - Temperature 6 - motor of blade C (PITCH MOTOR TEMP C) [°C]":    "TEMP_PITCH_MOTOR_C",
    # ── Heat sink temperatures ──────────────────────────────────────────────
    "WT1 - Temperature 7 - heat sink of blade A (HEAT SINK TEMP A) [°C]":  "TEMP_HEAT_SINK_A",
    "WT1 - Temperature 8 - heat sink of blade B (HEAT SINK TEMP B) [°C]":  "TEMP_HEAT_SINK_B",
    "WT1 - Temperature 9 - heat sink of blade C (HEAT SINK TEMP C) [°C]":  "TEMP_HEAT_SINK_C",
    # ── Pitch cabinet temperatures ──────────────────────────────────────────
    "WT1 - Temperature 10 - control cabinet of blade A (PITCH CAB TEMP A) [°C]": "TEMP_PITCH_CAB_A",
    "WT1 - Temperature 11 - control cabinet of blade B (PITCH CAB TEMP B) [°C]": "TEMP_PITCH_CAB_B",
    "WT1 - Temperature 12 - control cabinet of blade C (PITCH CAB TEMP C) [°C]": "TEMP_PITCH_CAB_C",
    # ── Blade temperatures ──────────────────────────────────────────────────
    "WT1 - Temperature 13 - blade A (BLADE_A) [°C]":                       "TEMP_BLADE_A",
    "WT1 - Temperature 14 - blade B (BLADE_B) [°C]":                       "TEMP_BLADE_B",
    "WT1 - Temperature 15 - blade C (BLADE_C) [°C]":                       "TEMP_BLADE_C",
    # ── Rotor / stator temperatures ─────────────────────────────────────────
    "WT1 - Temperature 16 - rotor 1 (ROTOR TEMP 1) [°C]":                  "TEMP_ROTOR_1",
    "WT1 - Temperature 17 - rotor 2 (ROTOR TEMP 2) [°C]":                  "TEMP_ROTOR_2",
    "WT1 - Temperature 18 - stator 1 (STATOR TEMP 1) [°C]":                "TEMP_STATOR_1",
    "WT1 - Temperature 19 - stator 2 (STATOR TEMP 2) [°C]":                "TEMP_STATOR_2",
    # ── Nacelle temperatures ────────────────────────────────────────────────
    "WT1 - Temperature 20 - (Nacelle ambient temp.) [°C]":                  "TEMP_NACELLE_AMBIENT",
    "WT1 - Temperature 21 - (Nacelle temp.) [°C]":                          "TEMP_NACELLE",
    "WT1 - Temperature 22 - (Nacelle cabinet temp.) [°C]":                  "TEMP_NACELLE_CAB",
    # ── Ambient / tower / cabinet / transformer temperatures ────────────────
    "WT1 - Temperature 23 - (Ambient temp.) [°C]":                          "TEMP_AMBIENT",
    "EW1 - Temperature 24 - (Tower temp.) [°C]":                            "TEMP_TOWER",
    "EW1 - Temperature 25 - (Control cabinet temp.) [°C]":                  "TEMP_CTRL_CAB",
    "EW1 - Temperature 26 - (Transformer temp.) [°C]":                      "TEMP_TRANSFORMER",
    # ── Rotor ───────────────────────────────────────────────────────────────
    "WT1 - Rotor speed [rpm]":                                              "ROTOR_SPEED",
    # ── Power ───────────────────────────────────────────────────────────────
    "WT1 - Momentary production [kW]":                                      "POWER_ACTIVE",
    "WT1 - Actual reactive power Q [kVar]":                                  "POWER_REACTIVE",
    "WT1.DCE - Energy produced - this month [kWh]":                         "ENERGY_MONTH",
    # ── Wind ────────────────────────────────────────────────────────────────
    "WT1 - Momentary wind speed [m/s]":                                      "WIND_SPEED",
    "WT1 - Wind direction deviation [°]":                                    "WIND_DIR_DEVIATION",
    "WT1 - Nacelle direction (without correction) [°]":                      "NACELLE_DIR",
    # ── Grid ────────────────────────────────────────────────────────────────
    "WT1 - AC grid frequency [Hz]":                                          "GRID_FREQ",
}


# Vessel / Boat data
VESSEL_SCHEMAS = {

    # ──────────────────────────────────────────────────────────────────────
    # METADATA BLOCK — prepended to every table
    # Source: filename parsing
    # Note: vessel.json files have no ip_index or motor_id → NULL
    # ──────────────────────────────────────────────────────────────────────
    "_metadata": [
        "boat_name",       # "Helios"          — from filename
        "side",            # "DLB" | "DLT"     — from filename
        "ip_index",        # 3 | 4             — from filename (NULL for vessel tables)
        "motor_id",        # 33|49|65|81       — from filename (NULL for vessel tables)
        # "snapshot_index",  # 0 | 1 | 2         — order within file
    ],

    # ──────────────────────────────────────────────────────────────────────
    # TABLE 1 — position_logs
    # Source: vessel.json
    # ──────────────────────────────────────────────────────────────────────
    "position_logs": [
        # ...metadata...
        "hmiYear",
        "hmiMonth",
        "hmiDay",
        "hmiHour",
        "hmiMinute",
        "hmiSecond",
        "currentPositionLatitude",
        "currentPositionLongitude",
        "currentPositionToggle",
        "currentHeading",
        "headingDestination",
        "headingHome",
        "speedOverGround",
        "speedOverGroundFixed",
        "speedThroughWater",
        "sogValid",
        "trip",
        "distanceHome",
        "distanceDestination",
        "socDestination",
        "socHome",
        "timeDestHour",
        "timeDestMinute",
        "timeHomeHour",
        "timeHomeMinute",
    ],

    # ──────────────────────────────────────────────────────────────────────
    # TABLE 2 — vessel_power_logs
    # Source: vessel.json
    # ──────────────────────────────────────────────────────────────────────
    "vessel_power_logs": [
        # ...metadata...
        "hmiYear",
        "hmiMonth",
        "hmiDay",
        "hmiHour",
        "hmiMinute",
        "hmiSecond",
        # HV battery (aggregated across all packs)
        "batteryStateOfChargePercent",
        "hvBatteryCapacity",
        "hvBatteryType",
        "currentBatteryPower",
        "maxBatteryPower",
        "timeToFullMinute",
        "timeBattery",
        # LV / starter battery
        "starterBatteryVoltage",
        "starterBatteryVoltagePercent",
        "lvBatteryCapacity",
        "lvBatteryMaxCapacity",
        "lvBatteryStateOfChargePercent",
        "lvBatteryType",
        "lvBatteryVoltage",
        "lvBatteryVoltagePercent",
        # Power flows
        "powerBalance",
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
        # AC chargers (vessel-level view)
        "acChargerPowerPercent",
        "portAcChargerPower",
        "portAcChargerEnable",
        "stbdAcChargerPower",
        "stbdAcChargerEnable",
        # DC-AC / DC-DC
        "dcacPower",
        "dcacPowerConfirmed",
        "dcacPowerPercent",
        "dcacEnable",
        "dcdcPower",
        "dcdcPowerConfirmed",
        "dcdcPowerPercent",
        "dcdcEnable",
        # Regen / solar
        "regenerationPower",
        "regenerationPowerPercent",
        "regenerationEnable",
        "solarPower",
        "solarPower_hv",
        # PTO / eLPTX
        "elPtxPower",
        "elPtxPowerConfirmed",
        "elPtxPowerConfirmedPercent",
        "elPtxPowerPercent",
        "ptoPower",
        "ptoPowerConfirmed",
        "ptoPowerPercent",
        # Genset
        "portGenSetPower",
        "portGenSetPowerPercent",
        "portGenSetFuelConsumption",
        "stbdGenSetPower",
        "stbdGenSetPowerPercent",
        "stbdGenSetFuelConsumption",
        "runTimeGenset",
    ],

    # ──────────────────────────────────────────────────────────────────────
    # TABLE 3 — vessel_state_logs
    # Source: vessel.json
    # ──────────────────────────────────────────────────────────────────────
    "vessel_state_logs": [
        # ...metadata...
        "hmiYear",
        "hmiMonth",
        "hmiDay",
        "hmiHour",
        "hmiMinute",
        "hmiSecond",
        "systemState",
        "vesselState",
        "selectSystemMode",
        "gCommand",
        "gCommandState",
        "portDriveState",
        "stbdDriveState",
        "portBatteryConnectionState",
        "stbdBatteryConnectionState",
        "portThrottleGearState",
        "stbdThrottleGearState",
        "recoveryState",
        "serverCpuLoad",
        "serverMemoryUsage",
        "serverSoftwareVersion",
        "serverCompilationTime",
        "updateRateMs",
        "scuConnectionState",
        "boxLinkEnable",
        "nightModeActive",
        "displayEnable",
    ],

    # ──────────────────────────────────────────────────────────────────────
    # TABLE 4 — battery_pack_logs
    # Source: BMWix .json  (system / gateway view)
    # ──────────────────────────────────────────────────────────────────────
    "battery_pack_logs": [
        # ...metadata...
        # SOC / SOH
        "gStateOfCharge",
        "gStateOfHealth",
        "gEnergyRemaining",
        "gParamMaxCapacity",
        "gParamMaxChargeVoltage",
        # Electrical
        "gPackVoltage",
        "gBusVoltage",
        "gCurrent",
        "gCellBalance",
        # Power limits
        "gPowerLimitCharge",
        "gPowerLimitDischarge",
        # Thermal
        "gAverageTemperature",
        "gMaxCellTemperature",
        "gMinCellTemperature",
        "gCoolingPolicy",
        # Time
        "gTimeToFullMinute",
        # State / control
        "gState",
        "gCommand",
        "gError",
        "gDisableReason",
        "gBalancingState",
        "batteryErrorCode",
        "batteryErrorListEraseState",
    ],

    # ──────────────────────────────────────────────────────────────────────
    # TABLE 5 — battery_pack_device_logs
    # Source: BMWix _DEVICE.json  (raw BMS view)
    # ──────────────────────────────────────────────────────────────────────
    "battery_pack_device_logs": [
        # ...metadata...
        # SOC
        "actualSoc",
        "actualUserSoc",
        "actualSocDelta",
        "maxSocAllowed_StateOfHealth",
        "minSocAllowed",
        # Electrical
        "actualPackVoltage",
        "actualBusVoltage",
        "actualCurrent",
        "maxCapacity",
        "maxVoltageCharge",
        "minVoltageDischarge",
        "maxCurrentCharge",
        "maxCurrentDischarge",
        "maxCellVoltage",
        "minCellVoltage",
        "cellBalance",
        # Power limits (raw BMS values — different precision from gateway view)
        "availablePowerChargeLong",
        "availablePowerChargeShort",
        "availablePowerDischargeLong",
        "availablePowerDischargeShort",
        # Thermal
        "actualTempBattery",
        "actualTempBatteryMax",
        "actualTempBatteryMin",
        "actualTempHeatexchanger",
        # Cooling (EKMV compressor)
        "coolingRequested",
        "coolingRequestedPower",
        "coolingType",
        "coolingWorking",
        "coolingValveState",
        "coolingValveRequest",
        "coolingValveErrorState",
        "ekmvOperationState",
        "ekmvTemp",
        "ekmvTempIn",
        "ekmvTempOut",
        "ekmvPresHigh",
        "ekmvPresLow",
        "ekmvRpmPercent",
        "ekmvEpower",
        "ekmvErrorState",
        # Contactor / safety
        "stateContactor",
        "stateDischargeBus",
        "stateErrorContactor",
        "stateErrorExternalIsolation",
        "stateErrorInternalIsolation",
        "stateWarnIsolation",
        "statusWarnOverTemp",
        "isoMeasurementActive",
        # Requests
        "requestAbortCharging",
        "requestContactorClose",
        "requestInterruptCharging",
        "requestOpenContactorFast",
        "requestOpenContactorNow",
        # Time
        "timeToFullMinute",
        "predictedChargeTimeMinute",
        # Device identity
        "batteryType",
        "deviceState",
        "deviceEnableSetting",
        "deviceIdentification",
        "error",
    ],

    # ──────────────────────────────────────────────────────────────────────
    # TABLE 6 — charger_logs
    # Source: BCL25 .json  (system / gateway view)
    # ──────────────────────────────────────────────────────────────────────
    "charger_logs": [
        # ...metadata...
        # AC side
        "gActAcCurrent",
        "gActAcVoltage",
        "gActAcFrequency",
        "gCommandAcCurrentLimitPP",
        "gParamMaxAcCurrentPP",
        # DC side
        "gActDcPower",
        "gActDcVoltage",
        "gCommandDcPowerLimit",
        "gCommandMaxDcVoltage",
        "gMaxDcPower",
        # Thermal
        "gActElectronicTemperature",
        "gCoolingPolicy",
        # State / control
        "gState",
        "gCommand",
        "gError",
        "gDisableReason",
        "gIsSlave",
        "gWake",
        "gSimConnectedPhaseCount",
    ],

    # ──────────────────────────────────────────────────────────────────────
    # TABLE 7 — charger_device_logs
    # Source: BCL25 _DEVICE.json  (raw charger hardware view)
    # ──────────────────────────────────────────────────────────────────────
    "charger_device_logs": [
        # ...metadata...
        # AC side (raw 3-phase)
        "currentL1",
        "currentL2",
        "currentL3",
        "voltageL1",
        "voltageL2",
        "voltageL3",
        "inputFrequency",
        "acCurrentLim",
        # DC / battery side
        "batteryCurrent",
        "batteryCurrentLim",
        "batteryVoltage",
        "batteryVoltageLim",
        "chgIbatMaxAvail",
        # Thermal
        "invTempAmb",
        "bbTempAmb",
        "externalTemp",
        "signalTempAmb",
        "signalTempChassis",
        # Inverter / buck-boost state
        "inverterState",
        "inverterShutDownReason",
        "buckBoostState",
        "buckBoostShutDownReason",
        "shutDownReason",
        "powerStage",
        # Signal / command
        "signalState",
        "signalConnection",
        "cmdEnable",
        "cmdMode",
        "mode",
        # EVSE (charge plug interface)
        "evseStatus",
        "evseType",
        "evseTypeStatus",
        "contrPilotImp",
        "proximityState",
        "lockState",
        "pilotDuty",
        "pilotFreq",
        # LV battery
        "lV_Vbat",
        "lvBattUVlim",
        # Device identity
        "deviceMode",
        "deviceEnableSetting",
        "deviceSeen",
        "deviceCantStart",
        "error",
        "errorStatus",
        "BBuCVersion",
        "INVuCVersion",
        "signaluCVersion",
        "hwRev",
    ],
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
