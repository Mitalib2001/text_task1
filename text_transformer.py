import tkinter as tk
import logging

# Configure logging
logging.basicConfig(filename='text_transformer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to transform the input text
def transform_text():
    try:
        user_input = user_entry.get().strip()  # Remove leading and trailing whitespaces
        # Check if input has at least 3 words
        if len(user_input.split()) < 3:
            result_display_label.config(text="Please input a minimum of 3 words.")
            logging.warning("Less than 3 words inputted.")
            return

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

        # Display the transformed text
        result_display_label.config(text=transformed_text)
        logging.info("Text transformed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        result_display_label.config(text="An error occurred during transformation.")

# Function to validate input in the entry widget
def validate_input(char):
    return char.isalpha() or char.isspace()  # Allow alphabetic characters and spaces

# Graphical User Interface
root = tk.Tk()
root.title("Text Transformer")

frame = tk.Frame(root, bg="black")
frame.pack(padx=20, pady=20)

# Label for instruction
instruction_label = tk.Label(frame, text="Enter a string with at least 3 words:")
instruction_label.grid(row=1, column=1, padx=20, pady=10)

# Entry widget for user input
validate_input_cmd = root.register(validate_input)  # Register the validation function
user_entry = tk.Entry(frame, width=50, validate="key", validatecommand=(validate_input_cmd, "%S"))
user_entry.grid(row=2, column=1, padx=5, pady=5)

# Button to trigger text transformation
transform_button = tk.Button(frame, text="Transform", command=transform_text, bg="green")
transform_button.grid(row=3, column=1, padx=10, pady=10)

# Label to display the transformed text
result_display_label = tk.Label(frame, text="", bg="white")
result_display_label.grid(row=4, column=0, columnspan=2, pady=15)

root.mainloop()