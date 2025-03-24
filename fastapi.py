from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import httpx

app = FastAPI()

# Keycloak Configuration
KEYCLOAK_URL = "http://localhost:8080"
REALM = "myrealm"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token")

async def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify the JWT token with Keycloak."""
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return response.json()

@app.get("/protected")
async def protected_route(user_info: dict = Depends(verify_token)):
    print("calling this")
    """Returns user info for authenticated users."""
    return {"message": "Authenticated!", "user": user_info}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
