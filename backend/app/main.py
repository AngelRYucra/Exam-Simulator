# from fastapi import FastAPI
# from app.database import Base, engine
# from app.models.question import Question
# from app.models.answer import Answer
# from app.routers.questions import router as questions_router
# from app.routers.answers import router as answers_router
# from app.routers import exam
# from fastapi.middleware.cors import CORSMiddleware



# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.include_router(questions_router)
# app.include_router(answers_router)
# app.include_router(exam.router)

# @app.get("/")
# def root():
#     return {"message": "Backend is running"}

# origins = [
#     "http://localhost:5173",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# We only import the exam router now, because it handles everything via the JSON service!
from app.routers import exam

app = FastAPI()

# 1. Setup CORS so React can talk to FastAPI
origins = [
    "http://192.168.18.39:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Include ONLY your active, clean router
app.include_router(exam.router)

# 3. Simple health check route
@app.get("/")
def root():
    return {"message": "Backend is running"}