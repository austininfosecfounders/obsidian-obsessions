import os

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

MODEL      = "mixtral:8x22b-instruct"
VAULT_PATH = "/Users/pedram/Library/Mobile Documents/iCloud~md~obsidian/Documents/Pedsidian"
INDEX_PATH = VAULT_PATH + "/.llamaindex"

# LLM and embedding settings.
Settings.llm = Ollama(model=MODEL, request_timeout=60.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# create or laod index.
if not os.path.exists(INDEX_PATH):
    print("initializing embeddings...")
    # load the documents and create the index
    documents = SimpleDirectoryReader(VAULT_PATH, required_exts=[".md"], recursive=True, exclude=["GenAI/*"]).load_data()
    index = VectorStoreIndex.from_documents(documents)

    # store it for later
    index.storage_context.persist(persist_dir=INDEX_PATH)

else:
    print("loading embeddings...")
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_PATH)
    index = load_index_from_storage(storage_context)

# query engine REPL.
query_engine = index.as_query_engine()

while True:
    query = input("Enter your query (or 'exit' to quit): ")

    if query.lower() == 'exit':
        break

    response = query_engine.query(query)

    print(response)
