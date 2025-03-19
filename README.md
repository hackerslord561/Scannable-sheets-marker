# Scannable-sheets-marker
A Program to mark examination scannable sheets using Open CV in Python

In extract_answers, the threshold for detecting a marked box was raised to 0.7 (70% dark pixels) to ensure it detects fully shaded boxes rather than partial marks like ticks

This was programmed based on the scannable sheets used during official examniations in Ghana

## How It Works

**Alignment**: The
`align_image` function corrects any skew in the scanned sheet using corner markers.

**Answer Extraction:** The `extract_answers` function checks each box for shading by counting dark pixels after thresholding. A box is marked only if >70% of it is shaded.

**Scoring**: The `score_answers` function compares the detected answers with the answer key.

**Output**: The `mark_sheet` function returns the score and the student’s answers for verification.

## Customization
**Box Layout**: Adjust `bubble_size`, `start_x`, `start_y`, `spacing_x`, and `spacing_y` to match your OMR sheet’s design.

**Shading Threshold**: The 70% threshold (0.7) can be tuned (e.g., 0.6 or 0.8) based on how students shade the boxes.

**Image Resolution**: Modify width and height in align_image if your scans have a different resolution.

## Running the Code
**Install Dependencies**: Run `pip install opencv-python numpy` if you haven’t done so already.

**Provide Input**: Replace `"sample_sheet.png"` with the path to your scanned OMR sheet and ensure `answer_key` matches your exam (50 answers in my code).

**Execute**: Now run the script to get the score and answers

## Troubleshooting
**File Not Found Error**:
Double-check the image_path. Ensure the file exists at that location and the path is correct.

**Alignment Issues**:
If the code can’t detect corner markers, ensure your sheet has clear, large markers (e.g., black squares) and the scan isn’t too skewed.

**Incorrect Answers**:
If shaded boxes aren’t detected properly, adjust the threshold in extract_answers (e.g., change 0.7 to 0.6 or 0.8) or verify the box positions (`bubble_size`, `spacing_x`, etc.) match your sheet.










