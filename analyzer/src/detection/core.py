import cv2
import numpy as np
import yaml
from .grid import GridMapper


class BreadboardAnalyzer:
    def __init__(self, config_path="configs/default.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        grid_params = self.config.get('grid_params', {})
        rows = grid_params.get('rows', 30)
        cols = grid_params.get('cols', 10)
        self.grid = GridMapper(rows, cols)

    def process_image(self, img_path):
        img = cv2.imread(img_path)
        processed = self._preprocess(img)
        components = self._detect_components(processed)
        wires = self._detect_colored_wires(img)
        return {'image': img, 'components': components, 'wires': wires}

    def _preprocess(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.GaussianBlur(gray, (5, 5), 0)

    def _detect_components(self, img):
        edges = cv2.Canny(img, 50, 150)
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return [self._contour_data(c) for c in contours if cv2.contourArea(c) > 100]

    def _contour_data(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        return {'type': 'component', 'bbox': (x, y, w, h), 'centroid': (x+w//2, y+h//2)}

    def _detect_colored_wires(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        wire_colors = self.config['wire_colors']

        detected_wires = []
        for color_name, (lower_bound, upper_bound) in wire_colors.items():
            lower_bound = np.array(lower_bound)
            upper_bound = np.array(upper_bound)

            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) > 50:   # Filter small noise
                    x, y, w, h = cv2.boundingRect(contour)
                    detected_wires.append({
                        'type': 'wire',
                        'color': color_name,
                        'bbox': (x, y, w, h),
                        'centroid': (x+w//2, y+h//2)
                    })

        return detected_wires
