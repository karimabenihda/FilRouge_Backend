from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):

    print("Request received:", request.url)

    response = await call_next(request)

    print("Response status:", response.status_code)

    return response