# EduTrack — Micro-Learning Progress & Analytics API
A robust REST API prototype for a mobile micro-learning platform. Built with **FastAPI**, **SQLModel**, and **SQLite**, this project utilizes a clean Service Layer Architecture to separate routing, business logic, and database operations.
## Getting Started
Follow these instructions to set up the project and run it locally.
### 1. Create a Virtual Environment (Recommended)
Isolate your project dependencies by creating a virtual environment:
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

### 2. Install Dependencies
Ensure your `requirements.txt` is in the root directory, then run:
   pip install -r requirements.txt

### 3. Start the Server (and Initialize Database)
You don't need to manually create the database. Upon starting the server for the first time, the application will automatically generate the `microlearning.db` SQLite file and seed it with sample courses and a test user.
Run the development server using Uvicorn:
   uvicorn main:app --reload

### 4. Explore the API Documentation
FastAPI automatically generates interactive documentation. Once the server is running, open your browser and navigate to the Swagger UI to test all endpoints:
* **Interactive Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
