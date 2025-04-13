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

# Initialize Gemini API with key in .env
def initialize_api():
    print(f"Loading .env from: {os.path.abspath(ENV_PATH)}")
    load_dotenv(ENV_PATH)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    print(f"Loading API Key from: {ENV_PATH}")
    genai.configure(api_key=api_key)

# Load circuit data from JSON file
def circuit_data() -> Dict[str, Any]:
    try:
        with open(DATA_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Circuit data not found at {DATA_PATH}")

# Build NetworkX graph from circuit data
def build_graph(data: Dict[str, Any]) -> nx.Graph:
    graph = nx.Graph()
    for comp in data['components']:
        graph.add_node(comp['id'], type=comp['type'], value=comp['value'])
    for conn in data['connections']:
        graph.add_edge(*conn)
    return graph

# Convert graph to text description
def describe_graph(graph: nx.Graph) -> str:
    description = []
    for node, attrs in graph.nodes(data=True):
        description.append(f"{node} is a {attrs['type']} with value {attrs['value']}")
    description.append("\nConnections:")
    for u, v in graph.edges():
        description.append(f"{u} is connected to {v}")
    return "\n".join(description)

# Generate circuit analysis using Gemini AI
def analyze_circuit(prompt: str) -> str:
    model = genai.GenerativeModel(model_name='models/gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

# Main function to execute the pipeline
def main() -> None:
    try:
        initialize_api()
        data = circuit_data()
        circuit_graph = build_graph(data)
        text_description = describe_graph(circuit_graph)

        prompt = f"""
        You are a student that has a circuit analysis assignment. 
        Reiterate the details about the components, their connections.
        Analyze the circuit and provide a high-level explanation of the circuit.

        Use the following circuit description:
        {text_description}
        """

        print("Circuit Description:\n", text_description)
        print("\n\nGemini AI Response:\n", analyze_circuit(prompt))

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
