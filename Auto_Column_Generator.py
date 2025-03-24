from openai import OpenAI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os
import re
from yaspin import yaspin
from time import sleep
from Select_and_download import Download
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich import box

# === Load environment variables ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
console = Console()


def display_header():
    ascii_art = r"""
     █████╗ ██╗   ██╗████████╗ ██████╗      ██████╗ ██████╗ ██╗      ██████╗ ██╗   ██╗
    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██╔════╝ ██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
    ███████║██║   ██║   ██║   ██║   ██║    ██║  ███╗██████╔╝██║     ██║   ██║ ╚████╔╝ 
    ██╔══██║██║   ██║   ██║   ██║   ██║    ██║   ██║██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ╚██████╔╝██║     ███████╗╚██████╔╝   ██║   
    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝      ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
    """

    header = Text()
    header.append(ascii_art, style="bold cyan")
    header.append(
        "\n[bold magenta]Auto Column Generator[/bold magenta] — 🧬 [italic]AI-powered Kaggle data enhancer[/italic]",
        style="white",
    )
    header.append(
        "\n📊 Generate ML features & visualizations in seconds\n", style="green"
    )

    console.print(Panel.fit(header, border_style="bold magenta", padding=(1, 4)))


def display_dataframe_with_highlight(df, original_cols):
    new_columns = [col for col in df.columns if col not in original_cols]
    table = Table(title="\n📊 Enhanced DataFrame Preview", box=box.MINIMAL_DOUBLE_HEAD)

    for col in df.columns:
        style = "bold cyan" if col in new_columns else ""
        table.add_column(col, style=style)

    for _, row in df.head(10).iterrows():
        table.add_row(*[str(val) for val in row.values])

    console.print(table)


