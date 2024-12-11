import websocket, json, pprint, talib
import numpy as np
from newton_api_wrapper.newton_wrapper import newton_wrapper as nt
from config import CLIENT_ID, SECRET_KEY

# Enable WebSocket debugging logs
# websocket.enableTrace(True)
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSDT"
TRADE_QUANTITY = 0.05
closes = []
in_position = False

def on_open(ws):
    print("Opened connection.")

def on_close(ws):
    print("Closed connection.")

def on_message(ws, message):
    global closes
    #print("Received message:")
    json_message = json.loads(message)
    #pprint.pprint(json_message)
    candle = json_message['k']
    print(candle)

    candle_closed = candle['x']
    close = candle['c']

    if candle_closed:
        print(f"candle closed at {close}")
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("All RSIs calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print(f"The current rsi is {last_rsi}")
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("sell")
                    # Sell logic here
                else:
                    print("Do not own any eth, cannot sell")
            elif last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("in position, cannot buy")
                else:
                    print("buy")
                    # Buy logic here

ws = websocket.WebSocketApp(SOCKET, 
                            on_open=on_open, 
                            on_close=on_close, 
                            on_message=on_message)
ws.run_forever()
