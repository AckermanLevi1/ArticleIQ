
# ArticleIQ: "Decode Articles, Discover Wisdom."

ArticleIQ is a user-friendly news research tool designed to facilitate effortless information retrieval across diverse domains. Users can easily input article URLs and ask questions, receiving relevant insights spanning a wide range of topics. Whether you're delving into technology, health, science, or any other domain, ArticleIQ empowers users with a seamless and intuitive platform for informed decision-making based on comprehensive research

## Our Demo Video
[CLick this](https://drive.google.com/file/d/1ygL-XWVFEbDsimaV1y9-1qkmPKWXUwn_/view?usp=sharing)


## Features

- Load URLs to fetch article content.
- Process article content through LangChain's WebbasedURL Loader
- Construct an embedding vector using MistralAI embeddings and leverage FAISS, a powerful similarity search library, to enable swift and effective retrieval of relevant information
- Interact with the LLM by inputting queries and receiving answers along with source URLs.


## Usage/Examples

1. Run the Streamlit app by executing:
```bash
python -m streamlit run main.py

```

2.The web app will open in your browser.

- On the sidebar, you can input URLs directly.

- Initiate the data loading and processing by clicking "Process URLs."

- Observe the system as it performs text splitting, generates embedding vectors, and efficiently indexes them using FAISS.

- The embeddings will be stored and indexed using FAISS, enhancing retrieval speed.

- The FAISS index will be saved in a local file path in pickle format for future use.
- One can now ask a question and get the answer based on those news articles
- In video tutorial, we used following news articles
  - https://en.wikipedia.org/wiki/Article_370_of_the_Constitution_of_India
  - https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/


## Project Structure

- main.py: The main Streamlit application script.
- requirements.txt: A list of required Python packages for the project.
- faiss_store_openai.pkl: A pickle file to store the FAISS index.
- .env: Configuration file for storing your HuggingFace API key.


## Contributing

Contributions to this repository are welcome. If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This repository is licensed under the [MIT License](LICENSE).
