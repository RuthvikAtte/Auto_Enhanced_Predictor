import json
import pandas as pd
import requests
import threading
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# dict1 = {}


# # Global var storing df with all information
# all_info_df = get_dataFrame("Classes.json")


# def title_check(className):
#     df = pd.read_csv("Dicts.csv")
#     info = all_info_df.iloc[df[className][0]]
#     return info["sections"][0]["openStatusText"]


# def print_subjects():
#     title = all_info_df["title"]
#     title.to_csv("Subjects.csv", index=False)


# def get_OpenStatus(cnKey):
#     return cnKey["sections"][0]["openStatusText"]
class APIError(Exception):
    """Exception raised for errors in the API call.

    Attributes:
        status_code -- HTTP status code returned by the API
        message -- explanation of the error
    """

    def __init__(self, message="API request failed"):
        # self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f" {self.message}"


class Sniper:
    # def get_dataFrame(self, Jfile):
    #     # file = open(Jfile, "r")
    #     # parsedR = json.loads(file.read())
    #     # df = pd.json_normalize(parsedR)

    #     # df.to_csv("Classes.csv")
    #     return df

    def createClassesJson(self):
        response = requests.get(
            "https://classes.rutgers.edu/soc/api/courses.json?year=2024&term=9&campus=NB"
        )

        if response.status_code == 200:
            # Request was successful
            data1 = response.json()
            # Parse and use the data as needed
        else:
            # Request failed
            print(f"Request failed with status code: {response.status_code}")

        data1 = response.json()
        # with open("Classes.json", "w") as f:
        #     json.dump(data1, f, ensure_ascii=False, indent=4)
        df = pd.json_normalize(data1)
        df.to_csv("Classes")
        return df

    # finish this method later and add it to the constructor
    def createDicts(self):
        # with open("dicts.txt", "w") as file:
        dict1 = {}
        # self.master_df = self.get_dataFrame(classes)
        titles = self.master_df["title"]
        count = 0
        for x in titles:
            dict1[x] = count
            # file.write(str(x) + ": " + str(count) + "\n")
            count = count + 1
        json_string = json.dumps(dict1)
        # with open("my_data.json", "w") as f:
        #     f.write(json_string)
        return dict1

    def getIndexClasses(self):
        indexToClass = {}
        for titles in self.master_df["title"]:
            try:
                count = 0
                for sections in self.getilocTitle(titles)["sections"]:
                    indexToClass[sections["index"]] = [titles, count]
                    count += 1
                    # print(str(titles) + ": " + str(sections["index"]))

            except:
                # raise IndexError("Class: " + titles + " is not avaiable check getindexClasses method")
                pass
        json_string = json.dumps(indexToClass)
        # with open("indexToClass.json", "w") as f:
        #     f.write(json_string)
        return indexToClass

    def __init__(self):
        self.master_df = self.createClassesJson()
        self.dicts = self.createDicts()
        self.indexClasses = self.getIndexClasses()
        self.runningSnipes = {}
        # ilocNum = self.dicts[str(title).upper()]
        # self.course = self.master_df.iloc[ilocNum]

    def getilocTitle(self, title):
        return self.master_df.iloc[self.dicts[str(title).upper()]]

    def jsonToList(self, Jfile):
        with open(Jfile, "r") as f:
            content = f.read()

        data = json.loads(content)
        my_list = list(data)
        return my_list

    def binary_search(self, arr, target):
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return True
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return False

    def get_numSections(self):
        return len(self.course["sections"])

    def get_OpenSections(self):
        return self.course["openSections"]

    def get_code(self):
        return self.course["coreCodes"]["coreCode"]

    def get_credits(self):
        return self.course["credits"]

    def get_main_Campus(self):
        return self.course["mainCampus"]

    def get_preReqNotes(self):
        return self.course["preReqNotes"]

    def printInformation(self):
        string = (
            "Number of Sections: "
            + str(self.get_numSections())
            + "\n"
            + "Number of Open Sections: "
            + str(self.get_OpenSections())
            + "\n"
            + "Number of credits: "
            + str(self.get_credits())
            + "\n"
            + "Campus: "
            + self.get_main_Campus()
            + "\n"
            + "Pre Req Notes: "
            + self.get_preReqNotes()
        )
        print(string)

        # Section layer

    def get_Sections(self):
        return self.course["sections"]

    def printAllSections(self):
        string = ""
        for i in self.get_Sections():
            string += (
                str(i["number"])
                + "\n"
                + i["index"]
                + "\n"
                # + str(i["openStatus"])
                # + "\n"
                + i["instructorsText"]
                + "\n\n\n"
            )
            # times = ""
            # for t in i["meetingTimes"]:
            #     string += ()
        print(string)

    def checkSectionAva(self, openSections, indexnum):
        opens = self.jsonToList(openSections)
        return self.binary_search(opens, indexnum)

    def checkSectionAva(self, jsonIndexes, indexnum):
        opens = jsonIndexes
        return self.binary_search(opens, indexnum)

    def callOpenSections(self):
        for x in range(10):
            try:
                response = requests.get(
                    "https://classes.rutgers.edu/soc/api/openSections.json?year=2024&term=9&campus=NB"
                )
                if response.text:
                    if response.status_code == 200:
                        # Request was successful
                        data1 = response.json()
                        return data1
                        # Parse and use the data as needed
                    else:
                        raise APIError(
                            f"JSON STATUS {response.status_code} Date and Time: {str(datetime.datetime.now())}"
                        )
                else:
                    print(f"RESPONSE: {response.text} DUE TO THE Response.text and API")
                    return False

            except:
                # during UTC 9:45:00 the API returns Status code 500 or 503 showing it is shut down for manintance. Once the API sends status 500
                # we wait for 5 seconds and try again with time.sleep(5) and this loop runs 10 times just to give the API some time to get back up.
                # Request failed
                # print(
                #     f"Request failed
                #     status code: {response.status_code} Date and Time: {str(datetime.datetime.now())} \n requesting again..."
                # )
                time.sleep(5)

        raise APIError(
            f"FINIAL JSON STATUS {response.status_code} APPLICATION CRASH DUE TO API PROBLEM Date and Time: {str(datetime.datetime.now())}"
        )
        # raise ("APPLICATION CRASH DUE TO API PROBLEM")

    def runSnipe(self, index, event: threading.Event):
        infodict = self.getinfoBasedonIndex(index)
        data1 = self.callOpenSections()
        while not self.checkSectionAva(data1, index):
            # print(index)
            time.sleep(0.05)
            if event.is_set():
                print("The thread was stopped prematurely.")
                return
            data1 = self.callOpenSections()

        print("Section " + str(index) + " OPENED")
        del self.runningSnipes[index]
        self.sendEmail(
            f" {self.indexClasses[index][0]} INDEX: {index} has OPENED",
            f"Click the link https://sims.rutgers.edu/webreg/editSchedule.htm and input {index} to sign up for the class\n Class: {self.indexClasses[index][0]} \n Section: {str(infodict['number'])} \n Instructors: {str(infodict['instructorsText'])}",
        )
        return

    def getinfoBasedonIndex(self, index):
        info = self.getilocTitle(self.indexClasses[index][0])["sections"][
            self.indexClasses[index][1]
        ]
        return info

    def addSnipe(self, index):
        # list_indexes = str(index).split(" ")
        list_indexes = index
        str_info = ""
        for i in list_indexes:
            if i not in self.runningSnipes.keys():
                event = threading.Event()
                self.runningSnipes[i] = [
                    threading.Thread(
                        target=self.runSnipe,
                        args=(
                            i,
                            event,
                        ),
                    ).start(),
                    event,
                ]
                # print("Successfully added index: " + str(i))
                info = self.getinfoBasedonIndex(i)
                str_info += f"Index: {i} \n Section: {str(info['number'])} \n Class: {self.indexClasses[i][0]} \n Professor: {info['instructorsText']} \n\n"
            else:
                print("Already Sniping Index: " + str(i))

        self.sendEmail(
            f"INDEXES ADDED",
            f"These are the Classes added to your Snipe List \n\n {str_info}",
        )

    def deleteSnipe(self, index):
        if index in self.runningSnipes.keys():
            self.runningSnipes[index][1].set()
            del self.runningSnipes[index]
            return True
        else:
            print("Index has not been set up yet")
            return False

    def showRunningSnipes(self):
        return self.runningSnipes.keys()

    def setEmail(self, sendergmail, emailpassword, emailrecievers):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        # email_password = "woff flkn kgyu dwre"
        self.email_password = emailpassword  # It's safer to use environment variables or input for credentials
        # self.sender_email = "rutgersnbsniper@gmail.com"
        self.receiver_email = emailrecievers
        self.sender_email = sendergmail

    def sendEmail(self, subject, text):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = ""
        message["Subject"] = subject
        body = text
        message.attach(MIMEText(body, "plain"))
        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure the connection
            server.login(self.sender_email, self.email_password)  # Log in to the server
            text = message.as_string()
            server.sendmail(self.sender_email, self.receiver_email, text)
            # print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()

    def getNumThreads(self):
        return threading.active_count()


