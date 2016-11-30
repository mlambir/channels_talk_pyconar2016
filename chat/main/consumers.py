from channels import Group

# websocket.connect
def ws_add(message):
    Group("chat").add(message.reply_channel)

# websocket.receive
def ws_message(message):
    Group("chat").send({
        "text": message.content['text'],
    })

# websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)