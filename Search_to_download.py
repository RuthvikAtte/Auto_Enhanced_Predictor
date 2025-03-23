import os
import pandas as pd


class Search:
    def __init__(self, keyword):
        self.keyword = keyword
        os.system(f'kaggle datasets list -s "{keyword}" > output.txt')

    def get_pandas_df(self):
        try:
            with open("output.txt", "r") as f:
                lines = f.readlines()

            # Filter out warnings
            lines = [line for line in lines if not line.startswith("Warning")]

            # Find the start of the actual data (after header line)
            header_line_index = -1
            for i, line in enumerate(lines):
                if "ref" in line and "title" in line:
                    header_line_index = i
                    break

            if header_line_index == -1 or header_line_index + 2 >= len(lines):
                raise ValueError("Could not find dataset table in kaggle output.")

            data_lines = lines[header_line_index + 2 :]

            ref = []
            title = []
            size = []
            last_updated = []
            downloads = []
            votes = []
            usability = []

            for line in data_lines:
                if not line.strip():
                    continue
                # Split line based on fixed-width columns
                ref_col = line[:50].strip()
                title_col = line[50:90].strip()
                size_col = line[90:98].strip()
                date_col = line[98:118].strip()
                downloads_col = line[118:133].strip()
                votes_col = line[133:144].strip()
                usability_col = line[144:].strip()

                ref.append(ref_col)
                title.append(title_col)
                size.append(size_col)
                last_updated.append(date_col)
                downloads.append(downloads_col)
                votes.append(votes_col)
                usability.append(usability_col)

            df = pd.DataFrame(
                {
                    "Topic": [self.keyword.capitalize()] * len(ref),
                    "Reference": ref,
                    "Title": title,
                    "Size": size,
                    "Last Updated": last_updated,
                    "Downloads": downloads,
                    "Votes": votes,
                    "Usability Rating": usability,
                }
            )

            return df

        except Exception as e:
            print("Error while parsing Kaggle output:", str(e))
            return pd.DataFrame()


# Example usage
# if __name__ == "__main__":
# df = Search("apple").get_pandas_df()
# print(df)
