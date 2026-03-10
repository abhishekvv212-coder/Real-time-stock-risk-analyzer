from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.cache import get_cached, set_cache
from db.connection import get_db, engine, Base
from db.models import Stock
import yfinance as yf

load_dotenv()

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Risk Analyzer")

@app.get("/")
def health_check():
    return {"status": "running", "version": "1.0"}

@app.get("/stock/{symbol}")
def get_stock(symbol: str, db: Session = Depends(get_db)):
    key = f"stock:{symbol.upper()}"

    # 1 — Check Redis cache first
    cached = get_cached(key)
    if cached:
        cached["source"] = "CACHE ⚡"
        return cached

    # 2 — Fetch from Yahoo Finance
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info

        # Reject invalid symbols
        if not info or (info.get("currentPrice") is None and info.get("regularMarketPrice") is None):
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

        data = {
            "symbol": symbol.upper(),
            "company": info.get("longName", "N/A"),
            "price": info.get("currentPrice", 0.0),
            "currency": info.get("currency", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "52w_high": info.get("fiftyTwoWeekHigh", 0.0),
            "52w_low": info.get("fiftyTwoWeekLow", 0.0),
            "pe_ratio": info.get("trailingPE", 0.0),
            "source": "LIVE 🌐"
        }

        # 3 — Save to PostgreSQL
        stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
        if stock:
            stock.price = data["price"]
            stock.market_cap = data["market_cap"]
            stock.pe_ratio = data["pe_ratio"]
        else:
            stock = Stock(
                symbol=data["symbol"],
                company=data["company"],
                price=data["price"],
                currency=data["currency"],
                market_cap=data["market_cap"],
                high_52w=data["52w_high"],
                low_52w=data["52w_low"],
                pe_ratio=data["pe_ratio"],
            )
            db.add(stock)
        db.commit()

        # 4 — Save to Redis cache
        set_cache(key, data, ttl=60)
        return data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

@app.get("/stocks/saved")
def get_saved_stocks(db: Session = Depends(get_db)):
    stocks = db.query(Stock).all()
    return [
        {
            "symbol": s.symbol,
            "company": s.company,
            "price": s.price,
            "updated_at": str(s.updated_at)
        }
        for s in stocks
    ]