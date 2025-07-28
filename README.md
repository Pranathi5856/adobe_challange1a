# Challenge 1a - PDF Heading Extraction

## Overview

This project extracts the document title and outline (headings) from PDF files using Python.  
It dynamically identifies heading levels (H1, H2, H3) based on font sizes without hardcoded thresholds, enabling robust extraction across diverse PDF layouts.

The solution uses:

- **pdfminer.six** for parsing PDF text and layout.
- **numpy** for statistical analysis of font sizes.
- (Optionally) **scikit-learn** for clustering font sizes (if you use the advanced version).
  
## Features

- Extracts title and headings at the line level from PDFs.
- Assigns heading levels based on relative font size clusters.
- Avoids hardcoded font size thresholds; auto-adapts to PDF font characteristics.
- Skips numeric-only or irrelevant lines.
- Produces a JSON output containing the document title and structured outline.

## Project Structure

├── input/ # Place your input PDF files here
├── output/ # The JSON output files will be saved here
├── process_pdfs.py # Main Python script for processing PDFs and extracting headings
├── requirements.txt # Python dependencies
└── README.md # This readme file

## Requirements

- Python 3.7+
- pdfminer.six
- numpy

## Usage

1. Place your PDF files inside the `input` directory.
2. Run the extraction script:

python process_pdfs.py

text

3. The results (title and outline JSON) will be saved in the `output` directory with the same base filename as the PDFs.

## Output Format

The output JSON for each PDF looks like:

{
"title": "Document Title",
"outline": [
{"level": "H1", "text": "Main Heading", "page": 1},
{"level": "H2", "text": "Subheading", "page": 2},
{"level": "H3", "text": "Sub-subheading", "page": 3}
]
}

text

## Docker Usage (Optional)

Build the docker container:

docker build -t mysolutionname:somerandomidentifier .

text

Run the container (assuming current directory contains `input` and `output` folders):

docker run -it --rm
-v "${PWD}/input:/app/input"
-v "${PWD}/output:/app/output"
--network none
mysolutionname:somerandomidentifier