sniper = Sniper()
# dicts1 = pd.read_csv("Dicts.csv")
# num = dicts1["DATA STRUCTURES"]

# df = pd.read_csv("Classes.csv")
# # print(df["title"])

# run_status1 = True
# run_status2 = True

# event1 = threading.Event()
# event2 = threading.Event()


# sniper = Sniper()
# sniper.addSnipe("07474")
# sniper.addSnipe("07475")
# sniper.addSnipe("05957")
# time.sleep(3)
# sniper.deleteSnipe("07474")
# sniper.getinfoBasedonIndex("07475")
# t = threading.Thread(
#     target=sniper.runSnipe,
#     args=(
#         "07474",
#         event1,
#     ),
# )
# t.start()


# t2 = threading.Thread(
#     target=sniper.runSnipe,
#     args=(
#         "07475",
#         event2,
#     ),
# )
# t2.start()


# time.sleep(3)

# event1.set()

# time.sleep(2)

# event2.set()

# sniper.runSnipe("07475")
# print(sniper.master_df.iloc[sniper.dicts["DATA STRUCTURES"]]["sections"][0]["index"])
# sniper.printAllSections()
# # print(sniper.runSnipe("05959"))
# sniper.getIndexClasses()
# print(indexes["07474"])
# count = 0
# while True:
#     response = requests.get(
#         "https://classes.rutgers.edu/soc/api/openSections.json?year=2024&term=9&campus=NB"
#     )

