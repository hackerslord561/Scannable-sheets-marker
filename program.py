import cv2
import numpy as np

def align_image(image):
    """Align the scanned image using corner markers."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Detect edges
    edged = cv2.Canny(blurred, 75, 200)
    
    # Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sort by area to find the largest rectangles (corner markers)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]
    
    if len(contours) != 4:
        raise ValueError("Could not detect four corner markers.")
    
    # Approximate corners
    corners = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  # Ensure it’s a quadrilateral
            corners.append(approx)
    
    # Order corners: top-left, top-right, bottom-right, bottom-left
    corners = np.vstack(corners).squeeze()
    corners = sorted(corners, key=lambda x: x[0] + x[1])  # Rough sorting by sum of coordinates
    top_left = corners[0]
    bottom_right = corners[-1]
    top_right = max(corners, key=lambda x: x[0])
    bottom_left = min(corners, key=lambda x: x[0] + x[1] - x[0])
    src_pts = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")
    
    # Define destination points for a 1000x1400 aligned image (adjust as needed)
    width, height = 1000, 1400
    dst_pts = np.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype="float32")
    
    # Compute perspective transform and warp image
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    aligned = cv2.warpPerspective(image, matrix, (width, height))
    return aligned

def extract_answers(aligned_image, num_questions=50, options_per_question=4):
    """Extract marked answers from the aligned image by detecting shaded boxes."""
    # Convert the image to grayscale for easier processing
    gray = cv2.cvtColor(aligned_image, cv2.COLOR_BGR2GRAY)
    answers = []
    
    # Define the size and layout of the answer boxes
    bubble_size = 20  # Size of each box in pixels (adjust based on your sheet)
    start_x, start_y = 50, 50  # Starting position of the boxes
    spacing_x, spacing_y = 30, 30  # Spacing between boxes horizontally and vertically
    
    # Loop through each question
    for q in range(num_questions):
        marked_option = -1  # Default: no option marked
        # Check each option for the current question
        for opt in range(options_per_question):
            # Calculate the position of the current box
            x = start_x + opt * spacing_x
            y = start_y + q * spacing_y
            # Extract the region of interest (ROI) for this box
            roi = gray[y:y+bubble_size, x:x+bubble_size]
            
            # Apply a threshold to detect dark (shaded) areas
            _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            dark_pixels = cv2.countNonZero(thresh)  # Count dark pixels
            total_pixels = bubble_size * bubble_size  # Total pixels in the box
            
            # Check if the box is shaded (more than 70% dark pixels)
            if dark_pixels / total_pixels > 0.7:
                if marked_option != -1:
                    # If multiple boxes are shaded, invalidate this question
                    marked_option = -1
                    break
                marked_option = opt  # Record the shaded option
        
        # Add the result for this question (-1 if no mark or multiple marks)
        answers.append(marked_option)
    
    return answers

def score_answers(answers, answer_key):
    """Calculate the score by comparing answers with the answer key."""
    score = 0
    option_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}  # Map letters to indices
    key_indices = [option_map[ans] for ans in answer_key]
    
    for student_ans, correct_ans in zip(answers, key_indices):
        if student_ans == correct_ans and student_ans != -1:
            score += 1
    return score

def mark_sheet(image_path, answer_key):
    """Main function to mark a single answer sheet."""
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Image file not found.")
    
    # Process the image
    aligned_image = align_image(image)
    answers = extract_answers(aligned_image)
    score = score_answers(answers, answer_key)
    
    # Map indices back to letters for display (optional)
    option_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', -1: 'None'}
    student_answers = [option_map[ans] for ans in answers]
    
    return score, student_answers

# Example usage
if __name__ == "__main__":
    # Sample answer key for 50 questions
    answer_key = ['A', 'C', 'B', 'D'] * 12 + ['A', 'B']  # Example, adjust length to 50
    image_path = "sample_sheet.png"  # Replace with your image path
    
    try:
        score, student_answers = mark_sheet(image_path, answer_key)
        print(f"Student Score: {score}/{len(answer_key)}")
        print("Student Answers:", student_answers)
    except Exception as e:
        print(f"Error: {e}")