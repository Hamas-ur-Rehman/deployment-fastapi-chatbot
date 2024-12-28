from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from example1 import chain

class QueryInput(BaseModel):
    question: str
    stream: bool = False


app = FastAPI()

app.add_middleware(
    CORSMiddleware
    , allow_origins=["*"]
    , allow_methods=["*"]
    ,allow_headers=["*"]
)

@app.post("/ask")
def handle_question(input: QueryInput): 
    try:
        if input.stream:
            response = chain.stream({"question":input.question})
            return StreamingResponse(response)
        else:
            response = chain.invoke({"question":input.question})
            return JSONResponse(content={"response":response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))