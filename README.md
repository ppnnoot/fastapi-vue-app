# FastAPI and Vue.js Full Stack Application

This project is a full-stack application using FastAPI for the backend and Vue.js with Vuetify for the frontend. The backend is containerized using Docker Compose, with a PostgreSQL database as the data store. The application allows users to upload files, which are processed on the backend, and then displays the data on the frontend.

## Table of Contents
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Folder Structure](#folder-structure)

## Features
- **File Upload**: Users can upload `.csv` or `.xlsx` files which are processed and validated.
- **Data Processing**: Uploaded files are parsed with Pandas and returned as JSON data.
- **Frontend UI**: Built with Vue 3, Vuetify, and Pinia for state management.
- **Dockerized Services**: Both the frontend and backend run in Docker containers.
- **Database**: PostgreSQL for storing and managing structured data.

## Setup and Installation

### Prerequisites
- **Docker** and **Docker Compose** installed on your system.
- Basic knowledge of Docker, FastAPI, and Vue.js.

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ppnnoot/fastapi-vue-app.git
   cd fastapi-vue-app
   ```
2. Start the Application: Run the following command to build and start the services:
   ```
   docker-compose up --build
   ```

### Running Backend and Frontend Without Docker
If you encounter issues running the application with Docker, you can run the backend and frontend independently.

### Running the Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. **Run the FastAPI application:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   Access the backend at ```http://localhost:8000.```

### Running the Frontend
1. Navigate to the front directory:
   ```
   cd frontend
   ```

2. Install the required Node.js packages:
   ```
   npm install
   ```
3. Run the Vue application:
   ```
   npm run server
   ```

## Usage
1. File Upload:
- Open the frontend application.
- Select a file in .csv or .xlsx format.
- Click "Upload" to send the file to the backend for processing.
- After successful upload, the data will be displayed on the frontend.

2. API Endpoints:
- ```POST /uploadfile``` : Accepts file uploads in ```.csv``` or ```.xlsx``` format.
- Use Postman or similar tools to test API endpoints directly if needed.


