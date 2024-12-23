from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello https "}

@app.post("/")
async def create_item():
    return {"message": "Helloss"}

@app.put("/")
async def update_item():
    return {"message": "Helloss"}

@app.delete("/")
async def delete_item():
    return {"message": "Helloss"}
