# Flask API Project

This is a Flask API project that provides backend for the caculation of SDT based factors based on the CV and Psychodynamil surveys

## Features
- **User Authentication**: JWT-based login and registration.
- **PDF Text Extraction**: Extracts characteristics from uploaded PDF files.
- **Company Search**: Search functionality based on query and characteristics.
- **Chat with GPT**: Interact with ChatGPT through API prompts.
- **Test Functionality**: Allows users to take tests and saves the results.

## Requirements

- Docker
- OpenAI API Key (for ChatGPT integration)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2. Add Environment Variables
Create a .env file in the root directory to store your environment variables. This file should include your OpenAI API key and any other sensitive data.

```bash
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///database.db
OPENAI_API_KEY=your_openai_api_key
```

### 3. Build and Run with Docker
Build the Docker image:

```bash
docker build -t flask-api-project .
```

Run the Docker container:

```bash
docker run -p 5000:5000 --env-file .env flask-api-project
```
This command will:
- Expose the application on port 5000.
= Use the .env file to set environment variables.

## API Endpoints
Here are the primary API endpoints:

- User Registration: POST /api/register
- User Login: POST /api/login
- PDF Characteristics Extraction: POST /api/cv
- Company Search: GET /api/companies?query=<query>&characteristics=<characteristics>
- ChatGPT Integration: POST /api/chat
- Take a Survey: POST /api/test

## Example Usage
For each endpoint, you can use tools like curl or Postman to interact with the API.

#### Example Request for ChatGPT API:

```bash
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d '{"prompt": "Explain the importance of teamwork"}'
```

# Notes
- Ensure that you have configured all necessary environment variables before running.
- You can modify the Dockerfile and requirements.txt for additional dependencies or adjustments.

# License
This project is licensed under the MIT License
