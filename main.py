import os
import streamlit as st
import pickle
import time
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFaceHub
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate


from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)

st.title("ArticleIQ: A Research Tool ")
st.sidebar.title("Article URLs")

urls = []
for i in range(1):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()
# llm = OpenAI(temperature=0.9, max_tokens=500)
llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    model_kwargs={"temperature":0.5,"max_new_tokens": 512,"max_length":128},
)

if process_url_clicked:
    # load data
    nurls = [
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023",
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-9-2023",
    ]
    loader = WebBaseLoader(urls[0])
    # loader = UnstructuredURLLoader(urls=nurls)
    main_placeholder.text("Data Loading...Started...✅✅✅")
    data = loader.load()    
    print("data :", data)

    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=500,
        chunk_overlap=0
    )
    chunks = text_splitter.split_documents(data)
    len(chunks)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    # docs = text_splitter.split_documents(data)
    # create embeddings and save it to FAISS index
    vectorstore = FAISS.from_documents(chunks, embeddings)

    nquery = "what are the top news"
    ndocs = vectorstore.similarity_search(nquery)
    print(ndocs[0].page_content)

    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    time.sleep(2)

    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore, f)

query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            pick = pickle.load(f)
            retriever = pick.as_retriever(search_type="mmr", search_kwargs={"k":1})
            docs_rel = retriever.get_relevant_documents(query)
            print(docs_rel)
            qa = RetrievalQA.from_chain_type(
                llm = llm,
                retriever = retriever,
                chain_type = "stuff",
                return_source_documents = True
            )
            prompt = f"""
            {query}
            """
            prompt_template = PromptTemplate.from_template(
                "Only answer based on the context provided to you : {content}. Provide only to the point answer"
            )
            prompt_template.format(content=docs_rel)
            response = qa(prompt)
            print(response["result"])
            # chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=pick.as_retriever())
            # result = chain({"question": query}, return_only_outputs=True)
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")
            st.write(response["result"])
            # Display sources, if available
            sources = response.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)


