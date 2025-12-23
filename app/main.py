from fastapi import FastAPI, Depends
from app.database import engine
from app.models import Base
from app.routes import files
from app.routes.users import router as user_router
from app.auth import get_current_user

app = FastAPI(title="File Upload API")

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(files.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"message": f"Hello {user.email}"}