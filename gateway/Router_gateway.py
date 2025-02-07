from fastapi import FastAPI, HTTPException ,  File, UploadFile
import fastapi as _fastapi
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from jwt.exceptions import DecodeError
from fastapi import APIRouter
import schema 
import requests
import base64
import pika
import logging
import os
import jwt
import httpx
import rpc_client

router_gateway= APIRouter(tags=['Authentication Service'])
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Retrieve environment variables
JWT_SECRET = os.environ.get("JWT_SECRET")
AUTH_BASE_URL = os.environ.get("AUTH_BASE_URL")
RABBITMQ_URL = os.environ.get("RABBITMQ_URL")

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_URL)) # add container name in docker
channel = connection.channel()
channel.queue_declare(queue='gatewayservice')
channel.queue_declare(queue='ocr_service')



# JWT token validation
async def jwt_validation(token: str = _fastapi.Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")

# Authentication routes
@router_gateway.post("/auth/login")
async def login(user_data: schema.UserCredentials):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_BASE_URL}/api/token",
                json={"username": user_data.username, "password": user_data.password},
                timeout=10  # Set a timeout for the request
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
        
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Authentication service is unavailable")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")

    

@router_gateway.post("/auth/register")
async def registeration(user_data:schema.UserRegisteration):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_BASE_URL}/api/users",
                json={"name": user_data.username, "email": user_data.email, "password": user_data.password},
                timeout=10  # Set a timeout for the request
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
                
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Authentication service is unavailable")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
      

@router_gateway.post("/auth/generate_otp")
async def generate_otp(user_data:schema.GenerateOtp):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_BASE_URL}/api/users/generate_otp",
                json={"email": user_data.email},
                timeout=10  # Set a timeout for the request
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())

        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Authentication service is unavailable")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
   

@router_gateway.post("/auth/verify_otp")
async def verify_otp(user_data:schema.VerifyOtp):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_BASE_URL}/api/users/verify_otp",
                json={"email": user_data.email, "otp": user_data.otp},
                timeout=10  # Set a timeout for the request
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())

        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Authentication service is unavailable")
        except httpx.RequestError as e:
   
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
  
        
# ml microservice route - OCR route
@router_gateway.post('/ocr' ,  tags=['Machine learning Service'] )
def ocr(file: UploadFile = File(...),
        payload: dict = _fastapi.Depends(jwt_validation)):
    
    # Save the uploaded file to a temporary location
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    ocr_rpc = rpc_client.OcrRpcClient()

    with open(file.filename, "rb") as buffer:
        file_data = buffer.read()
        file_base64 = base64.b64encode(file_data).decode()
    
    request_json = {
        'user_name':payload['name'],
        'user_email':payload['email'],
        'user_id':payload['id'],
        'file': file_base64
    }
   
    # Call the OCR microservice with the request JSON
    response = ocr_rpc.call(request_json)

    # Delete the temporary image file
    os.remove(file.filename)

    return response



