from data_parser import parser
import internet
import time
import gc

module_info = {"type": "temperature_module", "id": "kTBPnkp49inug3K4"}

config = {
    "apiKey": "AIzaSyC8goB9QvkspCrsJ8BN7JkYyblUsUAgqPk",
    "authDomain": "smart-home-project-db.firebaseapp.com",
    "databaseURL": "https://smart-home-project-db-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "smart-home-project-db.appspot.com"
};
parser = parser()

if parser.get_connected_ssid_data()[0] == "":
    internet.point_activate()
    print('Access point startup')

    from server import Server
    server = Server()
    server.start_server()

time.sleep(1) 
connect_data = internet.wlan_activate()
if(connect_data):
    print(connect_data)
    print('Success startup')
    time.sleep(1) 

    internet.point_deactivate()
    gc.collect()
    time.sleep(3)   
    
    from check_database_temp import Database
    db = Database(config, module_info, *parser.get_firebase_user_data())
    db.start()

else:
    print("error on connecting...")
    internet.point_activate()
    print('Access point startup')

    from server import Server
    server = Server()
    server.start_server()

