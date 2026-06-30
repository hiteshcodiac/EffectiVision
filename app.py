# For Fastapi server and strict formatted answer (pydantic)
from fastapi import FastAPI
from fastapi import UploadFile, File
from pydantic import BaseModel, Field

# Gets predict function from the predictor.py
from predictor import predict

# Gets get_command function from the interaction_manager.py
from interaction_manager import get_command

# Gets query_answer function from the rag.py
from rag import query_answer

# Gets upload_pdf_file and get_pdf_path function from the pdf_info.py
from pdf_info import upload_pdf_file, get_pdf_path

from fastapi.middleware.cors import CORSMiddleware


# Runs the server
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Motion data in specific format
class MotionData(BaseModel):
    x_velocity: float
    y_velocity: float

    x_direction: str
    y_direction: str

    pinch_distance: float
    pinch_velocity: float

# App state in specific format
class AppState(BaseModel):

    mode: str
    num_act: bool

# Frame data in specific format
class FrameRequest(BaseModel):

    # Avoids unecessary errors
    features: list[float]=Field(
    min_length=63,
    max_length=63
    )
    motion: MotionData
    state: AppState


# Query data in specific format
class QueryRequest(BaseModel):

    pdf_id: str

    llm: str

    ai_model: str
    api_key: str

    page_range: bool
    page_start: int
    page_end: int

    query: str


# When called (initiated)
@app.get("/")
def home():

    return {
        "message": "Welcome to EffectiVision Backend!"
    }

# For checking if the app works
@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    result = await upload_pdf_file(file)

    return {
        "success": result["success"],
        "pdf_id": result["pdf_id"],
        "filename": result["filename"]
    }


# Getting the info from the frontend
@app.post("/process_frame")
def process_frame(data: FrameRequest):

    prediction = predict(data.features, data.state.mode)

    command = get_command(
        prediction["gesture"],
        {
            "x_direction": data.motion.x_direction,
            "y_direction": data.motion.y_direction,
            "x_velocity": data.motion.x_velocity,
            "y_velocity": data.motion.y_velocity,
            "pinch_distance": data.motion.pinch_distance,
            "pinch_velocity": data.motion.pinch_velocity
        },
        data.state.mode,
        data.state.num_act
    )

    return {
        "success": True,
        "gesture": prediction["gesture"],
        "confidence": prediction["confidence"],

        "command": command,
        "mode": data.state.mode,

        "motion": {
            "x_velocity": data.motion.x_velocity,
            "y_velocity": data.motion.y_velocity,
            "x_direction": data.motion.x_direction,
            "y_direction": data.motion.y_direction,
            "pinch_distance": data.motion.pinch_distance,
            "pinch_velocity": data.motion.pinch_velocity
        }
    }



# Getting the query from the frontend
@app.post("/query")
def process_query(data: QueryRequest):

    pdf_path = get_pdf_path(data.pdf_id)

    answer = query_answer(

        pdf_path,

        data.llm,
        data.ai_model,
        data.api_key,

        data.page_range,
        data.page_start,
        data.page_end,

        data.query
    )

    return {

        "success": True,

        "rel_pages": answer["rel_pages"],

        "answer": answer["answer"],

        "error": answer["error"]

    }
