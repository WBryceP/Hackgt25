from fastapi import FastAPI

app = FastAPI(title="Backend Research API", version="1.0.0")


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Backend Research API", "version": "1.0.0"}
