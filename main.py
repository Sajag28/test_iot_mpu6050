import logging
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI
app = FastAPI()

# Set up OpenAI client using the API key from the environment variable
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Connect to MongoDB using the connection string from the environment variable
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client["Confirm"]  # Replace with your database name
collection = db["Peple"]  # Replace with your collection name

# Define data model for the request
class OpenAIRequest(BaseModel):
    contact: str  # Change from query_id to contact

class SensorData(BaseModel):
    distance: str
    timestamp: str

# Define endpoint to get response from OpenAI
# @app.post("/retrieve")
# async def generate_response(request: OpenAIRequest):
#     try:
#         # Fetch data from MongoDB based on the contact field
#         data = collection.find_one({"contact": request.contact})  # Use the contact field

#         if data is None:
#             raise HTTPException(status_code=404, detail="Data not found")

#         # Use the fetched data in the prompt
#         prompt = f"Give me the info on the following company: {data['Company']}"  # Adjust the field name if needed

#         # Call OpenAI API using the new client
#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",  # Use the correct model name
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=100  # You can adjust this as needed
#         )

#         return {"response": completion.choices[0].message.content}

#     except Exception as e:
#         logging.error(f"Error occurred while generating response: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# Define endpoint to store sensor data
@app.post("/sensor")
async def sensor_data(request: SensorData):
    try:
        # Print the incoming sensor data to the console (or serial monitor)
        logging.info(f"Received sensor data: Distance: {request.distance}, Timestamp: {request.timestamp}")

        # Prepare the data to be inserted into MongoDB
        sensor_record = {
            "distance": request.distance,
            "timestamp": request.timestamp
        }
        
        # Insert the sensor data into the MongoDB collection
        result = collection.insert_one(sensor_record)

        # Return the ID of the inserted document
        return {"inserted_id": str(result.inserted_id)}

    except Exception as e:
        logging.error(f"Error occurred while inserting sensor data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run the application using Uvicorn
# Command to run: uvicorn main:app --reload