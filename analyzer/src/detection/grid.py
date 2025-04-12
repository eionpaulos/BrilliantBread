import cv2
import numpy as np


class GridMapper:
    def __init__(self, rows=30, cols=10):
        self.rows = rows
        self.cols = cols

    def detect_grid(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                                minLineLength=100, maxLineGap=10)
        return self._process_lines(lines)

    def _process_lines(self, lines):
        if lines is None:
            return {'vertical': [], 'horizontal': []}
            
        vertical = []
        horizontal = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Calculate angle to determine if line is horizontal or vertical
            angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
            
            if angle < 45 or angle > 135:  # Horizontal lines
                horizontal.append(((x1, y1), (x2, y2)))
            else:  # Vertical lines
                vertical.append(((x1, y1), (x2, y2)))
        
        # Sort horizontal lines by y-coordinate
        horizontal.sort(key=lambda line: (line[0][1] + line[1][1]) / 2)
        
        # Sort vertical lines by x-coordinate
        vertical.sort(key=lambda line: (line[0][0] + line[1][0]) / 2)
        
        return {'vertical': vertical, 'horizontal': horizontal}
