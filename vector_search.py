import os
import tempfile
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

# === Real-Time Resume Vector Indexing ===
def create_resume_vector_index(resume_text, model_name="mistral"):
    try:
        # Step 1: Split resume text into chunks
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents([Document(page_content=resume_text)])

        # Step 2: Generate Embeddings
        embedding_model = OllamaEmbeddings(model=model_name)
        vectorstore = FAISS.from_documents(docs, embedding_model)

        print("✅ Real-time vector store created successfully.")
        return vectorstore

    except Exception as e:
        print("❌ Error creating vector store:", e)
        return None

# === Sample Usage ===
if __name__ == '__main__':
    sample_resume_text = """
    Experienced software developer with 5+ years of experience in Java, Spring Boot,
    SQL, and REST API development. Worked on scalable microservices and cloud deployment using AWS.
    Skilled in Agile methodologies, CI/CD pipelines, Docker, and Git.
    """
    vector_index = create_resume_vector_index(sample_resume_text)

    if vector_index:
        print("✅ Sample resume embedded and indexed for search.")