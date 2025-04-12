from src.detection.core import BreadboardAnalyzer
from src.utils.visualization import show_components

if __name__ == "__main__":
    analyzer = BreadboardAnalyzer()

    # Replace "data/raw/demo.jpg" with your image path
    results = analyzer.process_image("data/raw/demo.jpg")

    show_components(results)
