from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Optional


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load medicine data - make sure the path is correct
try:
    with open('Data/Dataset_Ayur.json') as f:
        medicines_db = json.load(f)
except FileNotFoundError:
    medicines_db = {"medicines": []}
    print("Warning: Dataset_Ayur.json not found - using empty database")

@app.get("/search")
def search_medicines(query: Optional[str] = None):
    if not query:
        return {"results": []}
    
    query = query.lower().strip()
    results = []
    
    for medicine in medicines_db.get("medicines", []):
        # Check medicine name, indications, and ingredients
        score = 0
        
        # Check medicine name
        if query in medicine.get("medicine", "").lower():
            score += 2
        
        # Check indications - handle both string and list formats
        indications = medicine.get("indications", "")
        if isinstance(indications, str):
            indications_list = [i.strip().lower() for i in indications.split(",")]
        else:
            indications_list = [i.lower() for i in indications]
            
        score += sum(1 for ind in indications_list if query in ind)
        
        # Also check ingredients
        ingredients = medicine.get("ingredients", [])
        score += sum(0.5 for ing in ingredients if query in ing.lower())
        
        if score > 0:
            results.append({
                "medicine": medicine,
                "score": score
            })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": [item["medicine"] for item in results[:5]]}  # Return top 5 matches