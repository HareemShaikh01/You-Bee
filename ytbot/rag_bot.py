from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Initialize once
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

prompt = PromptTemplate(
    template="""
You are a helpful YouTube chatbot named You-Bee. 
Briefly answer questions from the given context.
If the context is insufficient, just say: "Sorry man, this question is not covered in this video."

context: {context}
question: {query}
""",
    input_variables=["context", "query"]
)

# Session cache
current_video_id = None
retriever = None

def load_video_to_retriever(video_id: str):
    global current_video_id, retriever

    if current_video_id == video_id and retriever is not None:
        print("video id is same")
        return retriever  # Already loaded

    # New video, update everything
    transcript = YouTubeTranscriptApi().fetch(video_id)
    docs = " ".join([snippet.text for snippet in transcript])
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([docs]) 

    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    current_video_id = video_id

    return retriever

def get_bot_response(video_id: str, question: str) -> str:
    retriever = load_video_to_retriever(video_id)
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    final_prompt = prompt.invoke({"context": context, "query": question})
    answer = llm.invoke(final_prompt)
    return answer.content
