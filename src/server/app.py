from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union, Dict, Any
from datetime import datetime, timedelta
import uvicorn
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database import get_db, engine, Base
from models import JSONData
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
   
    await engine.dispose()

app = FastAPI(
    title="Python JSON Server",
    description="HTTP fastAPI server for JSON data",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Модели данных
class DataRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="JSON data")

   

class DataResponse(BaseModel):
    message: str
    processed_at: str
    status: str


class ErrorResponse(BaseModel):
    error: str
    status: str


@app.get("/", response_model=Dict[str, str])
async def home():
    return {
        "message": "Server is running",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }


@app.post("/api/data", response_model=DataResponse)
async def receive_data(data: DataRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Сохранить данные в бд
        json_data = JSONData(data=json.dumps(data.data))
        db.add(json_data)
        await db.commit()
        await db.refresh(json_data)
        #убрать обертку
        # Очистить старые данные
        two_days_ago = datetime.now() - timedelta(days=2)
        await db.execute(
            delete(JSONData).where(JSONData.created_at < two_days_ago)
        )
        await db.commit()

        response = {
            "message": "Data received successfully",
            "processed_at": datetime.now().isoformat(), 
            "status": "success"
        }
        return response
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing data: {str(e)}"
        )

# все данные
@app.get("/api/data", response_model=List[Dict[str, Any]])
async def get_all_data(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(JSONData).order_by(JSONData.created_at.desc())
        )
        rows = result.scalars().all()

        return [
            {
                "id": row.id,
                "data": json.loads(row.data),
                "created_at": row.created_at.isoformat()
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving data: {str(e)}"
        )

# info
@app.get("/api/info", response_model=Dict[str, Any])
async def server_info():
    return {
        "server": "Python FastAPI Server",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Main page"},
            {"path": "/api/data", "method": "POST", "description": "receiving JSON data"},
            {"path": "/api/data", "method": "GET", "description": "get all stored data"},
            {"path": "/api/info", "method": "GET", "description": "About server"},
            {"path": "/docs", "method": "GET", "description": "Swagger documentation"},
            {"path": "/redoc", "method": "GET", "description": "ReDoc documentation"}
        ],
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

# DELETE by ID
@app.delete("/api/data/{data_id}", response_model=Dict[str, str])
async def delete_data(data_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Checking existence of data
        result = await db.execute(
            select(JSONData).where(JSONData.id == data_id)
        )
        data = result.scalar_one_or_none()
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"Data with ID {data_id} not found"
            )
        
       
        await db.delete(data)
        await db.commit()
        
        return {
            "message": f"Data with ID {data_id} successfully deleted",
            "status": "success"
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting data: {str(e)}"
        )

# DELETE all data
@app.delete("/api/data", response_model=Dict[str, str])
async def delete_all_data(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(delete(JSONData))
        await db.commit()
        
        return {
            "message": "All data successfully deleted",
            "status": "success"
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting data: {str(e)}"
        )

if __name__ == "__main__": #если через fastapi dev app.py запускать то это не выполняется
    print("🚀 Запуск FastAPI сервера...")
    print("📡 Сервер доступен по адресам:")
    print("   Локально: http://127.0.0.1:8000")
    print("   В сети:   http://<ваш_ip>:8000")
    print("📋 Документация:")
    print("   Swagger UI: http://<ваш_ip>:8000/docs")
    print("   ReDoc:      http://<ваш_ip>:8000/redoc")
    print("\n💡 Для остановки сервера нажмите Ctrl+C")
    
    # -
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        limit_concurrency=1000,
        limit_max_requests=10000,
        timeout_keep_alive=120,
        proxy_headers=True,
        server_header=False,
        date_header=False,
    )
