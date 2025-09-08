from fastapi import FastAPI
from .routers import auth, projects, payments, admin, editors

app = FastAPI(title="Video Editing Service API")

@app.get("/")
def root():
    return {"message": "✅ Video Editing Service Backend is Live!"}

# Include routers with prefixes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(editors.router, prefix="/editors", tags=["Editors"])
