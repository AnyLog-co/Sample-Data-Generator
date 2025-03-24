import random
from data_generator.support import create_timestamp

def r_50(db_name:str):
    # Generate the initial values
    SealStage = round(random.uniform(0.0, 100.0), 2)
    FillerStage = round(random.uniform(0.0, 100.0), 2)
    RunHours = round(random.uniform(0.0, 200.0), 2)
    MachineState = random.randint(0, 5)
    CapPickInCyc = random.choice([True, False])
    CapPressInCyc = random.choice([True, False])

    # Introducing dependencies
    if SealStage > 80:
        SealCycTime = round(random.uniform(3.0, 5.0), 2)  # Longer cycle time when SealStage is high
    else:
        SealCycTime = round(random.uniform(0.5, 3.0), 2)

    if RunHours > 100:
        BatchCount = random.randint(5000, 10000)  # Higher batch count if run hours are more
    else:
        BatchCount = random.randint(0, 5000)

    # CapPressInCyc should be True if CapPickInCyc is True
    if CapPickInCyc:
        CapPressInCyc = True

    return {
        "dbms": db_name,
        "table": "r_50",
        "ts": [create_timestamp()],
        "SealStage": [SealStage],
        "Cyc/Min": [round(random.uniform(20.0, 60.0), 2)],
        "BatchCount": [BatchCount],
        "RunHours": [RunHours],
        "MachineState": [MachineState],
        "DenesterInCycle": [random.choice([True, False])],
        "FillerStage": [FillerStage],
        "FillerCycTime": [round(random.uniform(0.5, 5.0), 2)],
        "SealCycTime": [SealCycTime],
        "Heater1Setpoint": [round(random.uniform(100.0, 300.0), 2)],
        "Heater1Temp": [round(random.uniform(100.0, 300.0), 2)],
        "CapPickInCyc": [CapPickInCyc],
        "CapPressInCyc": [CapPressInCyc],
        "RotaryIndexRDY": [random.choice([True, False])],
        "RotaryIndexRun": [random.choice([True, False])],
        "RotaryIndexI": [round(random.uniform(0.0, 100.0), 2)],
        "OutfeedConvRDY": [random.choice([True, False])],
        "OutfeedConvRun": [random.choice([True, False])],
        "OutfeedConvI": [round(random.uniform(0.0, 100.0), 2)],
        "FilmSupplyRDY": [random.choice([True, False])],
        "FilmSupplyRun": [random.choice([True, False])],
        "FilmSupplyI": [round(random.uniform(0.0, 100.0), 2)],
        "FilmAdvRDY": [random.choice([True, False])],
        "FilmAdvRun": [random.choice([True, False])],
        "FilmAdvI": [round(random.uniform(0.0, 100.0), 2)],
        "AirPressureOk": [random.choice([True, False])]
    }
