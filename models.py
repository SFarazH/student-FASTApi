from pydantic import BaseModel

# creating models to update data
class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address
