import re

def convert_double_spaces(line):
    # Use regular expressions to find and replace double spaces with single spaces
    converted_line = re.sub(r'\s{2,}', ' ', line)
    return converted_line

def convert_file_double_spaces(input_file, output_file):
    # Read the input file line by line
    with open(input_file, 'r') as input_file:
        with open(output_file, 'w') as output_file:
            for line in input_file:
                # Convert double spaces to single spaces for each line
                converted_line = convert_double_spaces(line)
                # Write the converted line to the output file
                output_file.write(converted_line)

# Example usage
input_file = 'raw_double.txt'
output_file = 'un_double.txt'
convert_file_double_spaces(input_file, output_file)
print("Conversion complete.")
