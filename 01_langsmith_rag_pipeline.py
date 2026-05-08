"""
Step 1 — LangSmith-instrumented RAG Pipeline
=============================================
TASK:
  1. Load your dataset, split into chunks, index with FAISS
  2. Build a RAG chain: retriever → prompt → LLM → output parser
  3. Decorate the query function with @traceable so every call is traced
  4. Run all 50 questions → generates ≥ 50 LangSmith traces

DELIVERABLE: Open https://smith.langchain.com and confirm traces appear.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ── 1. Environment setup ────────────────────────────────────────────────────
# Load .env file
load_dotenv()

# Ensure LangSmith environment variables are set
# (They should be loaded from .env, but we can verify or set defaults if needed)
if not os.environ.get("LANGCHAIN_API_KEY"):
    print("⚠️  LANGCHAIN_API_KEY not found in environment. Tracing might not work.")

# ── 2. LangChain + LangSmith imports ────────────────────────────────────────
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langsmith import traceable

# ── 3. LLM and Embeddings ───────────────────────────────────────────────────
# Using gpt-4o-mini as a reasonable default for a lab
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)


# ── 4. Build FAISS vector store ─────────────────────────────────────────────
def build_vectorstore():
    """
    Load the knowledge base, split into chunks, embed and index with FAISS.
    """
    # Read dataset file
    data_path = Path("data/knowledge_base.txt")
    if not data_path.exists():
        print(f"❌ Dataset not found at {data_path}")
        sys.exit(1)
        
    text = data_path.read_text(encoding="utf-8")

    # Split text
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    print(f"Split into {len(chunks)} chunks")

    # Build and return the FAISS vectorstore
    print("Building FAISS index...")
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore


# ── 5. RAG prompt template ──────────────────────────────────────────────────
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the context below to answer the question. If the context doesn't contain the answer, say 'I don't know based on the provided context'.\n\nContext:\n{context}"),
    ("human",  "{question}"),
])


# ── 6. Build the RAG chain ──────────────────────────────────────────────────
def build_rag_chain(vectorstore):
    """
    Build a LangChain RAG chain using LCEL.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain, retriever


# ── 7. Traced query function ────────────────────────────────────────────────
@traceable(name="rag-query", tags=["rag", "step1"])
def ask(chain, question: str) -> str:
    """
    Run the RAG chain on a single question.
    The @traceable decorator sends input/output/latency to LangSmith.
    """
    return chain.invoke(question)


# ── 8. Sample questions (50 total — one per topic area) ────────────────────
SAMPLE_QUESTIONS = [
    "What are the three main types of machine learning?",
    "What is overfitting in machine learning?",
    "Explain the bias-variance tradeoff.",
    "How does regularization prevent overfitting?",
    "What is cross-validation?",
    "What is backpropagation?",
    "What are Convolutional Neural Networks primarily used for?",
    "How do LSTM networks address the vanishing gradient problem?",
    "What activation functions are commonly used in neural networks?",
    "What is the role of pooling layers in CNNs?",
    "What is the transformer architecture?",
    "What are word embeddings?",
    "What is transfer learning in NLP?",
    "How does BERT handle language understanding?",
    "What is self-attention in transformers?",
    "What is GPT and how is it trained?",
    "What is instruction tuning?",
    "What is RLHF?",
    "What is chain-of-thought prompting?",
    "What is the context length of GPT-4?",
    "What is Retrieval-Augmented Generation?",
    "What are the main components of a RAG pipeline?",
    "What is dense retrieval?",
    "Why is chunking strategy important in RAG?",
    "What advanced RAG techniques exist beyond basic retrieval?",
    "What are vector databases used for?",
    "What is FAISS?",
    "How do text embeddings capture semantic meaning?",
    "What is HNSW?",
    "What is hybrid search in vector databases?",
    "What is LangChain?",
    "What is LangChain Expression Language (LCEL)?",
    "What is LangGraph?",
    "What memory types does LangChain support?",
    "What are LangChain retrievers?",
    "What is LangSmith?",
    "What information do LangSmith traces capture?",
    "What is the LangSmith Prompt Hub?",
    "How does LangSmith help monitor production LLM applications?",
    "What are LangSmith datasets used for?",
    "What is RAGAS?",
    "How does RAGAS compute faithfulness?",
    "What is answer relevancy in RAGAS?",
    "What is context recall in RAGAS?",
    "What inputs does RAGAS evaluation require?",
    "What is Guardrails AI?",
    "What is PII and why is it important to detect in LLM responses?",
    "What does structured output validation ensure?",
    "What is Constitutional AI?",
    "What are common AI safety concerns with LLMs?",
]


# ── 9. Main ─────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Step 1: LangSmith RAG Pipeline")
    print("=" * 60)

    # Build the vectorstore
    vectorstore = build_vectorstore()

    # Build the RAG chain
    chain, retriever = build_rag_chain(vectorstore)

    # Loop through all SAMPLE_QUESTIONS, call ask(), print results
    print(f"\nRunning {len(SAMPLE_QUESTIONS)} questions...")
    for i, question in enumerate(SAMPLE_QUESTIONS, 1):
        answer = ask(chain, question)
        print(f"[{i:02d}/{len(SAMPLE_QUESTIONS)}] Q: {question[:60]}")
        answer_preview = answer[:100].replace('\n', ' ')
        print(f"       A: {answer_preview}...\n")

    # Print confirmation that traces were sent
    print(f"✅ {len(SAMPLE_QUESTIONS)} traces sent to LangSmith project '{os.environ.get('LANGCHAIN_PROJECT', 'default')}'")
    print("   Open https://smith.langchain.com to view traces.")


if __name__ == "__main__":
    main()
