# JSON Data Cleaner

## Description
Python script designed to parse and clean JSON data by handling invalid strings and decoding errors for small or big files. It reads JSON data from an input file, cleans it by decoding Unicode escape sequences, and writes the cleaned data to an output file that can be used by your database.

## Features
- Parse JSON data from an input file
- Clean JSON data and replace invalid values with 'n/a'
- Write cleaned JSON data to an output file
- Display progress bar with progress updates
- Log errors and warnings to a log file
- Print summary of the processing

## Install
- Requires python 3.6 or higher
- To install the required packages, run: `pip install tqdm termcolor`

## Usage
Run the following command: `python json_cleaner.py --input_file <path_to_input_file> --output_file <path_to_output_file>`

Replace <path_to_input_file> with the path to your input JSON file, and <path_to_output_file> with the desired output file path for the cleaned JSON data.

For example: `python json_cleaner.py --input_file input.json --output_file cleaned_output.json`
