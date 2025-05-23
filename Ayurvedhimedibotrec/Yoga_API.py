from fastapi.staticfiles import StaticFiles 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Optional
from pathlib import Path

app = FastAPI()
# In yoga_api.py
app.mount("/static", StaticFiles(directory="D:\Yoga\IMAGES"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load yoga pose data - with better error handling
try:
    yoga_file = Path(r"D:/Yoga/DATA/Yoga_Dataset")  # Using raw string and Path
    with open(yoga_file) as f:
        yoga_db = json.load(f)
except FileNotFoundError:
    yoga_db = {"poses": []}
    print("Error: Yoga dataset not found at specified path")
except json.JSONDecodeError:
    yoga_db = {"poses": []}
    print("Error: Invalid JSON format in yoga dataset")

@app.get("/search")
def search_poses(query: Optional[str] = None):
    if not query:
        return {"results": []}
    
    query = query.lower().strip()
    results = []
    
    for pose in yoga_db.get("poses", []):
        # Verify image URL exists in the pose data
        if "image_url" not in pose:
            pose["image_url"] = ""  # Set default if missing
            
        score = 0
        
        # Check indication
        if query in pose.get("indication", "").lower():
            score += 2
        
        # Check pose names
        if query in pose.get("pose_name", "").lower():
            score += 1.5
        if query in pose.get("sanskrit_name", "").lower():
            score += 1
            
        # Check purpose and description
        if query in pose.get("purpose", "").lower():
            score += 1
        if query in pose.get("description", "").lower():
            score += 0.5
            
        if score > 0:
            results.append({
                "pose": pose,
                "score": score
            })
    
    # Sort by score and return top 5
    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": [item["pose"] for item in results[:5]]}

@app.get("/poses")
def get_all_poses():
    """Endpoint to verify all pose data (including images) is loading correctly"""
    return yoga_db