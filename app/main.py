from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import sys
import os
from routes import oders,product
# Setting enviornment. Default is Test
if len(sys.argv)==2 and sys.argv[1]=="prod":
    os.environ["db_env"]="prod"

from database.db import init_db
# Code to run on startup and shutdown
@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield
    print("Shut Down")

app=FastAPI(title="E-Comerce",lifespan=lifespan)


app.include_router(oders.router,prefix="/oders",tags=["oders"])
app.include_router(product.router,prefix="/products",tags=["products"])

if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)