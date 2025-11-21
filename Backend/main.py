from database import db
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import bcrypt


load_dotenv()

app = FastAPI(title="ToDo_App", version="1.0.0")

class simple(BaseModel):
    name: str= Field("Olamide")
    email: str= Field("olamide@gmail.com")
    password: str= Field("ola123")

@app.post("/sign_up")
def sign_up(input: simple):
    try:
        # for existing email
        query = text("""
            SELECT * FROM users
            WHERE email = :email
        """)

        exists = db.execute(query, {"email" : input.email})
        if exists:
            print("This email already exists")
            #new users
        new_query = text("""
            INSERT INTO users(name, email, password)
            VALUES(:name, :email, :password)
        """)
            #password encryption
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        print(hashed_password)

        db.execute(new_query, {"name": input.name, "email": input.email, "password": hashed_password})
        db.commit()

        return{
            "message" : "User signed up successfully",
            "data": {"name": input.name, "email": input.email}
        }

    except Exception as e:
        raise HTTPException(status_code=501, detail=str(e))
    
class dimple(BaseModel):
    email: str= Field('olamide@gmail.com')
    password: str= Field('ola123')

@app.post('/sign_in')
def sign_in(input: dimple):
    try:
        #do we have you in the database?
        query = text("""
            SELECT * FROM users
            WHERE email = :email
        """)

        ours = db.execute(query, {"email": input.email}).fetchone()
        if not ours:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        our_password = bcrypt.checkpw(input.password.encode('utf-8'), ours.password.encode('utf-8'))
        if not our_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        return{
            "message": "User Logged in successfully",
            "data": {input.email}
        }
        


    except Exception as e:
        raise HTTPException(status_code=501, detail=str(e))


    
if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('host'), port=int(os.getenv('port')))

