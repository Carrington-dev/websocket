import threading
from flask import Flask, request, jsonify
from app import ArbitrageDetector, MarketDataFeed, WebSocketServer

app = Flask(__name__)

@app.route('/config', methods=['POST'])
def config():
    data = request.json
    if 'threshold' in data:
        arbitrage_detector.threshold = data['threshold']
    return jsonify({'status': 'success'}), 200

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({'threshold': arbitrage_detector.threshold}), 200

if __name__ == '__main__':
    data_feed = MarketDataFeed()
    arbitrage_detector = ArbitrageDetector(threshold=0.001)

    # Start the market data feed generator
    data_thread = threading.Thread(target=data_feed.generate_data)
    data_thread.start()

    # Start the WebSocket server
    ws_server = WebSocketServer(data_feed, arbitrage_detector)
    ws_thread = threading.Thread(target=ws_server.start)
    ws_thread.start()
    app.run(port=5000)
