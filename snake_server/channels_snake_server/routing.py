from channels import route

from channels_snake_server.consumers import ws_add, ws_disconnect, ws_message

channel_routing = [
     route("websocket.connect", ws_add),
     route("websocket.receive", ws_message),
     route("websocket.disconnect", ws_disconnect),
]