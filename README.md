# 🦨 Auto Column Generator

> AI-powered Kaggle dataset enhancer for Machine Learning and data exploration 🚀

&#x20; &#x20;

---

## ✨ Features

- 🔍 Search Kaggle datasets from the terminal
- 📦 Automatically download and extract CSVs
- 🧠 Use GPT to generate new ML features/columns
- 📊 Auto-generate matplotlib/seaborn visualizations
- 📀 Save enhanced DataFrames to CSV
- 🛉 Automatically clean up temporary files
- 💻 Beautiful terminal interface with [rich](https://github.com/Textualize/rich) and [yaspin](https://github.com/pavdmyt/yaspin)

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/auto-column-generator.git
   cd auto-column-generator
   ```

2. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file with your [OpenAI API key](https://platform.openai.com/account/api-keys):

   ```env
   OPENAI_API_KEY=your_openai_key_here
   ```

4. **Set Up Kaggle CLI**

   - Install the CLI:

     ```bash
     pip install kaggle
     ```

   - Place your `kaggle.json` API key in the correct location:

     ```bash
     mkdir -p ~/.kaggle
     cp kaggle.json ~/.kaggle/
     chmod 600 ~/.kaggle/kaggle.json
     ```

   - Test it:

     ```bash
     kaggle datasets list -s "bitcoin"
     ```

---

## 🚀 Usage

Run the tool using:

```bash
python Auto_Column_Generator.py
```

You'll be guided through:

1. Keyword search for Kaggle datasets
2. Selecting a dataset
3. Loading the CSV
4. Generating enhanced columns via GPT
5. Visualizing the dataset
6. Saving the final DataFrame if desired

---

## 📂 Output

- Enhanced CSVs are saved to: `Enhanced_Data_CSVs/`
- Terminal previews show new columns highlighted
- Visuals are displayed using matplotlib/seaborn

---

## 🛀 Tech Stack

- Python 3.8+
- [OpenAI API](https://platform.openai.com/)
- Kaggle CLI
- `pandas`, `matplotlib`, `seaborn`
- `rich` for terminal UI
- `yaspin` for spinners and loaders

---

## 🧪 Example Output

```
Enter a keyword: stocks
Enter index of dataset: 1

👋 Loaded DataFrame
Generating 10 new columns using GPT...
...
📊 How many visualizations do you want? 5

📂 Saved enhanced DataFrame to Enhanced_Data_CSVs/enhanced_stocks.csv
```

---

## 📌 TODO

- ***

## 🧠 Credits

Made with ❤️ using OpenAI, Kaggle, Python, and coffee.

---

## 📄 License

MIT License
