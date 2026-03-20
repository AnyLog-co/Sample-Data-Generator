import os
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

XLS_DIRS = [
    "Farm1_WTG1_parameters 53954 MV",
    "Farm1_WTG2_parameters 53955 MV",
    "Farm1_WTG3_parameters 53956 MV",
    "Farm1_WTG4_parameters 53957 MV",
    "Farm2_WTG1_parameters 53967 PA",
    "Farm2_WTG2_parameters 53968 PA"
]

file_columns = []

# only read ONE directory (since structure is same)

for xls_dir in XLS_DIRS:
    folder = os.path.join(DATA_PATH, xls_dir)
    per_file = {
        "farm": xls_dir.split('_')[0][-1],
        "turbine": xls_dir.split('_')[1][-1],
        "turbine_id": xls_dir.split(' ')[1],
        "columns": ["time"]
    }

    for file_name in os.listdir(folder):
        if not file_name.endswith(".xls"):
            continue

        
        full_path = os.path.join(folder, file_name)
        
        # json_file = full_path.replace("xls", "json")

        # read only header (FAST)
        df = pd.read_excel(full_path, engine="xlrd")
        df = df.astype(object).where(pd.notnull(df), None)
        for key in list(df.keys()):
            if key not in per_file["columns"]:
                per_file["columns"].append(key)
        # df.to_json(json_file, orient="records", lines=True)
    
    file_columns.append(per_file)

print(file_columns)