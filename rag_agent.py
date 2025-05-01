# rag_agent.py

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from vector_search import create_resume_vector_index

# === Custom Prompt Template ===
rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an intelligent resume analysis agent.
Use the following extracted content from a candidate's resume to answer the question.

Resume Content:
{context}

Question:
{question}

Respond with a detailed, professional answer.
"""
)

# === RAG Agent Function ===
def analyze_resume_with_rag(resume_text, query, model_name="mistral"):
    try:
        # Step 1: Create vector index
        vectorstore = create_resume_vector_index(resume_text, model_name=model_name)
        if not vectorstore:
            raise ValueError("Failed to create vectorstore.")

        # Step 2: Set up Ollama LLM
        llm = Ollama(model=model_name)

        # Step 3: Configure Retrieval QA Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            chain_type="stuff",
            chain_type_kwargs={"prompt": rag_prompt}
        )

        # Step 4: Run Query
        response = qa_chain.run(query)
        return response

    except Exception as e:
        return f"❌ RAG Agent Error: {str(e)}"

# === Sample Usage ===
if __name__ == '__main__':
    resume = """
    Software Engineer with expertise in Python, Django, RESTful APIs, and cloud deployment.
    Experienced in agile teams, Git version control, and CI/CD automation.
    """
    question = "What technical skills does this candidate have?"
    result = analyze_resume_with_rag(resume, question)
    print("🤖 RAG Response:\n", result)
