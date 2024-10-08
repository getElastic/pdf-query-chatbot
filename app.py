import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai.embeddings import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI configuration
AZURE_OPENAI_API_TYPE = os.getenv("AZURE_OPENAI_API_TYPE")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")
AZURE_OPENAI_ADA_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_ADA_DEPLOYMENT_NAME")
AZURE_OPENAI_ADA_MODEL_NAME = os.getenv("AZURE_OPENAI_ADA_MODEL_NAME")

# Set the page configuration to change the app name in the browser tab
st.set_page_config(page_title="PDF Query Chatbot", page_icon="📄", layout="wide")

# Streamlit app
st.title("Company Internal Knowledge Base")
st.write("Upload a PDF file and ask a question.")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Initialize variables for state
if 'faiss_vectorStore' not in st.session_state:
    st.session_state.faiss_vectorStore = None

if 'user_question' not in st.session_state:
    st.session_state.user_question = ""

if 'llm' not in st.session_state:
    st.session_state.llm = None

if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None

if uploaded_file and not st.session_state.faiss_vectorStore:
    # Read PDF and extract text
    pdfReader = PdfReader(uploaded_file)
    raw_text = ''

    # Extract text from each page
    for page in pdfReader.pages:
        text = page.extract_text()
        if text:
            raw_text += text

    # Split the text into manageable chunks
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    pdfTexts = text_splitter.split_text(raw_text)

    # Convert text chunks into Document objects
    documents = [Document(page_content=text_chunk, metadata={"source": "pdf"}) for text_chunk in pdfTexts]

    # Initialize Azure OpenAI Embeddings
    embeddings = AzureOpenAIEmbeddings(
        model=AZURE_OPENAI_ADA_MODEL_NAME,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        openai_api_version=AZURE_OPENAI_API_VERSION
    )

    # Create FAISS vector store from documents and embeddings
    st.session_state.faiss_vectorStore = FAISS.from_documents(documents, embeddings)

    # Initialize the LLM
    st.session_state.llm = AzureChatOpenAI(
        azure_deployment="gpt-35-turbo",
        api_version="2024-07-01-preview",
        temperature=0.6,
        max_tokens=None,
        max_retries=2,
        model="gpt-35-turbo",
        model_version="2024-05-13"
    )

    # Prepare the QA Chain
    condense_question_system_template = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    condense_question_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", condense_question_system_template),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        st.session_state.llm, st.session_state.faiss_vectorStore.as_retriever(), condense_question_prompt
    )

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    st.session_state.qa_chain = create_stuff_documents_chain(st.session_state.llm, qa_prompt)
    st.session_state.convo_qa_chain = create_retrieval_chain(history_aware_retriever, st.session_state.qa_chain)

    st.success("PDF has been processed. You can now ask a question.")

# User input for question (only visible after file upload)
if st.session_state.faiss_vectorStore:
    st.session_state.user_question = st.text_input("Enter your question:")
    submit_button = st.button("Submit")

    # Process the query only if the button is clicked
    if submit_button and st.session_state.user_question:
        # Process the question and get the answer
        with st.spinner("Processing..."):
            conversation_output = st.session_state.convo_qa_chain.invoke(
                {
                    "input": st.session_state.user_question,
                    "chat_history": [],
                }
            )

        # Extract the answer attribute
        answer = conversation_output.get("answer", "No answer found.")

        # Display the response in a text box
        st.text_area("Response:", value=answer, height=200)
    elif submit_button:
        st.warning("Please enter a question.")
else:
    st.warning("Please upload a PDF file to start.")