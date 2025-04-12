import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2


def show_components(results):
    img = results['image']
    components = results['components']
    wires = results['wires']

    plt.figure(figsize=(12, 8))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Draw components (e.g., LEDs or resistors)
    for comp in components:
        x, y, w, h = comp['bbox']
        plt.gca().add_patch(patches.Rectangle(
            (x, y), w, h,
            linewidth=1.5,
            edgecolor='cyan',
            facecolor='none'
        ))

    # Draw wires with their respective colors
    for wire in wires:
        x, y, w, h = wire['bbox']
        color_map = {
            'red': 'red',
            'blue': 'blue',
            'green': 'green',
            'yellow': 'yellow'
        }
        plt.gca().add_patch(patches.Rectangle(
            (x, y), w, h,
            linewidth=1.5,
            edgecolor=color_map.get(wire['color'], 'white'),
            facecolor='none'
        ))

    plt.title(f"Detected Components: {len(components)}, Wires: {len(wires)}")
    plt.show()
