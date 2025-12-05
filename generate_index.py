import os
import json
import re

# Configuration
SOLUTIONS_DIR = 'solutions'
OUTPUT_FILE = 'data.json'

def extract_meta(content, name):
    # Regex to find <meta name="..." content="...">
    pattern = r'<meta\s+name=["\']' + re.escape(name) + r'["\']\s+content=["\'](.*?)["\']'
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(1) if match else ""

def extract_title(content):
    match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    return match.group(1) if match else "Untitled"

data = []

# Walk through the solutions directory
if not os.path.exists(SOLUTIONS_DIR):
    print(f"Error: Directory '{SOLUTIONS_DIR}' not found.")
    exit()

for filename in os.listdir(SOLUTIONS_DIR):
    if filename.endswith(".html"):
        filepath = os.path.join(SOLUTIONS_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract metadata
            entry = {
                "filename": filename,
                "path": f"{SOLUTIONS_DIR}/{filename}",
                "title": extract_title(content),
                "id": extract_meta(content, "algo-id"),
                "difficulty": extract_meta(content, "algo-difficulty"),
                "tags": [t.strip() for t in extract_meta(content, "algo-tags").split(',') if t.strip()],
                "description": extract_meta(content, "description")
            }
            
            # Only add if it has an ID (ignores helper files)
            if entry["id"]:
                data.append(entry)

# Sort by ID
data.sort(key=lambda x: int(x["id"]) if x["id"].isdigit() else 0)

# Write to JSON
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Successfully indexed {len(data)} solutions into {OUTPUT_FILE}")