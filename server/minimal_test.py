#!/usr/bin/env python3

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    print("Starting minimal test server...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="debug"
    )
