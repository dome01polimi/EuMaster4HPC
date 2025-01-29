# Install packages if missing
import pkg_resources, subprocess, sys
required  = {'pandas','pathlib'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed
if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
# End installing missing packages

import os
import csv
import glob
import re
import pandas as pd
import argparse

from pathlib import Path

def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def process_reframe_logs(log_dir, output_file):
    print("Starting to process ReFrame log files...")
    
    results = []
    log_files = glob.glob(f"{log_dir}/reframe_*.log")
    
    for log_file in log_files:
        print(f"Processing file: {log_file}")
        with open(log_file) as f:
            for line in f:
                # Clean ANSI codes from the line
                clean_line = clean_ansi_codes(line)
                
                if 'info: reframe: [  PASSED  ] Ran' in clean_line or 'info: reframe: [  FAILED  ] Ran' in clean_line:
                    
                    # Extract timestamp
                    timestamp = clean_line[1:20]
                    
                    # Extract test numbers using regular expressions
                    tests_match = re.search(r'Ran (\d+)/(\d+) test case\(s\) from (\d+) check\(s\) \((\d+) failure\(s\), (\d+) skipped, (\d+) aborted\)', clean_line)
                    
                    if tests_match:
                        result = {
                            'timestamp': timestamp,
                            'log_file': os.path.basename(log_file),
                            'tests_run': tests_match.group(1),
                            'total_tests': tests_match.group(2),
                            'total_checks': tests_match.group(3),
                            'failures': tests_match.group(4),
                            'skipped': tests_match.group(5),
                            'aborted': tests_match.group(6),
                            'status': 'PASSED' if 'PASSED' in clean_line else 'FAILED'
                        }
                        results.append(result)
    
    print(f"Found {len(results)} test results")
    
    if results:
        fieldnames = ['timestamp', 'log_file', 'status', 'tests_run', 'total_tests', 
                     'total_checks', 'failures', 'skipped', 'aborted']
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
            print(f"Results written to: {output_file}")
            print(f"CSV columns: {', '.join(fieldnames)}\n\n")

def process_perlogs(perflog_dir):
    def parse_info(info):
        if pd.isna(info) or info.strip() == "":  # Handle NaN or empty strings
        	return {}
	# Regular expression to extract key-value pairs %<key>:<value>
        matches = re.findall(r"%([^:]+):([^%]+)", info)
        return dict(matches)

    # Iterate over all .log files in the directory
    for file_name in os.listdir(perflog_dir):
        if file_name.endswith(".log"):
            file_path = os.path.join(perflog_dir, file_name)
            print(f"Processing file: {file_path}")

            # Read the log file as a CSV
            df = pd.read_csv(file_path)

            # Process the `info` column if it exists
            if "info" in df.columns:
                print(f"Found 'info' column in {file_name}. Parsing it...")
                info_columns = df["info"].fillna("").apply(parse_info).apply(pd.Series)
                df = pd.concat([df.drop(columns=["info"]), info_columns], axis=1)

            # Remove columns with "dummy" in their names (case-insensitive)
            dummy_columns = df.columns[df.columns.str.contains("dummy", case=False)]
            if not dummy_columns.empty:
                print(f"Removing columns with 'dummy' in their names: {list(dummy_columns)}")
                df = df.loc[:, ~df.columns.str.contains("dummy", case=False)]
            else:
                print(f"No 'dummy' columns found in {file_name}.")

            # Overwrite the original file with the updated DataFrame
            df.to_csv(file_path, index=False)
            print(f"Updated file saved: {file_path}")

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process ReFrame log files and generate a CSV report. Fix columns in performance logs to produce a cleaner table file.")
    parser.add_argument('--log-dir', default='.', 
                        help="Directory where to search for the ReFrame log files. Default is current directory.")
    parser.add_argument('--output-file', default='./reframe_out/processed_logs/test_results.csv', 
                        help="Path to the output CSV file. Default is './reframe_out/processed_logs/test_results.csv'.")
    parser.add_argument('--perflog-dir', default='./reframe_out/perflogs',
                        help="Directory containing the performance logs stored by ReFrame.")
    args = parser.parse_args()

    file = Path(args.output_file)
    file.parent.mkdir(parents=True, exist_ok=True)
    
    process_reframe_logs(os.path.expanduser(args.log_dir), os.path.expanduser(args.output_file))

    process_perlogs(os.path.expanduser(args.perflog_dir))
