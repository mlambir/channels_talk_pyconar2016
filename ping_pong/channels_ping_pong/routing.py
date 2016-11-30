from channels.routing import route

channel_routing = [
    route("websocket.receive", "main.consumers.ws_message"),
]