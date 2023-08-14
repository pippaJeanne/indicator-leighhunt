import re

def convert_double_spaces(line):
    # Use regular expressions to find and replace double spaces with single spaces
    # Match spaces between non-linebreak characters (using negative lookahead and lookbehind)
    converted_line = re.sub(r'(?<!\n)\s{2,}(?!\n)', ' ', line)
    return converted_line

def undouble(input_file, output_file):
    # Read the input file line by line
    with open(input_file, 'r') as input_file:
        with open(output_file, 'w') as output_file:
            for line in input_file:
                # Convert double spaces to single spaces for each line
                converted_line = convert_double_spaces(line)
                # Write the converted line to the output file, preserving line breaks
                output_file.write(converted_line)
                # Add a newline character to preserve line breaks
                #output_file.write('\n')

# Example usage
input_file = 'raw_double.txt'
output_file = 'un_double.txt'
undouble(input_file, output_file)
print("Conversion complete.")
