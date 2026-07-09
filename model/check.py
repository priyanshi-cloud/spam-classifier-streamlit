import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), 'spam.csv')

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)
    print(f'Total lines: {len(lines)}')
    field_counts = [len(row) for row in lines]
    unique_counts = set(field_counts)
    print(f'Unique field counts: {unique_counts}')
    if len(unique_counts) == 1:
        print('All lines have the same number of fields.')
    else:
        print('Inconsistent field counts:')
        for i, count in enumerate(field_counts):
            if count != field_counts[0]:
                print(f'Line {i+1}: {count} fields')