import router_auth
from fastapi import FastAPI

app = FastAPI()

app.include_router(router_auth.router_auth)


@app.get("/")
def index():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)    