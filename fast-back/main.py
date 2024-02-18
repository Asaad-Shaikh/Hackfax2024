import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, init_db
from models import Login

#  AI-related imports
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ai.prompt import generate_context, qa_template

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = FastAPI()

# Initialize the database
init_db()

# CORS middleware setup
origins = ["http://localhost:3000",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/logins/")
async def create_login(login_request: LoginRequest, db: Session = Depends(get_db)):
    # Check if the username already exists to prevent duplicates
    existing_user = db.query(Login).filter(Login.username == login_request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    
    # Insert the new username into the database
    db_login = Login(username=login_request.username)
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    context = generate_context(db_login)
    llm = OpenAI(
        temperature=0,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
    )
    prompt = PromptTemplate(
        input_variables=["context", "question"], template=qa_template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(context=context, question=db_login)


    return {"response": response}
    #return {"status": "Username stored in database successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
