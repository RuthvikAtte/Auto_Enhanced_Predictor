# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
import pandas as pd
import json
import requests
import time
import threading
import datetime

start_time1 = time.time()
response = requests.get(
    "https://classes.rutgers.edu/soc/api/courses.json?year=2024&term=9&campus=NB"
)
if response.status_code == 200:
    # Request was successful
    data1 = response.json()
    df = pd.json_normalize(data1)
    df["title"]
    print("done1")
    # Parse and use the data as needed
else:
    # Request failed
    print(f"Request failed with status code: {response.status_code}")
end_time1 = time.time()

elp = end_time1 - start_time1
print(f"JSON {elp}")


start_time = time.time()
df = pd.read_csv("classes.csv")
df["title"]
print("done2")
end_time = time.time()
elp = end_time - start_time
print(f"CSV {elp}")
# with open("classes.csv")

# df = pd.json_normalize(data1)
# df = df["title"]

# with open("Titles.txt", "w") as f:
#     for x in df:
#         f.write(f"{str(x)}\n")

#     return True
# while True:
#     time.sleep(1)
#     try:
#         response = requests.get("http://localhost:8080/testing")
#         if response.status_code == 200:
#             # Request was successful
#             data1 = response.json()
#             print("STATUS SUCCESS")
#             # Parse and use the data as needed
#         else:
#             exec("THROWING EXEC")
#     except:
#         # Request failed
#         print("EXECPTING")
#         print(f"Request failed with status code: {response.status_code}")
# print(f"Date and Time: {datetime.datetime.now()}")
