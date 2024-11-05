"""
@batch_print_pdf.py
@brief A utility program for printing or merging PDF files using Ghostscript.

This script provides functionality to either print or merge PDF files found in a specified directory.
It utilizes Ghostscript to handle both printing and merging, with fallbacks to subprocess calls if 
the Ghostscript Python library is not available.

## Usage

The program supports the following command-line arguments:
  - `-d`, `--directory`: Specifies the directory containing PDF files to process.
  - `-p`, `--printer`: (Optional) Specifies the printer name to send PDF files to.
  - `-m`, `--merge`: (Optional) Specifies an output filename to merge all PDFs into a single document.
  
If both `--printer` and `--merge` options are provided, the program will prioritize merging.

## Dependencies

- Ghostscript Python library (optional but recommended for performance)
- Ghostscript executable (required for subprocess fallback)

@note This program requires Ghostscript to be installed on the system to function correctly.

@license MIT License
"""

from utilities.log_util import *
from utilities.printing import *
import os
import argparse
import sys

def main():
    # Set up argument parser with enhanced error handling and custom help message
    parser = argparse.ArgumentParser(
        description="A utility for printing or merging PDF files using Ghostscript.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage="%(prog)s -d DIRECTORY [-p PRINTER] [-m MERGE]",
        epilog="If both printing and merging options are provided, the program will prioritize merging."
    )

    parser.add_argument(
        "-d", "--directory", type=str, required=True,
        help="Path to the directory containing PDF files to process."
    )
    parser.add_argument(
        "-p", "--printer", type=str, default=None,
        help="Name of the printer to send PDF files to (optional)."
    )
    parser.add_argument(
        "-m", "--merge", type=str,
        help="Output filename for merging all PDFs into a single document."
    )

    # Show help message if arguments are missing or invalid
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Parse arguments
    args = parser.parse_args()

    # Verify directory
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.")
        return

    # Find all PDF files in the directory
    pdf_files = [os.path.join(args.directory, f) for f in os.listdir(args.directory) if f.lower().endswith(".pdf")]

    # Check if there are any PDF files
    if not pdf_files:
        print("No PDF files found in the specified directory.")
        return

    # If --merge is provided, merge PDFs
    if args.merge:
        merge_pdfs_with_ghostscript(pdf_files, args.merge)
    else:
        # Print each PDF file individually
        for pdf_file in pdf_files:
            print_pdf_with_ghostscript(pdf_file, args.printer)

if __name__ == "__main__":
    main()
