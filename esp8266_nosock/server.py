try: import asyncio
except: import uasyncio as asyncio
import json

config = {
    "apiKey": "AIzaSyC8goB9QvkspCrsJ8BN7JkYyblUsUAgqPk",
    "authDomain": "smart-home-project-db.firebaseapp.com",
    "databaseURL": "https://smart-home-project-db-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "smart-home-project-db.appspot.com"
};

class Server():

    def __init__(self, email, password, host='0.0.0.0', port=45328):
        self.host = host
        self.port = port
        self.email = email
        self.password = password

        self.clients = {}
        self.ip_to_id = {}

    def start_server(self):
        self.loop = asyncio.new_event_loop()
        
        self.loop.create_task(asyncio.start_server(self.accept_conection,
                                                   self.host, self.port))
        print("Server starts on {}".format(self.host+':'+str(self.port)))
        self.loop.run_forever()

    async def accept_conection(self, reader, writer):
        try:
            addr = writer.get_extra_info('peername')
            print('client {} connected'.format(addr[0]))
            writer.write(b'get_data')
            await writer.drain()
            recieved_data = await self.get_response(reader)
            if recieved_data == "Mobile app connection":
                print(recieved_data)
                response = await self.get_response(reader)
                print(response)
                wifi_info = json.loads(response.replace("\'", "\""))
                
                with open("esp8266/config.json", "r") as config:
                    data = json.load(config)
                    data["firebase"]["email"] = wifi_info["firebase"]["email"]
                    data["firebase"]["password"] = wifi_info["firebase"]["password"]

                    data["connected_ssid"]["essid"] = wifi_info["connected_ssid"]["essid"]
                    data["connected_ssid"]["password"] = wifi_info["connected_ssid"]["password"]

                    data["created_ssid"]["essid"] = wifi_info["created_ssid"]["essid"] if wifi_info["created_ssid"]["essid"] != "" else data["created_ssid"]["essid"]
                    data["created_ssid"]["password"] = wifi_info["created_ssid"]["password"] if wifi_info["created_ssid"]["password"] != "" else data["created_ssid"]["password"]
                    print(data)

                    with open("esp8266/config.json", "w") as writeConfig:
                        writeConfig.write(str(data).replace("\'", "\""))
                await self.close(writer)

        except OSError:
            return await self.close(writer)

    async def get_response(self, reader):
        try:
            response = await reader.read(256)
            try:
                response = response.decode('utf-8')
            except AttributeError:
                raise OSError()
            if response:
                return response
            else:
                raise OSError()
        except OSError:
            raise OSError()

    async def send_request(self, writer, data):
        try:
            writer.write(data.encode('utf-8'))
            await writer.drain()
        except OSError:
            raise OSError()
    

    async def close(self, writer):
        addr = writer.get_extra_info('peername')
        print('client {} disconnected'.format(addr[0]))
        writer.close()
        await writer.wait_closed()
        del self.clients[self.ip_to_id[addr[0]]]
        del self.ip_to_id[addr[0]]
        return


if __name__ == "__main__":
    server = Server("test@test.ru", "123QwertY", '0.0.0.0', 45328)
    server.start_server()
