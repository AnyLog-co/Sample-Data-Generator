import csv
import json

DATA = "WEA_10_Minuten.csv"

with open(DATA, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')

    index = None
    content = []

    for row in reader:
        row_clean = {k: (v.strip() if v else "") for k, v in row.items()}  # trim spaces

        if index is None:
            index = row_clean.get("Anlage")

        elif index != row_clean.get("Anlage"):
            # Save previous turbine data as JSON Lines
            with open(f"wind_turbine_{index}.json", 'w', encoding='utf-8-sig') as jf:
                for line in content:
                    json.dump(line, jf, ensure_ascii=False)
                    jf.write("\n")  # important: newline after each JSON object

            # Reset for new turbine
            index = row_clean.get("Anlage")
            content = []

        content.append(row_clean)

    # Save the last turbine
    if content:
        with open(f"wind_turbine_{index}.jsonl", 'w', encoding='utf-8-sig') as jf:
            for line in content:
                json.dump(line, jf, ensure_ascii=False)
                jf.write("\n")
