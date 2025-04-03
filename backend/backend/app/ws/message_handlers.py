from fastapi import WebSocket

async def handle_manager_message(data: dict, room_code: str, websocket: WebSocket):
    pass
async def handle_player_message(data: dict, room_code: str, websocket: WebSocket):
    pass