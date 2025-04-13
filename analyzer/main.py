import json
import schemdraw
import schemdraw.elements as elm
from datetime import datetime
import os


def create_circuit_diagram(json_data):
    data = json.loads(json_data)
    d = schemdraw.Drawing(show=False, config={
                          'orientation': 'horizontal', 'bgcolor': 'white'})

    d += elm.Battery(label="9V Battery")

    num_resistors = data.get('resistors', 0)
    resistor_value = data.get('resistor_value', '5Ω')

    for i in range(num_resistors):
        d += elm.Resistor(label=f"R{i+1} ({resistor_value})")

    num_leds = data.get('leds', 0)
    led_colors = data.get('led_colors', [])

    for i in range(num_leds):
        color = led_colors[i] if i < len(led_colors) else 'Default'
        d += elm.LED(label=f"LED{i+1} ({color})")

    if data.get('grounding', False):
        d += elm.Ground()

    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'circuit_diagram_{timestamp}.svg'
    filepath = os.path.join(results_dir, filename)
    d.save(filepath)
    return filepath
