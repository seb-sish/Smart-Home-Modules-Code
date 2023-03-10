import json

class parser:
    def __init__(self, file = 'config.json') -> None:  
        with open(file, 'r') as config:
            self.data = json.load(config)
            
    def get_all(self):
        return self.data

    def get_firebase_user_data(self) -> tuple:
        self.firebase_user = self.data["firebase"]

        email = self.firebase_user["email"]
        password = self.firebase_user["password"]

        return (email, password)

    def get_connected_ssid_data(self) -> tuple:
        self.connected_ssid = self.data["connected_ssid"]

        essid = self.connected_ssid["essid"]
        password = self.connected_ssid["password"]

        return (essid, password)


    def get_created_ssid_data(self) -> tuple:
        self.created_ssid = self.data["created_ssid"]

        essid = self.created_ssid["essid"]
        password = self.created_ssid["password"]

        return (essid, password)