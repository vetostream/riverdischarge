from channels import include

channel_routing = [
	include("rdmsystem.routing.device_websocket", path=r"^/chdevice"),
	include("rdmsystem.routing.reading_websocket", path=r"^/chreading"),
]