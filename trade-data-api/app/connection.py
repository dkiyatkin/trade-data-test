from fastapi import WebSocket


class TickerConnection:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.ticker_subscribers = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        websocket_index = self.active_connections.index(websocket)
        self.ticker_subscribers.pop(websocket_index, None)
        self.active_connections.remove(websocket)

    async def broadcast_ticker_item(self, ticker_id: str, ticker_item):
        for websocket_index in list(self.ticker_subscribers):
            if ticker_id in self.ticker_subscribers[websocket_index]:
                await self.active_connections[websocket_index].send_json(ticker_item)

    def update_ticker_subscribes(self, websocket: WebSocket, ticker_ids):
        websocket_index = self.active_connections.index(websocket)
        self.ticker_subscribers[websocket_index] = ticker_ids