def run_pipeline():
    display_header()

    keyword = Prompt.ask("🔍 Enter a keyword to search for Kaggle datasets").strip()
    downloaded = Download(keyword)
    df_list = downloaded.get_listOf_pandasDf()

    if not df_list:
        console.print(
            "❌ No CSV file found in the downloaded dataset.", style="bold red"
        )
        return

    df = df_list[0]
    console.print("\n✅ [bold green]Loaded DataFrame[/bold green]")
    console.print(df.columns)

    original_cols = list(df.columns)

    num_cols = Prompt.ask(
        "🧬 How many new columns would you like to generate?", default="10"
    )
    num_cols = int(num_cols) if num_cols.isdigit() and int(num_cols) > 0 else 10

    def GPT():
        dict1 = {
            x: df[x].unique()[:7] if len(df[x].unique()) > 7 else df[x].unique()
            for x in df.columns
        }

        prompt = "Using this data frame with columns and its unique values = "
        for x in dict1:
            prompt += f"{x}: {dict1[x]}, "

        prompt += (
            f"create {num_cols} new and unique and meaningful columns using the previous columns as variables "
            f"to create more meaningful data for a Machine learning Classification problem and show the python code that creates "
            f"the {num_cols} new and unique columns. Only generate python code for adding dataframe columns to df "
            f"without creating a DataFrame or redefining df. Do not use `data = {{...}}` or `df = pd.DataFrame(...)`."
            f"DO NOT create new variables. Have all logic in one line"
        )
        print(f"Promt: {prompt}")

        with yaspin(
            text="🧠 Generating new columns with GPT...", color="cyan"
        ) as spinner:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            spinner.ok("✅")

        return response.choices[0].message.content.strip()

    code = GPT()
    console.print("\n🧬 [bold cyan]Generated Feature Engineering Code:[/bold cyan]")
    console.print(code)

    lines = code.splitlines()
    column_code_lines = [line for line in lines if line.strip().startswith("df[")]

    for line in column_code_lines:
        try:
            exec(line, globals(), locals())
        except Exception as e:
            console.print(f"⚠️ [yellow]Failed to run line:[/yellow] {line}")
            console.print(f"    [red]Error:[/red] {e}")

    display_dataframe_with_highlight(df, original_cols)

    plt.figure(figsize=(7, 7))
    sns.heatmap(df.corr(numeric_only=True), cmap="YlGnBu", annot=True)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

    def GPT_visualize(num_graphs=5):

        prompt = "Using this data frame with columns and its unique values = "
        for x in df:
            unique_values = df[x].unique()
            if df[x].dtype in ["int64", "float64"] and len(unique_values) > 20:
                # For numeric columns with too many unique values, only include the dtype
                prompt += f"{x}: {df[x].dtype}, "
            else:
                # For categorical columns with too many unique values, show only the first 5 unique values
                if len(unique_values) > 5:
                    prompt += f"{x}: {unique_values[:5]}, "
                else:
                    # For columns with 5 or fewer unique values, show all unique values
                    prompt += f"{x}: {unique_values}, "

        prompt += (
            f"\n\nGenerate Python matplotlib and seaborn code using this dataframe (named `df`) to create approximately {num_graphs} meaningful visualizations and extract insights. "
            "Only generate valid Python code. Do not include markdown, titles, or explanations — only code that could directly run in Python. "
            "Do not include import statements or redefine the dataframe. "
            "Assume df already exists. Do not include comments. "
            "Limit your output to a maximum of 40 lines of executable Python code. "
            "Only use df.corr(numeric_only=True) instead of df.corr()."
            "Always give python code to display the charts after each chart creation."
            "Always have a very detailed comment before the python code on what you did and why for the user to understand."
            "Always have a Title for each chart."
        )

        print(f"PROMPT 2 {prompt}")
        with yaspin(
            text="📊 Generating visualizations with GPT...", color="cyan"
        ) as spinner:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            spinner.ok("✅")

        return response.choices[0].message.content.strip()

    def safe_exec_viz(code, df):
        import builtins

        code = code.replace("```python", "").replace("```", "").strip()
        code = code.replace("df.corr()", "df.corr(numeric_only=True)")

        pattern = r"df\[['\"](.+?)['\"]\]"
        lines = code.split("\n")
        safe_lines = []

        for line in lines:
            if "df[" in line:
                if any(col not in df.columns for col in re.findall(pattern, line)):
                    console.print(f"⚠️ Skipped line due to missing column: {line}")
                    continue
            safe_lines.append(line)

        final_code = "\n".join(safe_lines)
        console.print("\n✅ [bold green]Cleaned Visualization Code:[/bold green]")
        console.print(final_code)

        exec_env = {"df": df, "plt": plt, "sns": sns, "__builtins__": builtins}

        try:
            for line in safe_lines:
                if "plt.show()" in line:
                    with yaspin(text="📈 Plotting chart...", color="green") as spinner:
                        sleep(0.3)
                        exec("plt.show()", exec_env)
                        spinner.ok("✅")
                else:
                    exec(line, exec_env)
        except Exception as e:
            console.print(
                "❌ [bold red]Error while executing visualization code:[/bold red]", e
            )

    num_viz = Prompt.ask(
        "📊 How many visualizations do you want GPT to generate?", default="5"
    )
    num_viz = int(num_viz) if num_viz.isdigit() and int(num_viz) > 0 else 5

    viz_code = GPT_visualize(num_viz)
    # console.print(" UNCLEANED DATA FROM GPT")
    # console.print("_______________________________________")
    # console.print(viz_code)
    # console.print("_______________________________________")
    safe_exec_viz(viz_code, df)

    # Option to save enhanced DataFrame
    save_csv = Prompt.ask(
        "💾 Do you want to save the enhanced DataFrame as a CSV file? (y/n)",
        default="n",
    )
    if save_csv.lower() == "y":
        filename = Prompt.ask(
            "📁 Enter the name for the output CSV file", default="enhanced_data.csv"
        )
        save_path = os.path.join("Enhanced_Data_CSVs", filename)
        os.makedirs("Enhanced_Data_CSVs", exist_ok=True)
        df.to_csv(save_path, index=False)
        console.print(f"✅ [green]Saved enhanced DataFrame to[/green] {save_path}")

    # Clean up CSV files
    for csv_file in downloaded.get_csv_filenames():
        if os.path.exists(csv_file):
            try:
                os.remove(csv_file)
                console.print(f"🧹 Removed CSV file: {csv_file}", style="dim")
            except Exception as e:
                console.print(f"⚠️ Could not delete file {csv_file}: {e}", style="red")


# === Run full pipeline ===
if __name__ == "__main__":
    run_pipeline()
