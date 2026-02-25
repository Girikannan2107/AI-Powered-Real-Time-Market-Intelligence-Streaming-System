import websocket

def on_message(ws, message):
    print("Received:", message)

ws = websocket.WebSocketApp(
    "ws://localhost:8000/ws",
    on_message=on_message
)

ws.run_forever()