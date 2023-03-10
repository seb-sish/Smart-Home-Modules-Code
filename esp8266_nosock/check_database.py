import uasyncio as asyncio
from firebase import Firebase
from data_parser import parser

parser = parser()
class Database(Firebase):
    def __init__(self, config, email, password):
        self.email = email
        self.password = password

        super().__init__(config)

    def start(self):
        self.auth = self.auth()
        self.user = self.auth.sign_in_with_email_and_password(self.email, self.password)
        self.db = self.database()
        self.loop = asyncio.new_event_loop()
        self.task = self.loop.create_task(self.check_database())
        self.loop.run_forever()

    def stop(self):
        asyncio.run_until_complete(self.stopper())  

    async def stopper(self):
        self.check_task.cancel()
        try: await self.check_task
        except asyncio.CancelledError: pass
        self.loop.close()

    async def get_temp_from_db(self, temperature_module):
        temp = self.db.child("users").child(self.user["localId"]).child("modules").child(temperature_module).child("temperature").get(self.user["idToken"])
        return temp
    async def get_hum_from_db(self, humidity_module):
        hum = self.db.child("users").child(self.user["localId"]).child("modules").child(humidity_module).child("humidity").get(self.user["idToken"])
        return hum

    async def get_module_state_from_db(self, socket_module):
        state = self.db.child("users").child(self.user["localId"]).child("modules").child(socket_module).child("enabled").get(self.user["idToken"])
        return state

    async def set_module_state(self, socket_module, state):
        self.db.child("users").child(self.user["localId"]).child("modules").child(socket_module).update({"enabled": state}, self.user["idToken"])

    async def check_database(self):
        while True:
            try:
                scenarios = self.db.child("users").child(self.user["localId"]).child("scenarios").get(self.user["idToken"])
                for scenario in scenarios[1:]:
                    print(scenario)
                    if scenario['enabled']:
                        if scenario['indicator'] == "temperature":
                            temp = await self.get_temp_from_db(scenario['temperature_module'])
                            if scenario['condition'] == "<":
                                if temp < scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])
                            elif scenario['condition'] == ">":
                                if temp > scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])
                            elif scenario['condition'] == "=":
                                if temp == scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])
                            elif scenario['condition'] == ">=":
                                if temp >= scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])
                            elif scenario['condition'] == "<=":   
                                if temp <= scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])

                        elif scenario['indicator'] == "humidity":
                            hum = await self.get_hum_from_db(scenario['temperature_module'])
                            if scenario['condition'] == "<":
                                if hum < scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])
                            elif scenario['condition'] == ">":
                                if hum > scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])
                            elif scenario['condition'] == "=":
                                if hum == scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])
                            elif scenario['condition'] == ">=":
                                if hum >= scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])
                            elif scenario['condition'] == "<=":   
                                if hum <= scenario['threshold_temperature']:
                                    if await self.get_module_state_from_db(scenario['socket_module']) != scenario['action']:
                                        await self.set_module_state(scenario['socket_module'], scenario['action'])                    
                        
                    await asyncio.sleep(1)
            except:
                print("Trouble with connect to db")
                await asyncio.sleep(5)

if __name__ == "__main__":
    config = {
        "apiKey": "AIzaSyC8goB9QvkspCrsJ8BN7JkYyblUsUAgqPk",
        "authDomain": "smart-home-project-db.firebaseapp.com",
        "databaseURL": "https://smart-home-project-db-default-rtdb.europe-west1.firebasedatabase.app",
        "storageBucket": "smart-home-project-db.appspot.com"
    };
    db = Database(config,  *parser.get_firebase_user_data())
    db.start()