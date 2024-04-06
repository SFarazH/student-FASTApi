# API Documentation

Student data API created using FASTApi

## Overview

This API provides endpoints to manage student records. It allows creating, reading, updating, and deleting student information.

## Endpoints

- **Create Student**: `POST /student`
  - Creates a new student record.
  - Request Body: `Student` object
  - Response: Successful Response or Validation Error

- **List Students**: `GET /students`
  - Retrieves a list of students optionally filtered by country and/or age.
  - Query Parameters: `country` (string), `age` (integer)
  - Response: Successful Response or Validation Error

- **Get Student**: `GET /students/{student_id}`
  - Retrieves details of a specific student identified by `student_id`.
  - Path Parameter: `student_id` (string)
  - Response: Successful Response or Validation Error

- **Update Student**: `PATCH /students/{student_id}`
  - Updates details of a specific student identified by `student_id`.
  - Path Parameter: `student_id` (string)
  - Request Body: Updated student data (`object`)
  - Response: Successful Response or Validation Error

- **Delete Student**: `DELETE /students/{student_id}`
  - Deletes a specific student identified by `student_id`.
  - Path Parameter: `student_id` (string)
  - Response: Successful Response or Validation Error

## Schemas

- **Student**: Represents student information including name, age, and address.
    ```json
    {
        "name": "string",
        "age": 0,
        "address": {
            "city": "string",
            "country": "string"
        }
    }

## Usage

To use this API, send HTTP requests to the appropriate endpoints as described above. Make sure to handle validation errors as described in the responses section of each endpoint.

