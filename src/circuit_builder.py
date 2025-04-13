# circuit_ai.py
import json
import os
from typing import Dict, Any

import networkx as nx
import google.generativeai as genai
from dotenv import load_dotenv

# Constants
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(ROOT_DIR, '.env')
DATA_PATH = os.path.join(ROOT_DIR, 'data', 'sample_circuit_info.json')

def initialize_api():
    """Initialize Gemini API with environment variables."""
    print(f"Loading .env from: {os.path.abspath(ENV_PATH)}")
    load_dotenv(ENV_PATH)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    print(f"Loading API Key from: {ENV_PATH}")
    genai.configure(api_key=api_key)

def circuit_data() -> Dict[str, Any]:
    """Load circuit data from JSON file."""
    try:
        with open(DATA_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Circuit data not found at {DATA_PATH}")

def build_graph(data: Dict[str, Any]) -> nx.Graph:
    """Build NetworkX graph from circuit data."""
    graph = nx.Graph()
    for comp in data['components']:
        graph.add_node(comp['id'], type=comp['type'], value=comp['value'])
    for conn in data['connections']:
        graph.add_edge(*conn)
    return graph

def describe_graph(graph: nx.Graph) -> str:
    """Convert graph to text description."""
    description = []
    for node, attrs in graph.nodes(data=True):
        description.append(f"{node} is a {attrs['type']} with value {attrs['value']}")
    description.append("\nConnections:")
    for u, v in graph.edges():
        description.append(f"{u} is connected to {v}")
    return "\n".join(description)

def analyze_circuit(prompt: str) -> str:
    """Generate circuit analysis using Gemini AI."""
    model = genai.GenerativeModel(model_name='models/gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

def main() -> None:
    """Main execution pipeline."""
    try:
        initialize_api()
        data = circuit_data()
        circuit_graph = build_graph(data)
        text_description = describe_graph(circuit_graph)

        prompt = f"""
        You are an expert electronics engineer. Analyze the following circuit and provide:
        1. A high-level explanation.
        2. Any potential issues.
        3. Suggestions for improvements.

        Use the following circuit description:
        {text_description}
        """

        print("Circuit Description:\n", text_description)
        print("\nGemini AI Response:\n", analyze_circuit(prompt))

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
