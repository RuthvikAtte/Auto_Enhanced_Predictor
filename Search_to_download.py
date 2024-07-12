import os
import pandas as pd


class Search:
    oscommand = ""
    data = ""

    def __init__(self, keyword):
        global oscommand
        oscommand = keyword
        command = "kaggle datasets list -s " + oscommand + "> output.txt"
        os.system(command)

    def get_pandas_df(self):
        data = ""
        with open("output.txt") as file:
            file = file.read()
            file = file[file.rindex("'") + 2 :]
            file = file[file.rindex("usabilityRating") + 20 :]
            count = 0
            nums_of = 0
            while True:
                if file[count] == "-" or file[count] == " ":
                    nums_of = nums_of + 1
                else:
                    break
                count = count + 1
            file = file[nums_of + 1 :]
            data = file

        ref = []
        storage = []
        date = []
        downloads = []
        votecount = []
        usabilityRating = []

        while True:
            # append the ref
            ref.append(data[0 : data.index(" ")])
            data = data[data.index(" ") + 1 :]

            # append the memory
            count = 0
            while True:
                if data[count] < "9" and data[count] > "0":
                    while len(data[count : data.index("B")]) > 5:
                        count = count + 1
                        data = data[1:]
                    storage.append(data[count : data.index("B") - 1])
                    break
                count = count + 1

            data = data[
                data.index(storage[len(storage) - 1])
                + len(str(storage[len(storage) - 1]))
                + 4 :
            ]
            # append the date
            date.append(data[0 : data.index(" ")])
            data = data[19:]

            # append number of downloads
            count = 0
            while True:
                if data[count] != " ":
                    count1 = count
                    while True:
                        if data[count1] == " ":
                            downloads.append(data[count:count1])
                            data = data[count1:]
                            break
                        count1 = count1 + 1
                    break
                count = count + 1

            # append Votes
            count = 0
            while True:
                if data[count] != " ":
                    count1 = count
                    while True:
                        if data[count1] == " ":
                            votecount.append(data[count:count1])
                            data = data[count1:]
                            break
                        count1 = count1 + 1
                    break
                count = count + 1

            # append usabilityRating rating
            count = 0
            while True:
                if data[count] != " ":
                    count1 = count
                    while True:
                        if data[count1] == " ":
                            usabilityRating.append(data[count:count1])
                            data = data[count1:]
                            break
                        count1 = count1 + 1
                    break
                count = count + 1
            try:
                count = 0
                while True:
                    if data[count] > "a":
                        data = data[count:]
                        break
                    count = count + 1
            except:
                if len(data) == 0 or data.isspace():
                    break

        names = []
        for x in range(len(ref)):
            names.append(oscommand.capitalize())

        df = pd.DataFrame(
            {
                "Topic": names,
                "Reference": ref,
                "Size": storage,
                "Date": date,
                "Downloads": downloads,
                "Votes": votecount,
                "usabilityRating": usabilityRating,
            }
        )
        return df


print(Search("apple").get_pandas_df())
# print(date)
# print(storage)
# print(ref)
# print(downloads)
# print(votecount)
# print(usabilityRating)
# print(data)

# pass will work
# os.system("kaggle datasets download -d " + ref[0])
# print("H" > "2")
# print("a" > "2")
# print(" " > "A")

#   TEST CASE FAILAURE
#   when typing into the search bar "brain" we get error
# substring not found
# (base) ruthvikatte@nbp-41-192 Enhanced_Predictor % /usr/local/bin/python3 "/Users/ruthvikatte/Downloa
# ds/Ruthvik Atte/Enhanced_Predictor/Search_to_download.py"
# Traceback (most recent call last):
#   File "/Users/ruthvikatte/Downloads/Ruthvik Atte/Enhanced_Predictor/Search_to_download.py", line 134, in <module>
#     print(Search("Brain").get_pandas_df())
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Users/ruthvikatte/Downloads/Ruthvik Atte/Enhanced_Predictor/Search_to_download.py", line 48, in get_pandas_df
#     while len(data[count : data.index("B")]) > 5:
#                            ^^^^^^^^^^^^^^^
# ValueError: substring not found
