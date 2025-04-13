import google.generativeai as genai
import json
import schemdraw
import schemdraw.elements as elm
from datetime import datetime
import os
import base64
from typing import Dict, Any, Optional


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
    filename = f'{timestamp}.svg'
    filepath = os.path.join(results_dir, filename)
    d.save(filepath)
    return filepath


def process_image_for_json(
    image_path: str,
    json_schema: Dict[str, Any],
    api_key: Optional[str] = None,
    model: str = "gemini-2.0-flash"
) -> Dict[str, Any]:
    if api_key:
        genai.configure(api_key=api_key)

    file_extension = os.path.splitext(image_path)[1][1:].lower()
    mime_type = f"image/{file_extension}"

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    instructions = """
Generate a JSON response similar to this one:
{
  "resistors": 2,
  "resistor_value": "10Ω",
  "leds": 3,
  "led_colors": ["red", "green", "blue"],
  "grounding": true
}
Grounding is always true.
The values of resistors and LEDs are always in Ohms and colors respectively.
If you don't know the value, use '3Ω' for resistors and 'Default' for LEDs.
"""

    # Create the model instance (renamed from 'model' to avoid shadowing)
    model_instance = genai.GenerativeModel(model)

    # Pass the response_schema as part of the generation_config dictionary.
    response = model_instance.generate_content(
        [
            instructions,
            {
                "mime_type": mime_type,
                "data": encoded_image
            }
        ],
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": json_schema
        }
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse JSON response",
            "raw_response": response.text
        }
