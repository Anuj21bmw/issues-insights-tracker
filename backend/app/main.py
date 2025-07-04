from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth  # ✅ import auth router

app = FastAPI(title="Issues & Insights Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)  

@app.get("/")
def root():
    return {"message": "Backend running"}
