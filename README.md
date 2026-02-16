# Mini Resume Management API

## Project Overview

The Mini Resume Management API is a RESTful backend application built using FastAPI.  
It allows users to manage candidate resume data including personal details, education, experience, skills, and resume file uploads.

This project was developed as part of a backend technical assessment.

---

## Tech Stack

- Python 3.9+
- FastAPI
- Uvicorn
- Pydantic
- Python Multipart (for file uploads)

---

## Project Structure

```
miniresume-razal-kr/
│
├── main.py
├── README.md
├── requirements.txt
├── uploads/
└── venv/
```

- `main.py` – Application entry point  
- `uploads/` – Stores uploaded resume files  
- `requirements.txt` – Project dependencies  

---

## Setup Instructions

### 1. Clone or Download the Project

Navigate to the project directory:

```bash
cd path/to/your/project
```

Example (Windows):

```bash
cd C:\Users\PC\Desktop\miniresume-razal-kr
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

---

### 3. Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

After activation, you should see:

```
(venv)
```

---

### 4. Install Dependencies

```bash
pip install fastapi uvicorn python-multipart
```

Or using requirements file:

```bash
pip install -r requirements.txt
```

---

### 5. Run the Application

```bash
uvicorn main:app --reload
```

If successful, you will see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

## Access API Documentation

Open your browser and navigate to:

```
http://127.0.0.1:8000/docs
```

This opens the interactive Swagger UI where all endpoints can be tested.

## API Endpoints

### Health Check

**GET** `/health`  
Returns application status.

---

### Create Candidate

**POST** `/candidates`

**Form Data Required:**

- full_name (string)  
- dob (date)  
- contact_number (string)  
- contact_address (string)  
- education (string)  
- graduation_year (integer, max 2026)  
- experience_years (float)  
- skills (comma-separated string)  
- resume (PDF/DOC/DOCX file)  

Returns the created candidate with an auto-generated ID.

---

### List Candidates

**GET** `/candidates`

**Optional Query Parameters:**

- skill  
- min_experience  
- graduation_year  

---

### Get Candidate by ID

**GET** `/candidates/{id}`

---

### Delete Candidate

**DELETE** `/candidates/{id}`
## Validation Rules

- Date of Birth must be in the past  
- Graduation year cannot exceed 2026  
- Experience years cannot be negative  
- Only PDF, DOC, DOCX file formats allowed  
- Candidate ID is auto-generated (incremental)  

---

## Data Storage

- Uploaded resume files are saved inside the `uploads/` folder  
- Candidate data is stored in memory  
- Data resets when the server restarts  

---

## Testing the Application

1. Start the server  
2. Open `/docs`  
3. Test all endpoints using Swagger UI  
4. Verify filtering and validation  

---

## Stop the Server

Press:

```
CTRL + C
```
