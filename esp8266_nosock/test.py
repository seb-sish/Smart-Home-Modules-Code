
from urllib import response

response = "g"

if response in ("true", "false"):
    print(response)
# import urequests as requests
# import json

# # apiKey = "AIzaSyC8goB9QvkspCrsJ8BN7JkYyblUsUAgqPk";
# # email = "test@test.ru";
# # password = "123QwertY";

# # request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={}".format(apiKey)

# # headers = {"content-type": "application/json; charset=UTF-8"}
# # data = json.dumps({"email": email, "password": password, "returnSecureToken": True})

# # request_object = requests.get("https://google.com")
# # print(request_object)

# # req = requests
# # data = req.get("https://google.com")
# # print(data.text)
# # # req.post()

# def get_user_request_header():
#     post_data = json.dumps({ 'account': 'user_account', 'password': 'password'})
#     request_url = 'http://passport2.makeblock.com/v1/user/login'
#     res = requests.post(request_url, headers = {'content-type': 'application/json'}, data = post_data).json()
#     print(res)

# get_user_request_header()


# # wifi_info = {"connectWifi":"Quiyuib", "connectWifiPass":"43143531", "createWifi":"etretretr", "createWifiPass":""}

# # with open("esp8266/config.json", "r") as config:
# #     data = json.load(config)
# #     # data["firebase"]["email"] = wifi_info["connectWifi"]
# #     # data["firebase"]["password"] = wifi_info["connectWifiPass"]

# #     # data["connected_ssid"]["essid"] = wifi_info["connectWifi"]
# #     # data["connected_ssid"]["password"] = wifi_info["connectWifiPass"]

# #     # data["created_ssid"]["essid"] = wifi_info["createWifi"] if wifi_info["createWifi"] != "" else data["created_ssid"]["essid"]
# #     # data["created_ssid"]["password"] = wifi_info["createWifiPass"] if wifi_info["createWifiPass"] != "" else data["created_ssid"]["password"]
# #     print(data)

# #     with open("esp8266/config.json", "w") as writeConfig:
# #         writeConfig.write(str(data).replace("\'", "\""))
    