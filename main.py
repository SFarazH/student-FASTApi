import os
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException, Query, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from models import Student
from bson import ObjectId

load_dotenv() 
client = AsyncIOMotorClient(os.getenv("mongodb_uri"))
db = client['cosmo'] #connect db
collection = db["student"] #conect to collection
app = FastAPI()

# Create student
@app.post('/student')
async def create_student(student: Student):
    try:
        student_data = student.dict()
        result = await collection.insert_one(student_data)
        student_id = str(result.inserted_id) #get inserted student_id 
        content = jsonable_encoder({"id": student_id})
        return JSONResponse(content=content, status_code=201) #send 201 response along with student id
    except Exception as e:
        print(e)
    

#Get students list
@app.get("/students")
async def list_students(
    country: str = Query(None),
    age: int = Query(None) 
    #getting values from query
):
    try:
        query = {}
        if country:
            query["address.country"] = country
        if age is not None:
            query["age"] = {"$gte": age} #applying 'greater than equal to' criteria on age 
            
        cursor = collection.find(query, {"_id": 0, "name": 1, "age": 1}) #returning only the name and age
        students = await cursor.to_list(length=None)
        content = jsonable_encoder({"data": students})
        return JSONResponse(content=content, status_code=200) #returning data along with 200 status code
    
    except Exception as e:
        return {"error": str(e)}

#get specific student from ID
@app.get('/students/{student_id}')
async def get_student(student_id: str):
    try:
        collection = db["student"]
        student  = await collection.find_one({"_id": ObjectId(student_id)},{"_id": 0})
        if student:
            content = jsonable_encoder(student)
            return JSONResponse(content=content, status_code=200) 
        else:
            #if no student found with id
            raise HTTPException(status_code=404, detail="Student not found") 
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
#update student
@app.patch("/students/{student_id}")
async def update_student(
    student_id: str,
    updated_data: dict = None #get data to update
):
    try:
        student_id = ObjectId(student_id)
        result = await collection.find_one({"_id": ObjectId(student_id)})
        if result:
            if updated_data is None:
                updated_data = {}
            updated_address = updated_data.pop('address', None) #remove the address object , if found
            
            # removed the address object and handled it differently because 
            # if only city or country field is entered to be updated, it will overwrite the address field in db
            
            if updated_data:
                await collection.update_one({"_id": student_id}, {"$set": updated_data})

            if updated_address:
                address_updates = {}
                for key, value in updated_address.items():
                    if value is not None:
                        address_updates[f"address.{key}"] = value #updating only those fields of address object which have been entered
                
                if address_updates:
                    await collection.update_one({"_id": student_id}, {"$set": address_updates})
            return Response(status_code=204)
        else:
            raise HTTPException(status_code=404, detail="Student not found") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# delete student data
@app.delete("/students/{student_id}")
async def delete_student(student_id: str):
    try:
        result = await collection.find_one({"_id": ObjectId(student_id)})
        if result:
            await collection.delete_one({"_id": ObjectId(student_id)})
            content = jsonable_encoder({})
            return JSONResponse(status_code=200,content=content)
        else:
            raise HTTPException(status_code=404, detail="Student not found") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))