import numpy as np
import matplotlib.pyplot as plt
import random

import os
import re

def combine_rtf_files(input_folder, output_file):
    """
    Combines all .text.rtf and .rtf files from a specified folder into a single RTF file.

    Args:
        input_folder (str): The path to the folder containing the RTF files.
        output_file (str): The name of the output RTF file.
    """
    
    # Initialize the combined content with the RTF header
    combined_content = b'{\\rtf1\\ansi\\deff0'
    
    try:
        # Get a list of all files in the input folder
        files = os.listdir(input_folder)
        
        # Filter for .rtf and .text.rtf files
        rtf_files = [f for f in files if f.endswith('.rtf') or f.endswith('.text.rtf')]

        # Check if there are any RTF files to combine
        if not rtf_files:
            print(f"No .rtf or .text.rtf files found in '{input_folder}'.")
            return

        # Regular expression to remove the RTF header and footer
        rtf_header_footer_pattern = re.compile(br'\{\\rtf1\\ansi\\deff0|\\par\s*\}')

        for filename in rtf_files:
            file_path = os.path.join(input_folder, filename)
            
            with open(file_path, 'rb') as f:
                content = f.read()

            # Remove the RTF header and footer from the file's content
            # This ensures we don't have multiple headers/footers
            stripped_content = rtf_header_footer_pattern.sub(b'', content)
            
            # Add the stripped content and a separator line
            # \par is a paragraph break, \pard\sa200\sl276\slmult1\line is a line break
            # {\b\fs24\par\pard\sa200\sl276\slmult1\line\b0\fs20\par} is a bold line break with bigger font 
            separator = b'{\\par\\pard\\sa200\\sl276\\slmult1\\line}'
            combined_content += stripped_content + separator

    except FileNotFoundError:
        print(f"Error: The folder '{input_folder}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Add the final RTF footer
    combined_content += b'}'

    # Write the combined content to the output file
    with open(output_file, 'wb') as f:
        f.write(combined_content)
    
    print(f"Successfully combined {len(rtf_files)} files into '{output_file}'.")




if __name__ == '__main__':
        # --- Usage ---
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the input and output paths
    input_directory = os.path.join(script_dir, 'text_txt')
    output_file_name = os.path.join(script_dir, 'combined_notes.rtf')

    # Run the function
    combine_rtf_files(input_directory, output_file_name)