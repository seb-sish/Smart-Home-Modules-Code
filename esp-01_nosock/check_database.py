import uasyncio as asyncio
from firebase import Firebase
from data_parser import parser
from machine import Pin
parser = parser()
class Database(Firebase):
    state = False
    relay = Pin(0, Pin.OUT, value=0)

    def __init__(self, config, module_info, email, password):
        self.email = email
        self.password = password

        self.module_type = module_info['type']
        self.module_id = module_info['id']

        super().__init__(config)

    def start(self):
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


    async def check_database(self):
        self.auth = self.auth()
        self.user = self.auth.sign_in_with_email_and_password(self.email, self.password)
        self.db = self.database()
        while True:
            try:
                data = self.db.child("users").child(self.user["localId"]).child("modules").child(self.module_id).get(self.user["idToken"])
                if data['enabled'] != self.state:
                    self.state = data['enabled']
                    print(self.state)
                    if self.state is True: 
                        print("on")
                        self.relay.off()
                    else: 
                        print("off")
                        self.relay.on()
                    # if self.state: self.relay.on()
                    # else: self.relay.off()
                    
                await asyncio.sleep(0.15)
            except:
                print("Trouble with connect to db")
                await asyncio.sleep(5)

if __name__ == "__main__":
    module_info = {"type": "socket_module", "id": "b87c95385a5d935f"}
    config = {
        "apiKey": "AIzaSyC8goB9QvkspCrsJ8BN7JkYyblUsUAgqPk",
        "authDomain": "smart-home-project-db.firebaseapp.com",
        "databaseURL": "https://smart-home-project-db-default-rtdb.europe-west1.firebasedatabase.app",
        "storageBucket": "smart-home-project-db.appspot.com"
    };
    db = Database(config, module_info,  *parser.get_firebase_user_data())
    db.start()