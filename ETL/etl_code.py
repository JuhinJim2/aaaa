import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

os.chdir(r'C:\Users\audre\OneDrive\Desktop\IBM Python Project\ETL')

log_file = "log_file.txt"
target_file = "transformed_data.csv"

def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe

def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(columns=["name", "height", "weight"])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)
        dataframe = pd.concat([dataframe, pd.DataFrame([{"name":name, "height":height, "weight":weight}])], ignore_index=True)
    return dataframe

def extract():
    extracted_data = pd.DataFrame(columns=['name', 'height', 'weight'])  


    # process all csv files
    csv_files = glob.glob("**/*.csv", recursive=True)
    print(f"CSV files found: {csv_files}")
    for csvfile in csv_files:
        print(f"Processing CSV file: {csvfile}")
        extracted_data = pd.concat([extracted_data, extract_from_csv(csvfile)], ignore_index=True)
        
    # process all json files
    json_files = glob.glob("**/*.json", recursive=True)
    print(f"JSON files found: {json_files}")
    for jsonfile in json_files:
        print(f"Processing JSON file: {jsonfile}")
        extracted_data = pd.concat([extracted_data, extract_from_json(jsonfile)], ignore_index=True)
    
    # process all xml files
    xml_files = glob.glob("**/*.xml", recursive=True)
    print(f"XML files found: {xml_files}")
    for xmlfile in xml_files:
        print(f"Processing XML file: {xmlfile}")
        extracted_data = pd.concat([extracted_data, extract_from_xml(xmlfile)], ignore_index=True)
        
    return extracted_data

def transform(data):
    # Convert inches to meters and round off to two decimals
    # 1 inch is 0.0254 meters
    data['height'] = round(data['height'] * 0.0254, 2)
    
    # Convert pounds to kilograms and round off to two decimals
    # 1 pound is 0.45359237 kilograms
    data['weight'] = round(data['weight'] * 0.45359237, 2)
    
    return data

def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file, index=False)

def log_progress(message):
    timestamp_format = '%Y-%b-%d-%H:%M:%S'  # Corrected Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now()  # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(timestamp + ',' + message + '\n')

# Log the initialization of the ETL process
log_progress("ETL Job Started")

# Log the beginning of the Extraction process
log_progress("Extract phase Started")
extracted_data = extract()

# Log the completion of the Extraction process
log_progress("Extract phase Ended")

# Log the beginning of the Transformation process
log_progress("Transform phase Started")
transformed_data = transform(extracted_data)
print("Transformed Data")
print(transformed_data)

# Log the completion of the Transformation process
log_progress("Transform phase Ended")

# Log the beginning of the Loading process
log_progress("Load phase Started")
load_data(target_file, transformed_data)

# Log the completion of the Loading process
log_progress("Load phase Ended")

# Log the completion of the ETL process
log_progress("ETL Job Ended")
