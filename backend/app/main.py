from fastapi import FastAPI
from .routers import auth, projects, payments, admin, editors

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Video Editing Service Backend is live!"}

# include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(payments.router)
app.include_router(admin.router)
app.include_router(editors.router)
