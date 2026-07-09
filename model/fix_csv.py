import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), 'spam.csv')

# Read the file
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)

# Standardize to 2 fields: label, message
standardized = []
for row in lines:
    if len(row) >= 2:
        label = row[0].strip()
        message = row[1].strip()
        standardized.append([label, message])
    else:
        # If only 1 field, assume it's message with label missing? But probably not.
        print(f"Skipping invalid row: {row}")

# Write back
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(standardized)

print("CSV standardized to 2 fields.")