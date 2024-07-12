import openai
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk

df = pd.read_csv("Apple_stock_price_2020.csv")
print(df.columns)


print(df.head())


def GPT():
    dict1 = {}
    cols = df.columns
    for x in cols:
        if len(df[x].unique()) > 7:
            dict1[x] = df[x].unique()[0:7]

        else:
            dict1[x] = df[x].unique()

    Problem_type = "Classification"
    generate_cols = 10

    x = True

    prompt = "Using this data frame with columns and it's unique values = "

    for x in dict1.keys():
        prompt = prompt + x + " : " + str(dict1[x]) + ", "

    prompt = (
        prompt
        + "create "
        + str(generate_cols)
        + " new and unique and meaningful columns using the previous columns as variables to create more meaningful data for a Machine learning "
        + Problem_type
        + " problem and show the python code that creates the "
        + str(generate_cols)
        + " new and unique columns. Only generate pyton code for adding dataframe columns to df without creating a Dataframe and without any comments"
    )

    print(prompt)

    openai.api_key = "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"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    code = response.choices[0].message.content.strip()
    return code
    # exec(code)


def hot_encode():
    str_list = []
    for x in df.columns:
        if df[x].unique().dtype == "object" or df[x].unique().dtype == "string":
            str_list.append(x)

    # ohe = sk.
    return str_list


def pearson_Coefficient():
    list1 = []
    for x in df.columns:
        for y in df.columns:
            num = np.corrcoef(df[x], df[y])
            list1.append(num)
    return list1


# print(string_cols())
exec(GPT())
newdf = df.drop(columns=["Date"])

corr = df.corr()

plt.figure(figsize=(7, 7))  # Adjust the figure size if needed
sns.heatmap(
    corr, cmap="YlGnBu"
)  # 'YlGnBu' is a color map, 'annot=True' adds data value annotation to each cell

plt.show()


# print(newdf.columns)


# print(type(code))
# print(code.rindex(""))
# print(code.rindex("#"))
# code = code[code.rindex("#") + 6 : code.rindex("#") + 1]
# print(code)
