import argparse
import csv
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process complaints data.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-s', '--start_date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('-e', '--end_date', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('-o', '--output', help='Output CSV file')
    return parser.parse_args()

def count_complaints(input_file, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    borough_counts = {}
    
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = datetime.strptime(row['Created Date'], "%Y-%m-%d")
            if start <= date <= end:
                borough = row['Borough']
                complaint = row['Complaint Type']
                borough_counts.setdefault(complaint, {}).setdefault(borough, 0)
                borough_counts[complaint][borough] += 1
    
    return borough_counts

def save_output(borough_counts, output_file=None):
    if output_file:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Complaint Type', 'Borough', 'Count'])
            for complaint, boroughs in borough_counts.items():
                for borough, count in boroughs.items():
                    writer.writerow([complaint, borough, count])
    else:
        for complaint, boroughs in borough_counts.items():
            for borough, count in boroughs.items():
                print(f"{complaint} {borough} {count}")

if __name__ == '__main__':
    args = parse_arguments()
    borough_counts = count_complaints(args.input, args.start_date, args.end_date)
    save_output(borough_counts, args.output)
