import csv

src_csv_path = 'Test/Out/csv_test.csv'
dest_csv_path = 'Questions/par2.csv'

with open(src_csv_path, 'r', encoding='utf-8') as src_file:
    reader = csv.reader(src_file)
    next(reader, None)  # Skip the header row in the source CSV

    with open(dest_csv_path, 'a', newline='', encoding='utf-8') as dest_file:
        writer = csv.writer(dest_file)

        for row in reader:
            writer.writerow(row)

print('Succesfully executed') 