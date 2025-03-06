from fastapi import FastAPI
import uvicorn
from typing import Dict

app = FastAPI()

@app.get("/", response_model=Dict[str, str])
async def read_root() -> Dict[str, str]:
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
