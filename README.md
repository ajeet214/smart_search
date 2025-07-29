# Smart Search with GenAI

![Smart Search Logo](https://raw.githubusercontent.com/your-username/smart-search/main/assets/logo.png)

> **An intelligent, LLM-powered semantic search tool for querying structured data using natural language.**

---

## 🔍 Overview

**Smart Search with GenAI** is a semantic search application that combines vector similarity search (FAISS) with Azure OpenAI's powerful LLMs to answer user queries over structured datasets. Users can input natural language questions and receive context-aware, summarized responses based on pre-indexed data.

Built with **Streamlit**, the UI offers an interactive, user-friendly experience with prompt suggestions, onboarding guidance, and instant query answers.

---

## ✨ Features

* 🔎 Natural language search over structured data (Excel)
* 🧠 Azure OpenAI embedding + summarization (text-embedding-ada-002 + gpt-4o-mini)
* ⚡ Fast retrieval using FAISS vector index
* 🔁 Chunk reranking using cosine similarity for better accuracy
* 💡 Suggested prompt buttons to guide user input
* 👋 Onboarding walkthrough for new users
* 📊 Built-in Streamlit interface (no frontend coding needed)

---

## 🧱 Tech Stack

| Category         | Tools Used                                |
| ---------------- | ----------------------------------------- |
| UI               | Streamlit + Custom CSS                    |
| Embedding Model  | Azure OpenAI `text-embedding-ada-002`     |
| Completion Model | Azure OpenAI `gpt-4o-mini` (configurable) |
| Vector DB        | FAISS                                     |
| Reranking        | Cosine Similarity (Scikit-learn)          |
| Data Format      | Excel (`.xlsx`) + Pandas                  |
| Configuration    | Python `dotenv`                           |

---
## 📦 Project Structure

```bash
smart_search/
├── README.md
├── app.py                         # Streamlit UI
├── pyproject.toml                 # Project metadata & dependencies
├── .python-version                # Python version spec
├── uv.lock                        # Dependency lock file (if committed)
├── .gitignore
│
├── .env                          # [Not committed] Environment variables
│
├── data/                         # Input data
│   ├── raw/
│   │   ├── people_data_100.xlsx
│   │   ├── people_data_500.xlsx
│   │   └── people_data_1000.xlsx
│   └── processed/
│       └── people_data_1000_with_textchunk.xlsx
│
├── embeddings/                   # Vector storage & metadata
│   ├── chunk_embeddings.npy
│   ├── faiss_index_people_data.index
│   └── metadata.csv
│
├── prompts/
│   └── prompt_v1.txt             # LLM prompt template
│
├── scripts/                      # One-time/utility scripts
│   ├── __init__.py
│   ├── embed_and_index.py        # Embedding + indexing pipeline
│   ├── preprocess.py             # Excel data transformation
│   ├── search.py                 # Basic FAISS query CLI
│   └── search_with_llm.py        # RAG CLI interface
│
├── styles/
│   └── style.css                 # Custom CSS styling for Streamlit
│
└── utils/                        # Reusable backend logic
    ├── __init__.py
    ├── answer_generator.py       # Prompt & LLM answer generator
    ├── azure_openai_client.py    # Auth wrapper for Azure OpenAI
    ├── config.py                 # Env & path configs
    ├── embedder.py               # Query embedder
    ├── examples.py               # Suggested prompt examples
    ├── onboarding.py             # First-time user walkthrough
    ├── prompt_loader.py          # Load prompt from file
    ├── reranker.py               # Cosine-based reranker
    └── search_engine.py          # Semantic + reranked search logic
```

## ⚙️ Setup Instructions


1. **Clone the repository**

   ```bash
   - git clone https://github.com/ajeet214/smart_search.git
   - cd smart_search

2. **Install dependencies and setup environment using `uv`**

   - Initialize environment (if not already done):

     ```uv init```
   - Install dependencies (defined in pyproject.toml):
  
     ```uv sync```

3. **Activate the virtual environment**

   - Using `uv`:

     ```uv shell```
   - Or activate .venv manually::
     ```bash
     source .venv/bin/activate      # Linux/macOS
     .venv\Scripts\activate         # Windows
     ```

4. **Configure environment**

    Create a `.env` file at the root and fill the 
    - `AZURE_OPENAI_API_KEY`, 
    - `AZURE_OPENAI_ENDPOINT`
    , leave all other as it is.
    - You may change the `SHOW_ONBOARDING` to `false` if you like to disable the onboarding screen.
    
    ```env
    # Azure OpenAI
    AZURE_OPENAI_API_KEY=your_key_here
    AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
    AZURE_OPENAI_API_VERSION=2023-05-15
    AZURE_OPENAI_DEPLOYMENT=text-embedding-ada-002
    AZURE_OPENAI_COMPLETION_DEPLOYMENT=gpt-4o-mini
    
    # File Paths
    INPUT_FILE=data/processed/people_data_1000_with_textchunk.xlsx
    OUTPUT_INDEX=embeddings/faiss_index_people_data.index
    OUTPUT_METADATA=embeddings/metadata.csv
    CHUNK_EMBEDDINGS_PATH=embeddings/chunk_embeddings.npy
    
    # UI Behavior
    SHOW_ONBOARDING=true
    ```
---

## 4. Prepare Data

```bash
python scripts/preprocess.py
```
---

## 5. Generate Embeddings and Build Index

```bash
python scripts/embed_and_index.py
```
---
## Launch the App
To start the Streamlit web app, run:
```bash
uv run streamlit run app.py
```
or if your virtual environment is active:
```bash
streamlit run app.py
```
Then open your browser and go to:
```commandline
http://localhost:8501
```
---

## 💡 Example Prompts

* "Who attended AI-related events in Singapore?"
* "List members of the Data Science team based in Tokyo."
* "What events did Alice Ly take part in?"
* "Show the Marketing team members from Vietnam."

---

## 🔒 Security Note

This project uses Azure OpenAI via environment variables. **Never commit your `.env` file**. Always include `.env` in `.gitignore`.

---

---

## 🚀 Roadmap / Future Enhancements

* [ ] Support multi-file or live data ingestion
* [ ] Add citation reference to answers
* [ ] Export responses (PDF, Markdown)
* [ ] Chat history tracking
* [ ] Authentication layer for private access

---

## 📄 License

MIT License. Feel free to fork and extend.

---

## 🙌 Acknowledgements

* [Streamlit](https://streamlit.io/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Azure OpenAI](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)

---

Let me know if you'd like me to help you add badges, deployment instructions (e.g., for Azure App Service or HuggingFace Spaces), or GitHub Actions CI/CD!

Built with ❤️ by Ajeet using Azure OpenAI, Streamlit, and FAISS.