#     if response.status_code == 200:
#         # Request was successful
#         data1 = response.json()
#         # Parse and use the data as needed
#     else:
#         # Request failed
#         print(f"Request failed with status code: {response.status_code}")
#     print(str(sniper.checkSectionAva(data1, "23889")) + " " + str(count))
#     count += 1


# print(sniper.get_numSections())
# titles = df["title"]
# sections = df["sections"]

# count = 0
# for x in titles:
#     dict1[x] = count
#     count = count + 1

# with open("Dictonaries.json", "w") as f:
#     json.dump(dict1, f)
# print(title_check("BIBLE IN ARAMAIC"))


# print(type(df))
# print(df[0][0]["openStatusText"])
# print(df.to_frame())
# print(df.iloc[0][0]["openStatusText"])
# print(check_Ava(""))
# print_subjects()
# print(df.to_csv("output2.csv", index=False))
# print(["openStatusText"])
# print()
# print()

# df.to_csv("output.csv", index=False)


# Running this code shows me that pandas is over all faster and on average by almost +.00005
# sum_pandas = 0
# sum_polars = 0
# for i in range(1000):
#     t0 = time.time()
#     df.iloc[-1]
#     t1 = time.time() - t0
#     sum_pandas += t1

#     t3 = time.time()
#     df_pl.row(-1)
#     t2 = time.time() - t3
#     sum_polars += t2

# avg_pandas = sum_pandas / 1000
# avg_polars = sum_polars / 1000

# print(avg_pandas)
# print(avg_polars)
