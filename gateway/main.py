import Router_gateway
from fastapi import FastAPI


app = FastAPI()

app.include_router(Router_gateway.router_gateway)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

