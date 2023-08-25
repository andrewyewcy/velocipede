# Referenced from Eigen Foo
# https://gist.github.com/eigenfoo/ab6e3302aab97479738202e26980969e

# Import required packages
import argparse # The argparse module makes it easy to write user-friendly command-line interface.
import re
import json
import string

# Add a description for the function in command line
parser = argparse.ArgumentParser(
    description="Print a Markdown table of contents for a Jupyter notebook."
)

# Add argument for function in command line
parser.add_argument(
    "notebook", type=str, help="Notebook for which to create table of contents."
)

# Convert argument strings to objects and assign them as attributes of the namespace. Return the populated namespace
args = parser.parse_args()

# Define the function
if __name__ == "__main__":

    # Initiate a blank list for table of contents
    toc = []

    # Open the provided jupyter notebook, then extract cells into a list
    with open(args.notebook, "r") as f:
        cells = json.load(f)["cells"]

    # Iterate through each cell
    for cell in cells:

        # Identify if cell is markdown
        if cell["cell_type"] == "markdown":
            
            # Iterate through each line in markdown cell
            for line in cell["source"]:

                # Identify if there are any header lines
                match = re.search("^#+ \w+", line)

                # If a header line is identified, create a table of contents markdown printout
                if match:

                    # Define Level of header
                    level = len(line) - len(line.lstrip("#"))
                    
                    # Define Link to header
                    link = line.strip(" #\n").replace(" ", "-")

                    # Add header link markdown to table of contents
                    toc.append(
                        2 * (level - 1) * " "
                        + "- ["
                        + line.strip(" #\n")
                        + "](#"
                        + link
                        + ")"
                    )

    # Finally, after constructing a full table of contents, print out each line in command line for copy and pasting.
    for item in toc:
        print(item)