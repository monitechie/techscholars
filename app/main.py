# app/main.py

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from . import models, database
from .routers import admin, user, test, auth
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import SecurityScheme as SecuritySchemeModel
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Test Management System"}


@app.get("/secure-data/")
async def secure_data(token: str = Depends(oauth2_scheme)):
    return {"message": "This is secure data"}


@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    if not app.openapi_schema:
        app.openapi_schema = app.openapi()
        app.openapi_schema["components"]["securitySchemes"] = {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "tokenUrl": "token",
                        "scopes": {}
                    }
                }
            }
        }
        app.openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    return app.openapi_schema

app.include_router(admin.router, prefix="/admin")

app.include_router(user.router, prefix="/users")


app.include_router(test.router, prefix="/tests", tags=["tests"])
app.include_router(auth.router, prefix="/auth")
