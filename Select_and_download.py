from Search_to_download import Search
import os
import zipfile
import pandas as pd


def run_oscommand(dataset_ref):
    os.system(f"kaggle datasets download -d {dataset_ref} --force")


def displayOptions(keyword):
    df = Search(keyword).get_pandas_df()
    if df.empty:
        print(f"No datasets found for keyword '{keyword}'. Try again.")
        return None

    print(df)
    while True:
        try:
            x = input("Enter Index Number: ")
            selected = df.iloc[int(x)]
            print("\nSelected Dataset:\n", selected)
            return selected
        except Exception as e:
            print("Invalid input. Try again. Error:", e)


def download(keyword):
    ref = displayOptions(keyword)
    if ref is None:
        return None
    run_oscommand(ref["Reference"])
    print("Successfully downloaded:", ref["Reference"])
    return ref


def extractZip(keyword):
    ref = download(keyword)
    if ref is None:
        return []
    dataset_id = str(ref["Reference"]).split("/")[-1]
    zip_filename = dataset_id + ".zip"

    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        filenames = zip_ref.namelist()
        zip_ref.extractall()
    os.remove(zip_filename)

    print("Successfully extracted ZIP and got files:")
    print(filenames)
    return filenames


class Download:
    def __init__(self, keyword):
        self.filenames = extractZip(keyword)
        self.csv_filenames = [f for f in self.filenames if f.endswith(".csv")]

    def get_listOf_pandasDf(self):
        dataSet = []
        for file in self.csv_filenames:
            df = pd.read_csv(file)
            dataSet.append(df)
        return dataSet

    def get_csv_filenames(self):
        return self.csv_filenames

    # Optional cleanup
    # def deleteAll_csv(self):
    #     for file in self.csv_filenames:
    #         os.remove(file)


# === Ask user for keyword and load dataset ===
if __name__ == "__main__":
    keyword = input("🔍 Enter a keyword to search for Kaggle datasets: ").strip()
    x = Download(keyword)

    dfs = x.get_listOf_pandasDf()
    if dfs:
        print("\n📊 First CSV DataFrame Columns:")
        print(dfs[0].columns)
        print("\n📂 CSV Filename:")
        print(x.get_csv_filenames()[0])
    else:
        print("⚠️ No CSV files found in the dataset.")
