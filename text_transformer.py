import logging
import sys

# Configure logging
logging.basicConfig(filename='text_transformer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to transform the input text
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

# Get input from command line
if len(sys.argv) < 2:
    print("Please provide a string with at least 3 words as an argument.")
else:
    input_text = ' '.join(sys.argv[1:])
    transformed_text = transform_text(input_text)
    print(transformed_text)
