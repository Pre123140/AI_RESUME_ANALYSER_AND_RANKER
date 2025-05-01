from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# === Step 1: Load the Mistral model from Ollama ===
try:
    llm = Ollama(model="mistral")  # Make sure mistral is running in Ollama
    print("✅ Mistral LLM loaded via Ollama")
except Exception as e:
    print("❌ Failed to connect to Mistral via Ollama:", e)
    raise

# === Step 2: Create a basic prompt template for now ===
prompt_template = PromptTemplate(
    input_variables=["query"],
    template="""
    You are a resume analysis assistant. Answer the following query based on the uploaded resume:
    
    Query: {query}
    
    Respond in a clear, concise, and professional manner.
    """
)

# === Step 3: Create LLMChain ===
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    verbose=True
)

# === Step 4: Test it with a sample query ===
if __name__ == '__main__':
    test_query = "What are the candidate's top technical skills?"
    response = llm_chain.run({"query": test_query})
    print("\n🧠 LLM Response:")
    print(response)
