from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from get_transcript import getTranscript
from dotenv import load_dotenv

load_dotenv()

# 🔹 Initialize embeddings and LLM
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# 🔹 Prompt Template
prompt = PromptTemplate(
    template="""
You are You-Bee, a smart YouTube assistant.

Use the following video transcript context to answer the user's question **in detail**.
- If the answer is clearly in the video, give a complete and helpful explanation.
- If not, say:
"This question is not covered in the video. However, the answer is:" — and then give a thoughtful answer using your own knowledge.

Transcript Context:
{context}

User's Question:
{query}

Your Answer:
""",
    input_variables=["context", "query"]
)

# 🔹 Cache for performance
current_video_id = None
retriever = None

# 🔹 Build or reuse retriever
def load_video_to_retriever(video_id: str):
    global current_video_id, retriever

    if current_video_id == video_id and retriever is not None:
        print("video id is same")
        return retriever  # Already loaded

    print("loading transcript and building retriever...")

    # Load and split transcript
    transcript = getTranscript(video_id)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript]) 

    # Create vector store
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Use MMR-based retriever for more diverse context
    retriever = vector_store.as_retriever(
        search_type="mmr", 
        search_kwargs={"k": 5, "fetch_k": 10}
    )
    current_video_id = video_id

    return retriever

# 🔹 Get response
def get_bot_response(video_id: str, question: str) -> str:
    retriever = load_video_to_retriever(video_id)
    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    print("\n📌 Context fed to model:\n", context[:500], "...")  # debug print

    final_prompt = prompt.invoke({"context": context, "query": question})
    answer = llm.invoke(final_prompt)

    return answer.content
