from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

# === Resume Scorer ===
def score_resume(resume_text, jd_text):
    try:
        # Vectorize text
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([resume_text, jd_text])

        # Compute cosine similarity
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

        # Extract matched terms
        resume_tokens = set(resume_text.lower().split())
        jd_tokens = set(jd_text.lower().split())
        matched_skills = list(resume_tokens.intersection(jd_tokens))

        return similarity, matched_skills
    except Exception as e:
        return 0.0, [f"Error in scoring: {e}"]

# === Feedback Generator ===
def generate_feedback(resume_text, jd_text, model_name="mistral"):
    try:
        prompt_template = PromptTemplate(
            input_variables=["resume", "jd"],
            template="""
You are an expert resume reviewer.
Compare the candidate's resume with the job description below and generate suggestions for improvement.

Resume:
{resume}

Job Description:
{jd}

Provide clear and concise suggestions in bullet points.
"""
        )

        prompt = prompt_template.format(resume=resume_text, jd=jd_text)
        llm = Ollama(model=model_name)
        response = llm.invoke(prompt)
        return response
    except Exception as e:
        return f"❌ Error generating feedback: {e}"
