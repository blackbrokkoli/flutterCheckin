import logging
from json import dumps as jsonify
from json import loads as dejsonify
from datetime import datetime
from websocket_server import WebsocketServer

class OfficeCheckWebsocketServer(WebsocketServer):
    def __init__(self, host='127.0.0.1', port=12345, loglevel=logging.INFO, key=None, cert=None):
        super().__init__(host, port, loglevel, key, cert)
        super().set_fn_new_client(self.on_new_client)
        super().set_fn_client_left(self.on_client_left)
        super().set_fn_message_received(self.on_message_received)
        self.open = False
        self.name = "Anonym"
        self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def on_new_client(self, client, server):
        data = {
            "msg": f"New client joined: {client['id']}",
            "open": self.open,
            "name": self.name,
            "dati": self.datetime
        }
        server.send_message_to_all(jsonify(data))
        logging.info(f"New client joined: #{client['id']}")

    def on_client_left(self, client, server):
        data = {
            "msg": f"Client left: {client['id']}",
            "open": self.open,
            "name": self.name,
            "dati": self.datetime
        }
        server.send_message_to_all(jsonify(data))
        logging.info(f"Client left: #{client['id']}")

    def on_message_received(self, client, server, message):
        data = dejsonify(message)
        if data['open'] == 'True' or data['open'] == 'False':
            self.open = (data['open'] == 'True')
            if data['name']:
                self.name = data['name']
            else:
                self.name = "Anonym"
            self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "msg": f"{client['id']} said: {message}",
            "open": self.open,
            "name": self.name,
            "dati": self.datetime
        }
        server.send_message_to_all(jsonify(data))
        logging.info(f"Client #{client['id']}: {message}")

logging.getLogger().setLevel(logging.DEBUG)
server = OfficeCheckWebsocketServer(host='127.0.0.1', port=12345, loglevel=logging.INFO)
server.run_forever()
