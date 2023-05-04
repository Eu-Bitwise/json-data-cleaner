import argparse
import json
import ast
import codecs
from tqdm import tqdm
from termcolor import colored
import warnings
import logging

# Configure logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, filemode='w')

# Function to load JSON file and parse the contents
def load_json_file(file_path):
    print(colored("Step 1/2: parsing JSON file...", 'yellow'))
    
    with open(file_path, 'r', encoding='utf-8') as json_file:
        file_contents = json_file.read()

    debug_counters = {"source_rows": 0, "errors": 0, "resulting_rows": 0}
    
    file_contents = file_contents.strip().split('\n')
    progress_bar = tqdm(total=len(file_contents), desc="Processing", unit="rows")
    
    json_data = []
    # Parse each line of the file
    for item in file_contents:
        debug_counters["source_rows"] += 1
        try:
            parsed_item = ast.literal_eval(item)
            json_data.append(parsed_item)
        except Exception as e:
            error_msg = f"Error parsing line: {item}\nError: {e}"
            logging.error(error_msg)
            print(error_msg)
            debug_counters["errors"] += 1
        
        progress_bar.update(1)

    # Clean JSON data
    print(colored("Step 2/2: Cleaning data...", 'yellow'))
    cleaned_data = clean_json_data(json_data, debug_counters, progress_bar)
    debug_counters["resulting_rows"] = len(cleaned_data)

    progress_bar.close()

    return cleaned_data, debug_counters

# Function recursive to clean the JSON data
def clean_json_data(json_data, debug_counters, progress_bar):
    cleaned_data = []
    
    # filter out DeprecationWarning messages
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    for data_item in json_data:
        # Process dictionary items
        if isinstance(data_item, dict):
            cleaned_item = {}
            for key, value in data_item.items():
                # Recursively clean nested data
                cleaned_value = clean_json_data([value], debug_counters, progress_bar)
                cleaned_item[key] = cleaned_value[0] if cleaned_value else None
            cleaned_data.append(cleaned_item)        
        # Process list items
        elif isinstance(data_item, list):
            cleaned_data.extend(clean_json_data(data_item, debug_counters, progress_bar))
        # Process string items and decode Unicode escape sequences
        elif isinstance(data_item, str):
            try:
                cleaned_data.append(codecs.decode(data_item, 'unicode_escape'))
            except UnicodeDecodeError as e:
                error_msg = f"Error decoding string: {data_item}\nError: {e}"
                logging.error(error_msg)
                cleaned_data.append("n/a")
                debug_counters["errors"] += 1
            except DeprecationWarning as e:
                warning_msg = f"Deprecation warning: {data_item}\nWarning: {e}"
                logging.warning(warning_msg)
                cleaned_data.append("n/a")
                debug_counters["errors"] += 1

        # Process other data types
        else:
            cleaned_data.append(data_item if data_item is not None else "n/a")
        
        progress_bar.update(1)

    return cleaned_data

# Function to write cleaned JSON data to an output file
def write_cleaned_json_data(cleaned_data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(cleaned_data, output_file, ensure_ascii=False, indent=4)

# Function to print a summary of the processing
def print_summary(debug_counters):
    print("\nSummary:")
    print(f"Total source rows: {debug_counters['source_rows']}")
    print(f"Total errors found: {debug_counters['errors']}")
    print(f"Total resulting rows: {debug_counters['resulting_rows']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some JSON data.')
    parser.add_argument('--input_file', type=str, help='File path for input JSON data')
    parser.add_argument('--output_file', type=str, help='Output file path for cleaned JSON data')

    args = parser.parse_args()

    file_path = args.input_file
    output_file_path = args.output_file
    
    print(colored("Starting JSON processing...", 'green'))
    cleaned_json_data, debug_counters = load_json_file(file_path)
    write_cleaned_json_data(cleaned_json_data, output_file_path)
    print(colored("JSON processing completed.", 'green'))
    
    print_summary(debug_counters)