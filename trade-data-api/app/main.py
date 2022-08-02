import logging
from fastapi import FastAPI, HTTPException, WebSocket
from starlette.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi_utils.tasks import repeat_every

from .store import TickerStore
from .connection import TickerConnection

logger = logging.getLogger(__name__)
app = FastAPI()
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ticker_connection = TickerConnection()
ticker_store = TickerStore()


@app.on_event("startup")
@repeat_every(seconds=1, wait_first=True, logger=logger)
async def repeat_update():
    ticker_ids = await ticker_store.get_ticker_ids()
    for ticker_id in ticker_ids:
        ticker_item = await ticker_store.generate_ticker_item(ticker_id)
        if ticker_item:
            await ticker_connection.broadcast_ticker_item(
                ticker_id,
                jsonable_encoder({"ticker_id": ticker_id, "ticker_item": ticker_item}),
            )


@app.on_event("startup")
@repeat_every(seconds=1, logger=logger)
async def repeat_print():
    cur_tickers = await ticker_store.get_cur_tickers()
    print(jsonable_encoder(cur_tickers), "\n")


@app.get("/tickers")
async def get_tickers():
    ticker_ids = await ticker_store.get_ticker_ids()
    return ticker_ids


@app.get("/tickers/{ticker_id}")
async def get_tickers_ticker_id(ticker_id: str):
    ticker = await ticker_store.get_ticker(ticker_id)
    if ticker is None:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return ticker


@app.websocket("/ws")
async def websocket_ws(websocket: WebSocket):
    await ticker_connection.connect(websocket)
    try:
        while True:
            ticker_ids = await websocket.receive_json()
            ticker_connection.update_ticker_subscribes(websocket, ticker_ids)
    except WebSocketDisconnect:
        ticker_connection.disconnect(websocket)
