import openai
import streamlit as st
import PyPDF2
import os
import requests
from bs4 import BeautifulSoup

# ✅ Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or use: openai.api_key = "your-api-key"

# ✅ Extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# ✅ Estimate token count
def estimate_tokens(text):
    return len(text.split())

# ✅ Use the updated openai>=1.0.0 API format
def query_gpt(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# ✅ Scrape websites for extra info
def scrape_websites():
    urls = [
        "https://www.bou.ac.bd/BOU/VCProfile",
        "https://www.bousst.edu.bd/faculty-members"
    ]
    scraped_data = ""
    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3']):
                scraped_data += tag.get_text() + "\n"
        except Exception:
            continue
    return scraped_data

# ✅ Split large text into overlapping chunks
def split_text_into_chunks(text, max_tokens=16000, overlap=1000):
    tokens = text.split()
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunks.append(' '.join(tokens[start:end]))
        start += (max_tokens - overlap)
    return chunks

# ✅ List your PDF files
pdf_files = ["1.pdf", "2.pdf", "3.pdf", "4.pdf"]

# ✅ Streamlit interface
st.title("📚 BOUSST AI Chat Assistant")

# User inputs a question
question = st.text_input("Ask your question:")

if question:
    answer_found = False
    final_answer = ""

    for pdf_path in pdf_files:
        text = extract_text_from_pdf(pdf_path)
        for chunk in split_text_into_chunks(text):
            if estimate_tokens(chunk) + estimate_tokens(question) <= 16000:
                prompt = f"Based on the following text from a document, answer the user’s query:\n\n{chunk}\n\nUser's query: {question}. If the answer is not found, respond with 'I am sorry.'"
                response = query_gpt(prompt)
                if response and "I am sorry" not in response:
                    final_answer = response
                    answer_found = True
                    break
        if answer_found:
            break

    # If no answer found in PDFs, search websites
    if not answer_found:
        scraped = scrape_websites()
        for chunk in split_text_into_chunks(scraped):
            prompt = f"Based on the following info from websites, answer the query:\n\n{chunk}\n\nQuestion: {question}"
            response = query_gpt(prompt)
            if response and "I am sorry" not in response:
                final_answer = response
                answer_found = True
                break

    # Fallback
    if not answer_found:
        final_answer = query_gpt(f"Answer this general query:\n\n{question}")

    st.subheader("Answer:")
    st.text_area("Result", value=final_answer, height=200)

# 🔄 Reset Button
if st.button("Reset"):
    st.session_state.clear()
    st.rerun()
