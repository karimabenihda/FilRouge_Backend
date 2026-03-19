import joblib
import os 
from fastapi import APIRouter,Query

# ── Artifact paths ────────────────────────────────────────────────────────────
ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../model")
MODEL_PATH    = os.path.join(ARTIFACTS_DIR, "recommendation_system.joblib")
hybrid_similarity = joblib.load(MODEL_PATH)


recommendation_route=APIRouter()

def recommend_for_item(item_id: str, top_n: int = 5):
    if item_id not in hybrid_similarity.columns:
        return {"error": f"Item '{item_id}' not found"}
    similar = hybrid_similarity[item_id].sort_values(ascending=False)
    return similar.iloc[1:top_n + 1].index.tolist()

 
@recommendation_route.get("/recommend/{item_id}")
def get_recommendations(item_id: str, top_n: int = Query(default=5, ge=1, le=20)):
    result = recommend_for_item(item_id, top_n)
    return {"item_id": item_id, "recommendations": result}
 