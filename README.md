# pdf-query-chatbot

This Internal Knowledge Base Chatbot is designed to answer queries related to the contents of a PDF document uploaded from the browser where the Streamlit app is running. The chatbot leverages advanced technologies, including Langchain, Azure OpenAI, FAISS vector store, Streamlit, and Python, utilizing the gpt-35-turbo model for question-answering tasks and text-embedding-ada-002 for embedding.

The process flow of the chatbot involves:

    1. Upload PDF file: The user uploads a PDF document through the browser interface.
    2. User input for question: The user asks a question related to the document.
    3. Read PDF and extract text: The app reads and extracts text from the uploaded PDF.
    4. Extract text from each page: Text from each page of the PDF is gathered.
    5. Split the text into manageable chunks: The extracted text is split into smaller chunks for efficient processing.
    6. Convert text chunks into Document objects: These text chunks are transformed into Document objects for further processing.
    7. Initialize Azure OpenAI Embeddings: The embeddings are generated using text-embedding-ada-002.
    8. Create FAISS vector store from documents and embeddings: A FAISS vector store is created to enable fast retrieval of relevant document sections.
    9. Initialize the LLM: The gpt-35-turbo model is initialized to handle question-answering.
    10. Prepare the QA Chain: The Question Answering chain is set up using Langchain.
    11. Process the question and get the answer: The user's question is processed, and the model retrieves   relevant context from the document.
    12. Extract the answer attribute: The answer is extracted and displayed for the user.

This app is an efficient, knowledge-driven assistant for internal document queries, making use of Azure OpenAI services for high-quality responses.

## Prerequisites

- Install the below Python packages using pip in your environment : pip install [name of package]

python-dotenv 
os
streamlit 
PyPDF2 
langchain 
langchain-openai
langchain-community
langchain-core
faiss-cpu

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/pdf-query-chatbot.git
   cd pdf-query-chatbot
   ```
   
2. **Add your OpenAI API key**:

   Update the .env file with your Azure OpenAI API key:
   ```bash
   AZURE_OPENAI_API_TYPE=azure
   AZURE_OPENAI_DEPLOYMENT_NAME="your_azure_openai_deployment_name_here"
   AZURE_OPENAI_MODEL_NAME="gpt-35-turbo" #azure openai model used
   AZURE_OPENAI_ADA_DEPLOYMENT_NAME="your_azure_openai_ada_deployment_name_here"
   AZURE_OPENAI_ADA_MODEL_NAME="text-embedding-ada-002" #azure openai embedding model used
   AZURE_OPENAI_API_KEY="your_azure_openai_api_key_here"
   AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint_here"
   AZURE_OPENAI_API_VERSION="your_azure_openai_api_version_here"
   ```
## How to Run

In the root directory of the project, run the following command to start the Streamlit app:

   ```bash
   streamlit run app.py
   ```

This command will start the Streamlit application on your local system.


## Access the application:

Once the application is running, you can access the application in your web browser at http://localhost:8501.

##  Usage

1. **Corporate Knowledge Management:**

    Employees can upload internal documents such as manuals, policies, or reports and ask specific questions about them.
    It improves productivity by providing quick answers without having to manually search through lengthy documents.

2. **Legal and Compliance:**

    Law firms or compliance departments can upload legal contracts, regulations, or case files to quickly extract relevant information.
    It helps in navigating complex legal texts, making it easier to search for specific clauses or legal precedents.

3. **Healthcare and Medical Documentation:**

    Healthcare professionals can upload medical papers, guidelines, or research studies and ask questions related to treatment protocols or medical conditions.
    Facilitates access to critical information, ensuring timely responses to medical queries.

4. **Research and Academia:**

    Researchers or students can upload academic papers, research publications, or textbooks and ask detailed questions.
    Enhances academic research by making it easier to find information buried in long documents.

5. **Client Support and Training:**

    Organizations can use the chatbot to help employees or clients quickly access product documentation, training materials, or onboarding guides.
    Reduces the need for human support by providing automated, document-based answers.

6. **Human Resources:**

    HR teams can upload employee handbooks, benefits documents, or legal compliance forms to answer employee queries.
    This improves HR operations by allowing employees to self-serve when looking for specific policies or procedures.

7. **Government and Public Sector:**

    Government agencies can upload policies, regulations, or public reports and enable users to ask specific questions.
    Streamlines public services by helping users access the information they need without navigating complex bureaucratic documents.

8. **Financial and Investment Sector:**

    Financial institutions can upload investor reports, financial analyses, or market research and allow professionals to query specific data points.
    Helps with decision-making by making data retrieval from financial reports more efficient.

9. **Customer Support for Product Documentation:**

    Companies can upload product manuals, warranty guides, or troubleshooting documents to answer customer inquiries automatically.
    Great for reducing support ticket volumes by providing customers with self-service options.

10. **Knowledge Sharing in Engineering or IT Teams:**

    IT teams can upload technical specifications, architecture designs, or coding standards, and engineers can quickly query for specific details.
    Helps in maintaining and sharing critical technical knowledge efficiently across teams.

These use cases demonstrate how the chatbot can simplify access to complex information, offering a wide range of possibilities across different industries and functions.

## Files Description
- **app.py:** The main Streamlit application file.
