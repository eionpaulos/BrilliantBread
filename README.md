# bitcamp2025

Bread Board Image to Diagram Converter

## Setup:

Clone the repository

```bash

git clone git@github.com:eionpaulos/bitcamp2025.git
cd bitcamp2025
```

### Server Setup:

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --reload
```

### Client Setup:

```bash
cd client
pnpm install
pnpm run dev
```

## Usage:

1. Open the client in your browser (default: http://localhost:5173)
2. Upload a breadboard image
3. Click "Analyze" to generate the diagram
4. Download the diagram as a SVG file
