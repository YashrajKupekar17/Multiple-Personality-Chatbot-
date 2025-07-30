import os
from pydantic.v1 import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from mpdagents.config import settings

# --- 1. SETUP: Load API keys and connect to services ---

# Load variables from your .env file
load_dotenv()

# Initialize the OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize the Pinecone client
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

# Check if the index exists, otherwise raise an error
if index_name not in pinecone_client.list_indexes().names():
    raise ValueError(f"Index '{index_name}' does not exist. Please create it first.")

# Connect to your specific index
index = pinecone_client.Index(index_name)

print(f"Successfully connected to Pinecone index: '{index_name}'")

# --- 2. DEFINE YOUR QUERY ---

# The user's question you want to find documents for
user_question = "What is the syllabus for the MOST scholarship test?"

# The target namespace to search within.
# In your real app, this is determined by your query_router.
# For this example, we'll hardcode it to "motion".
target_namespace = "motion"

print(f"\nSearching for: '{user_question}' in namespace '{target_namespace}'...")

# --- 3. EMBED THE QUERY ---

def get_embedding(text: str, openai_client: OpenAI, model="text-embedding-3-small"):
    """Converts a text query into a vector embedding using OpenAI - Synchronous version"""
    try:
        # Ensure text is clean and not empty
        if not text or not text.strip():
            print("Empty text provided for embedding")
            return None
            
        # Clean the text
        clean_text = text.strip()
        
        # Make sure we're passing the right parameters to the API
        response = openai_client.embeddings.create(
            input=clean_text,  # Pass text directly, not as a list
            model=model
        )
        
        return response.data[0].embedding
        
    except Exception as e:
        print(f"Error getting embedding: {e}")
        print(f"Text input: {text}")  # Debug info
        print(f"Model: {model}")      # Debug info
        return None


# query_vector = get_embedding(user_question)

# --- 4. QUERY PINECONE ---

# if query_vector:
#     try:
#         # Perform the search in the specified namespace
#         query_results = index.query(
#             namespace=target_namespace,
#             vector=query_vector,
#             top_k=3,  # Retrieve the top 3 most relevant documents
#             include_metadata=True
#         )

#         # --- 5. DISPLAY THE RESULTS ---
#         print("\n--- Top 3 Retrieved Documents ---")
#         if query_results.matches:
#             for i, match in enumerate(query_results.matches):
#                 text = match.metadata.get('text', 'No text found.')
#                 source = match.metadata.get('source', 'No source found.')
#                 score = match.score

#                 print(f"\n{i+1}. Score: {score:.4f}")
#                 print(f"   Source: {source}")
#                 print(f"   Text: {text[:400]}...") # Print the first 400 characters
#         else:
#             print("No relevant documents found.")

#     except Exception as e:
#         print(f"An error occurred while querying Pinecone: {e}")



class Rag_Input_Schema(BaseModel):
    query : str = ""
    k : int = 3
    namespace : str = "motion"

async def get_rag_context(rag_input: Rag_Input_Schema):
    """Get RAG context from vector database (Pinecone)"""
    
    # Initialize clients
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY)
    index_name = settings.PINECONE_INDEX_NAME

    # Validate inputs
    if not rag_input.query.strip():
        raise ValueError("Query cannot be empty")

    # Check if index exists
    if index_name not in pinecone_client.list_indexes().names():
        raise ValueError(f"Index '{index_name}' does not exist. Please create it first.")
    
    # Connect to index
    index = pinecone_client.Index(index_name)   
    print(f"Successfully connected to Pinecone index: '{index_name}'")

    user_question = rag_input.query.strip()
    target_namespace = rag_input.namespace

    print(f"\nSearching for: '{user_question}' in namespace '{target_namespace}'...")

    # Generate embedding
    query_vector = get_embedding(user_question, openai_client)
    
    if not query_vector:
        raise ValueError("Failed to generate embedding for the query")

    try:
        # Perform the search
        query_results = index.query(
            namespace=target_namespace,
            vector=query_vector,
            top_k=rag_input.k,  # Use the k parameter from input
            include_metadata=True
        )

        # Validate results
        if not query_results.matches:
            print("No relevant documents found.")
            return {"matches": [], "message": "No relevant documents found"}

        print(f"\nFound {len(query_results.matches)} relevant documents")
        
        # Optional: Log results for debugging
        for i, match in enumerate(query_results.matches):
            score = match.score
            source = match.metadata.get('source', 'Unknown source')
            print(f"{i+1}. Score: {score:.4f} | Source: {source}")

        return query_results

    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        raise ValueError(f"Failed to query vector database: {e}")