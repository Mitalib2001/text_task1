import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import logging
import sys
import os

# Configure logging
logging.basicConfig(filename='pipeline_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_xml(xml_file):
    try:
        # Parse XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        data = []

        # Iterate over all ECUC-CONTAINER-VALUE elements
        for container in root.findall('.//{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE'):
            # Extract SHORT-NAME and DEFINITION-REF
            short_name = container.find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
            definition_ref = container.find('.//{http://autosar.org/schema/r4.0}DEFINITION-REF').text
            data.append({'Short Name': short_name, 'Definition Ref': definition_ref})

            # Iterate over all ECUC-CONTAINER-VALUE elements within each container
            for sub_container in container.findall('.//{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE'):
                # Extract SHORT-NAME and DEFINITION-REF for sub-containers
                sub_short_name = sub_container.find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
                sub_definition_ref = sub_container.find('.//{http://autosar.org/schema/r4.0}DEFINITION-REF').text
                data.append({'Short Name': sub_short_name, 'Definition Ref': sub_definition_ref})

        return data
    except Exception as e:
        # Handle exceptions during XML parsing
        error_msg = f"Error parsing XML file: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        return []

def generate_excel(data, output_path):
    try:
        if not data:
            # Warn if there's no data to create Excel file
            error_msg = "No data to create Excel file."
            logging.warning(error_msg)
            print(error_msg)
            return

        # Create DataFrame from the extracted data and save to Excel file
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        success_msg = f"Excel file created successfully: {output_path}"
        logging.info(success_msg)
        print(success_msg)
    except Exception as e:
        # Handle exceptions during Excel file generation
        error_msg = f"Error creating Excel file: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

def transform_text(user_input):
    try:
        user_input = user_input.strip()  # Remove leading and trailing whitespaces
        # Check if input has at least 3 words
        if len(user_input.split()) < 3:
            logging.warning("Less than 3 words inputted.")
            return "Please input a minimum of 3 words."

        transformed_text = ""
        capitalize_next = True
        # Iterate through each character in the input text
        for char in user_input:
            # Check if the character is alphabetic
            if char.isalpha():
                # Apply alternating capitalization
                if capitalize_next:
                    transformed_text += char.upper()
                else:
                    transformed_text += char.lower()
                capitalize_next = not capitalize_next
            else:
                transformed_text += char

        logging.info("Text transformed successfully.")
        return transformed_text
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return "An error occurred during transformation."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pipeline to parse XML, generate Excel, and transform text.')
    parser.add_argument('--str_input', help='Input text for transformation')
    parser.add_argument('--file_input', help='Input XML file path')
    parser.add_argument('--output', help='Output Excel file path')
    args = parser.parse_args()

    # Check if XML file exists
    if args.file_input and not os.path.exists(args.file_input):
        logging.error("XML file not found.")
        print("XML file not found.")
        sys.exit(1)

    # Check if output directory exists, if not, create it
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse XML file
    data = parse_xml(args.file_input)
    # Generate Excel file
    generate_excel(data, args.output)
    # Transform text
    transformed_text = transform_text(args.str_input)
    print("Transformed text:")
    print(transformed_text)
