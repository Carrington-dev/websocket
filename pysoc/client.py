import websocket

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws):
    print("Disconnected from the WebSocket server")

def on_open(ws):
    print("Connected to the WebSocket server")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:6789",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
