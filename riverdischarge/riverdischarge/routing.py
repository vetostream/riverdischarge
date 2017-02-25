from channels import include

channel_routing = [
	# include("riverdash.routing.device_websocket", path=r"^/chdevice"),
	include("riverdash.routing.reading_websocket", path=r"^/chreading"),
]