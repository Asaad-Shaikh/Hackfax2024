from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware setup to allow requests from your React app
origins = [
    "http://localhost:3000",  # Assuming your React app runs here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str

@app.post("/logins/")
async def login(login_request: LoginRequest):
    # Here you would typically handle the login request, e.g., check credentials
    # For demonstration, we'll just echo back the username received
    response_message = f"Received username: {login_request.username}"
    return {"status": response_message}

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
