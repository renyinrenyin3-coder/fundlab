from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .models import Holding

app = FastAPI(title="FundLab")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

class HoldingIn(BaseModel):
    code: str = Field(...)
    name: str = Field(...)
    units: float = Field(..., gt=0)
    cost: float = Field(..., gt=0)

def get_db() -> Session:
    return SessionLocal()

@app.post("/api/portfolio/add")
def add_holding(h: HoldingIn):
    db = get_db()
    try:
        row = Holding(
            code=h.code.strip(),
            name=h.name.strip(),
            units=h.units,
            cost=h.cost
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return {"ok": True, "id": row.id}
    finally:
        db.close()

@app.get("/api/portfolio/list")
def list_holdings():
    db = get_db()
    try:
        rows = db.query(Holding).all()
        return rows
    finally:
        db.close()

@app.get("/api/portfolio/summary")
def summary():
    db = get_db()
    try:
        rows = db.query(Holding).all()
        total = sum(r.cost for r in rows)

        items = []
        for r in rows:
            price = 1.0
            value = r.units * price
            pnl = value - r.cost

            items.append({
                "code": r.code,
                "name": r.name,
                "units": r.units,
                "cost": r.cost,
                "value": value,
                "pnl": pnl
            })

        return {
            "count": len(items),
            "total_cost": total,
            "items": items
        }
    finally:
        db.close()
