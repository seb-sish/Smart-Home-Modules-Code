from firebase import Firebase
from data_parser import parser
from machine import Pin
try:
    import dht
    import uasyncio as asyncio
except:
    import asyncio as asyncio
    import random

module_info = {"type": "temperature_module", "id": "kTBPnkp49inug3K4"}

parser = parser()

class Database(Firebase):
    try:
        sensor = dht.DHT11(Pin(2))
    except:
        pass

    def __init__(self, config, module_info, email, password):
        self.email = email
        self.password = password

        self.module_type = module_info['type']
        self.module_id = module_info['id']

        super().__init__(config)

    def start(self):
        self.loop = asyncio.new_event_loop()
        self.task = self.loop.create_task(self.update_database())
        self.loop.run_forever()

    def stop(self):
        asyncio.run_until_complete(self.stopper())  

    async def stopper(self):
        self.check_task.cancel()
        try: await self.check_task
        except asyncio.CancelledError: pass
        self.loop.close()

    async def get_temp(self):
        try:
            self.sensor.measure()
            temp = self.sensor.temperature()
            hum = self.sensor.humidity()
            temp_f = temp * (9/5) + 32.0
        except:
            temp = random.randint(-30, 30)
            hum = random.randint(10, 100)
            temp_f = temp * (9/5) + 32.0
        return {"temperature": temp, "temperature_f": temp_f, "humidity": hum}
        # except OSError:
        #     return {"error": 'Неисправность датчика температуры и влажности!'}

    async def update_database(self):
        self.auth = self.auth()
        self.user = self.auth.sign_in_with_email_and_password(self.email, self.password)
        self.db = self.database()
        while True:
            try:
                data = self.db.child("users").child(self.user["localId"]).child("modules").child(self.module_id).update(await self.get_temp(), self.user["idToken"])
                await asyncio.sleep(5)
            except:
                print("Trouble with connect to db")
                await asyncio.sleep(5)

if __name__ == "__main__":
    module_info = {"type": "temperature_module", "id": "kTBPnkp49inug3K4"}
    config = {
        "apiKey": "AIzaSyC8goB9QvkspCrsJ8BN7JkYyblUsUAgqPk",
        "authDomain": "smart-home-project-db.firebaseapp.com",
        "databaseURL": "https://smart-home-project-db-default-rtdb.europe-west1.firebasedatabase.app",
        "storageBucket": "smart-home-project-db.appspot.com"
    };
    db = Database(config, module_info,  *parser.get_firebase_user_data())
    db.start()
