import cv2
import numpy as np
import os

def find_breadboard_holes(image_path: str, output_path: str):
    # --- 1. Setup and Load Image ---
    # [Keep setup, loading, debug dir creation as before]
    output_dir = os.path.dirname(output_path)
    debug_dir = os.path.join(output_dir, "debug")
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading {image_path}")
        return
    print(f"Image loaded: {img.shape}")
    output_image = img.copy()
    debug_image_all_contours = img.copy()
    height, width, _ = img.shape

    # --- 2. Preprocessing ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    print("Preprocessing done.")

    # --- 3. Adaptive Thresholding ---
    block_size = 25
    C = 5
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, C)
    print(f"Thresholding done (Block: {block_size}, C: {C}).")
    cv2.imwrite(os.path.join(debug_dir, "1_thresholded.jpg"), thresh)

    # --- 4. Morphological Operations ---
    kernel = np.ones((3, 3), np.uint8)  # Keep 3x3 kernel for now
    # First, remove noise
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # === ADD CLOSING STEP ===
    # Now, try to fill gaps within the remaining white shapes
    # Use same kernel, 1 iteration
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
    # ========================
    processed_thresh = closing  # Use the result after closing
    print("Morphology (Opening then Closing) done.")
    # Save intermediate steps for comparison
    cv2.imwrite(os.path.join(debug_dir, "2a_morph_opening.jpg"), opening)
    cv2.imwrite(os.path.join(debug_dir, "2b_morph_closing.jpg"), closing)

    # --- 5. Detect Power Rail Regions & Define Boundaries ---
    # [Keep boundary detection logic exactly as before, including adjusted 0.18/0.82 values]
    # ... (boundary detection code) ...
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 60, 40])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    lower_red1 = np.array([0, 60, 40])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    lower_red2 = np.array([170, 60, 40])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_combined = cv2.bitwise_or(mask_blue, mask_red)
    kernel_lines = np.ones((5, 5), np.uint8)
    mask_combined_opened = cv2.morphologyEx(
        mask_combined, cv2.MORPH_OPEN, kernel_lines, iterations=2)
    mask_combined_closed = cv2.morphologyEx(
        mask_combined_opened, cv2.MORPH_CLOSE, kernel_lines, iterations=3)
    contours_lines, _ = cv2.findContours(
        mask_combined_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    left_boundary = width * 0.1
    right_boundary = width * 0.9
    min_line_height = height * 0.5
    potential_left_boundaries = []
    potential_right_boundaries = []
    for cnt in contours_lines:
        x, y, w, h_cnt = cv2.boundingRect(cnt)
        if h_cnt > min_line_height:
            center_x = x + w / 2
            roi_hsv = hsv[y:y+h_cnt, x:x+w]
            blue_pixels = cv2.countNonZero(
                cv2.inRange(roi_hsv, lower_blue, upper_blue))
            red_pixels = cv2.countNonZero(cv2.inRange(
                roi_hsv, lower_red1, upper_red1)) + cv2.countNonZero(cv2.inRange(roi_hsv, lower_red2, upper_red2))
            if blue_pixels > red_pixels and center_x < width * 0.4:
                potential_left_boundaries.append(x + w)
            elif red_pixels > blue_pixels and center_x > width * 0.6:
                potential_right_boundaries.append(x)
    if potential_left_boundaries:
        left_boundary = max(potential_left_boundaries) + 5
    else:
        print("Warning: Using default left boundary.")
    if potential_right_boundaries:
        right_boundary = min(potential_right_boundaries) - 5
    else:
        print("Warning: Using default right boundary.")
    top_boundary = height * 0.035
    bottom_boundary = height * 0.95
    print(
        f"Refined central area boundaries: X=[{left_boundary:.0f}, {right_boundary:.0f}], Y=[{top_boundary:.0f}, {bottom_boundary:.0f}]")
    # Draw boundary lines
    cv2.line(output_image, (int(left_boundary), 0),
             (int(left_boundary), height), (255, 0, 255), 1)
    cv2.line(output_image, (int(right_boundary), 0),
             (int(right_boundary), height), (255, 0, 255), 1)
    cv2.line(output_image, (0, int(top_boundary)),
             (width, int(top_boundary)), (255, 0, 255), 1)
    cv2.line(output_image, (0, int(bottom_boundary)),
             (width, int(bottom_boundary)), (255, 0, 255), 1)

    # --- 6. Find Contours ---
    # Find contours on the closed image
    contours, hierarchy = cv2.findContours(
        processed_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Found {len(contours)} initial contours (after closing).")
    # Draw all contours found after closing for debugging
    debug_image_post_closing_contours = img.copy()
    cv2.drawContours(debug_image_post_closing_contours,
                     contours, -1, (0, 0, 255), 1)
    cv2.imwrite(os.path.join(debug_dir, "3_all_contours_post_closing.jpg"),
                debug_image_post_closing_contours)

    # --- 7. Filter Contours ---
    # KEEP the relaxed filters from the previous step for now
    valid_holes = []
    hole_count = 0
    min_hole_area = 100
    max_hole_area = 420
    min_aspect_ratio = 0.6
    max_aspect_ratio = 1.6
    min_solidity = 0.65  # Keep relaxed solidity

    print(
        f"Filtering parameters: Area=[{min_hole_area}, {max_hole_area}], Aspect Ratio=[{min_aspect_ratio}, {max_aspect_ratio}], Solidity > {min_solidity}")

    # [Keep filtering loop exactly as before]
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if w == 0 or h == 0:
            continue
        aspect_ratio = float(w) / h
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = 0 if hull_area == 0 else float(area) / hull_area
        if not (min_hole_area <= area <= max_hole_area):
            continue
        if not (min_aspect_ratio <= aspect_ratio <= max_aspect_ratio):
            continue
        if not (left_boundary < cx < right_boundary and top_boundary < cy < bottom_boundary):
            continue
        if solidity < min_solidity:
            continue
        valid_holes.append(cnt)
        hole_count += 1

    print(f"Found {hole_count} potential holes after filtering.")

    # --- 8. Draw Results ---
    # [Keep drawing logic as before]
    if valid_holes:
        cv2.drawContours(output_image, valid_holes, -1, (0, 255, 0), 1)
    cv2.putText(output_image, f"Detected Holes: {hole_count}", (
        20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # --- 9. Save and Finish ---
    # [Keep saving logic as before, maybe update filename]
    try:
        output_path_v4 = output_path.replace(".jpg", "_v4.jpg")  # Append v4
        cv2.imwrite(output_path_v4, output_image)
        print(f"Successfully saved result image to {output_path_v4}")
    except Exception as e:
        print(f"Error saving image to {output_path_v4}: {e}")


# --- Execution ---
if __name__ == "__main__":
    INPUT_IMAGE = r"C:\Users\syedm\OneDrive\Desktop\Projects\projects\bitcamp2025\analyzer\data\raw\breadboard.jpg"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_IMAGE = os.path.join(script_dir, "data", "results",
                                "breadboard_holes_detected.jpg")  # Base name for saving v4
    os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)

    if not os.path.exists(INPUT_IMAGE):
        print(f"Error: Input file not found at {INPUT_IMAGE}")
    else:
        find_breadboard_holes(INPUT_IMAGE, OUTPUT_IMAGE)
