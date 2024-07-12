from Search_to_download import Search
import os
import zipfile
import pandas as pd


def run_oscommand(directory):
    os.system("kaggle datasets download -d " + directory + " --force")


def displayOptions(keyword):
    df = Search(keyword).get_pandas_df()
    print(df)
    while True:
        x = input("Enter Index Number: ")
        print(df.iloc[int(x)])
        return df.iloc[int(x)]


def download(keyword):
    ref = displayOptions(keyword)
    run_oscommand(ref["Reference"])
    print("Sucessfully Installed " + ref["Reference"] + ".csv")
    return ref


def extractZip(key):
    ref = download(key)
    name = str(ref["Reference"]).split("/")
    with zipfile.ZipFile(name[0] + ".zip", "r") as zip:
        filenames = zip.namelist()
        zip.extractall()
    os.remove(name[0] + ".zip")
    print("sucessfully Extracted Zip and got:")
    print(filenames)
    return filenames


class Download:
    filenames = ""

    def __init__(self, key):
        global filenames
        filenames = extractZip(key)

    def get_listOf_pandasDf(self):
        filenames
        for i in filenames:
            df = pd.read_csv(str(i))
            dataSet = []
            dataSet.append(df)
        return dataSet

    # def deleteAll_csv(self):
    #     for i in filenames:
    #         os.remove(i)


x = Download("beach")
# print(download("apple_stock"))
print(x.get_listOf_pandasDf()[0].columns)
# x.deleteAll_csv()
