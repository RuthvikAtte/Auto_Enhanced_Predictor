# Auto_Enhanced_Predictor

Create an openai-env with your API Key

# This project takes data and adds extra unique columns to the pandas data frame to make better feature engineering decisions. 

The Search_to_download.py takes in a search word and returns a Kaggle .txt file with all of the links to the data repos and manually parses it into a Pandas Dataframe

The Select_and_download.py imports the class in Search_to_download.py, uses the dataframe to download the CSV files, and automatically unzips them for use. 

The Add_Columns.py connects to GPT 3.5 and prompts it to create X new and unique and meaningful columns using the previous columns as variables to create more meaningful data for Machine learning ( classification or regression ) problems and show the Python code that makes the X many new and unique columns. Only generate Python code for adding data frame columns to df without creating a dataframe and without any comments. with this prompt, the code uses the string of commands and executes it to add the column created by GPT 3.5 

Then using the Pearson correlation coefficient heat map I am trying to use either a GPT 3.5 prompt or a graph nn to see what columns are best fitted with each other and which columns are not necessary and would cause the ML algorithm's accuracy to go down.
