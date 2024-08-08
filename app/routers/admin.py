# app/routers/admin.py

from fastapi import APIRouter

router = APIRouter()

# Define your routes here


@router.get("/admin")
def read_admin():
    return {"message": "Admin endpoint"}
