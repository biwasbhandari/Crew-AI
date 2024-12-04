from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crews.bca_gpt.bca_crew import run_bca_research

# Create FastAPI app
app = FastAPI(
    title="BCA Research Assistant API",
    description="API for searching BCA questions from Tribhuvan University",
    version="0.1.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Input model for validation
class ResearchRequest(BaseModel):
    query: str

# Research endpoint
@app.post("/api/research")
async def research_endpoint(request: ResearchRequest):
    try:
        # Call the research function from the crew script
        result = run_bca_research(request.query)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}