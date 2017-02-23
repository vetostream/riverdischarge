from channels.routing import route
from rdmsystem.consumers import reading_connect, reading_message, reading_disconnect

# channel_routing = [
# 	route('websocket.connect', ws_connect),
# 	route('websocket.receive',ws_message),
# 	route('websocket.disconnect', ws_disconnect),
# ]

# device_websocket = [
# 	route("websocket.connect",device_connect),
# 	route("websocket.receive",device_message),
# 	route("websocket.disconnect",device_disconnect)
# ]

reading_websocket = [
	route("websocket.connect",reading_connect),
	route("websocket.receive",reading_message),
	route("websocket.disconnect",reading_disconnect)
]