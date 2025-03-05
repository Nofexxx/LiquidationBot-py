from fastapi import FastAPI
import uvicorn
from typing import Dict

app = FastAPI()

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the FastAPI template"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
