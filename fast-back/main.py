from fastapi import FastAPI, HTTPException, Depends, Request
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models

from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.vectorstores import FAISS

from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
# from langchain_pinecone import Pinecone
from langchain.vectorstores import Pinecone as PineconeStore

from pinecone import Pinecone, ServerlessSpec, PodSpec
from langchain_community.vectorstores import ElasticsearchStore
from langchain_community.document_loaders import TextLoader

# import pinecone_datasets
# from datasets import load_dataset

import os
from dotenv import load_dotenv
import time

from tqdm.auto import tqdm
from uuid import uuid4

import sys


load_dotenv()  # take environment variables from .env.

# os.environ["HUGGINGFACEHUB_API_TOKEN"] = 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
# load_dotenv()


app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)


class LoginBase(BaseModel):
    masonid: str
    password: str


class LoginModel(LoginBase):

    class Config:
        orm_mode = True

# close database when request is complete


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# automate table creation
db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)


@app.post("/logins/", response_model=LoginModel)
async def create_login(login: LoginBase, db: db_dependency):
    # Change Transaction to Login
    db_login = models.Login(**login.model_dump())
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return db_login


def get_openai_generator(prompt: str):
    llm = ChatOpenAI(
        openai_api_key="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", )

# chat = HuggingFaceHub(
#     repo_id="gpt2")

    with open("events.txt") as f:
        text = f.read()
# print(text[:30])

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=100,
        chunk_overlap=50,
        # length_function=len,
        # is_separator_regex=False,
    )

    docs = text_splitter.create_documents([text])

    embeddings = OpenAIEmbeddings(
        openai_api_key="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",)
    vector = FAISS.from_documents(docs, embeddings)

# print(docs)

# embeddings = HuggingFaceInferenceAPIEmbeddings(
#     api_key='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', model_name="gpt2"
# )
# print(embeddings)
# res = embeddings.embed_documents([text])
# vectors = embeddings.embed_query("How are you")
# print(len(vectors[0][0]))


# # dataset = pinecone_datasets.load_dataset(
# #     'wikipedia-simple-text-embedding-ada-002-100K')

# data = load_dataset("wikipedia", "20220301.simple", split='train[:10000]')
# data

# # data = data.to_pandas()
# # data.head()

# # data.drop_duplicates(subset='context', keep='first', inplace=True)
# # data.head()


# # # we drop sparse_values as they are not needed for this example
# # dataset.documents.drop(['metadata'], axis=1, inplace=True)
# # dataset.documents.rename(columns={'blob': 'metadata'}, inplace=True)
# # # we will use rows of the dataset up to index 30_000
# # dataset.documents.drop(dataset.documents.index[30_000:], inplace=True)

# pc = Pinecone(api_key='e7f63fc4-5722-4205-8435-f25be0d1f3db')
# use_serverless = False
# if use_serverless:
#     spec = ServerlessSpec(cloud='aws', region='us-west-2')
# else:
#     # if not using a starter index, you should specify a pod_type too
#     spec = PodSpec(environment='us-central1-gcp')

# # check for and delete index if already exists
# index_name = 'langchain-retrieval-augmentation-fast'
# if index_name in pc.list_indexes().names():
#     print("---im being deleted----")
#     pc.delete_index(index_name)

# # we create a new index
# pc.create_index(
#     index_name,
#     dimension=768,  # dimensionality of text-embedding-ada-002
#     metric='cosine',
#     spec=PodSpec(
#         environment="gcp-starter"
#     )
# )

# # wait for index to be initialized
# while not pc.describe_index(index_name).status['ready']:
#     time.sleep(1)

# index = pc.Index(index_name)

# print(index.describe_index_stats())

# # for batch in dataset.iter_documents(batch_size=100):
# #     index.upsert(batch)

# batch_limit = 100

# texts = []
# metadatas = []

# for i, record in enumerate(tqdm(data)):
#     # first get metadata fields for this record
#     metadata = {
#         'wiki-id': str(record['id']),
#         'source': record['url'],
#         'title': record['title']
#     }
#     # now we create chunks from the record text
#     record_texts = text_splitter.split_text(record['text'])
#     # create individual metadata dicts for each chunk
#     record_metadatas = [{
#         "chunk": j, "text": text, **metadata
#     } for j, text in enumerate(record_texts)]
#     # append these to current batches
#     texts.extend(record_texts)
#     # print(texts)
#     metadatas.extend(record_metadatas)
#     # print(metadatas)
#     # if we have reached the batch_limit we can add texts
#     if len(texts) >= batch_limit:
#         ids = [str(uuid4()) for _ in range(len(texts))]
#         print('----im here----')
#         embeds = embeddings.embed_documents(texts)
#         index.upsert(vectors=zip(ids, embeds, metadatas))
#         texts = []
#         metadatas = []

# if len(text) > 0:
#     ids = [str(uuid4()) for _ in range(len(texts))]
#     print("---im annoying----")
#     embeds = embeddings.embed_documents(texts)
#     index.upsert(vectors=zip(ids, embeds, metadatas))


# print(index.describe_index_stats())

# vectorstore = PineconeStore.from_documents(
#     docs, embeddings, index_name=index_name)
# for batch in dataset.iter_documents(batch_size=100):
#     index.upsert(batch)

# texts = []

# for i, embed in enumerate(docs):
#     texts.extend(embed)

# print(texts)
# db = ElasticsearchStore.from_documents(
#     docs, embeddings, es_url="http://localhost:9200", index_name="test-basic", distance_strategy="COSINE",
# )

    retriever = vector.as_retriever()
# print("\ngot to indices\n")
# db.client.indices.refresh(index="test-basic")

# print("\ngot to query\n")
# query = "what are the event happening today"
# results = db.similarity_search(query)
# print(results)

    SYSTEM_TEMPLATE = "Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.----------------{context}"
    messages = [
        SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = ({"context": retriever, "question": RunnablePassthrough()}
             | prompt
             | llm
             | StrOutputParser())

    answer = chain.invoke(
        "List all the events from what seems most interest to least interesting")

    print(answer)
    return answer

    # for event in answer:
    #     if "content" in event["choices"][0].delta:
    #         current_response = event["choices"][0].delta.content
    #         yield "data: " + current_response + "\n\n"


@app.get('/login')
async def stream(prompt: str):
    return {"status": "Username stored in database successfully.",
            "response": get_openai_generator(prompt)}
