from fastapi import FastAPI

app = FastAPI(title="FundLab")

@app.get("/health")
def health():
    return {"ok": True}
