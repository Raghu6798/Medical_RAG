import sys
import os
from uuid import uuid4

import chainlit as cl  
from langchain.prompts import ChatPromptTemplate
from databases.Redis.redis_cache import semantic_cache
from langchain.globals import set_llm_cache
from obvservability.langfuse_setup import langfuse_handler
from langchain_core.output_parsers import StrOutputParser
from loguru import logger

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)
logger.add(
    "chainlit_app.log",
    rotation="10 MB",
    retention="1 week",
    compression="zip",
    level="DEBUG"
)

logger.info("Starting Medical QA Assistant")

# Ensure parent dir is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger.debug(f"Added parent directory to path: {os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))}")

try:
    logger.debug("Importing database modules...")
    from databases.Neo4j.graph_database import graph, graph_history
    from langchain.vectorstores import Neo4jVector
    from langchain_community.chat_message_histories import Neo4jChatMessageHistory
    from langchain_core.prompts.chat import MessagesPlaceholder
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from agent2agent.models.embedding_model.embed_model import Embed_model
    from models.llm_model.llm import LLM
    logger.info("All modules imported successfully")
except Exception as e:
    logger.error(f"Error importing modules: {str(e)}")
    raise

# Global vars
chat_with_message_history = None
retriever = None
SESSION_ID = str(uuid4())
logger.info(f"Session ID: {SESSION_ID}")

try:
    logger.debug("Setting up Redis semantic cache...")
    set_llm_cache(semantic_cache)
    logger.info("Redis semantic cache set successfully")
except Exception as e:
    logger.error(f"Failed to set Redis semantic cache: {str(e)}")
    raise
# Cypher-style system prompt

CYPHER_PROMPT = """
You are a highly knowledgeable AI medical assistant integrated with a clinical backend.

Your goal is to assist healthcare professionals by retrieving accurate information from a medical knowledge graph and returning well-structured, medically sound responses.

Respond to the user's query using the context below. Your answer **must follow a structured clinical format** when appropriate and **align with clinical communication standards**.

Format:
1. **Clinical Overview** – Summarize the topic or question concisely.
2. **Relevant Findings** – Use the context to expand on the user query with references to known diseases, treatments, or patient symptoms.
3. **Clinical Recommendations** – Where appropriate, offer medically accurate suggestions (not diagnoses), always framed as potential advice a physician may consider.
4. **Graph Context** – If Cypher or knowledge graph data contributes to the answer, refer to it clearly but in plain English.
5. **Example or Use Case** – Give an example scenario (clinical or patient-facing).
6. **Conclusion** – Recap key points clearly.

Always:
- Use medically accurate terminology.
- Avoid speculative advice.
- Do not hallucinate if context is insufficient.
- Maintain professionalism and follow clinical communication standards.

Context: {context}
"""

def get_retrieved_context(query: str) -> str:
    logger.debug(f"Retrieving context for query: {query}")
    try:
        retrieved_documents = retriever.invoke(query)
        logger.debug(f"Retrieved {len(retrieved_documents)} documents")
        context = "\n".join(doc.page_content for doc in retrieved_documents)
        logger.debug(f"Context length: {len(context)} characters")
        return context
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}")
        return "Error retrieving context. Please try again."

def get_memory(session_id):
    logger.debug(f"Getting memory for session: {session_id}")
    try:
        return Neo4jChatMessageHistory(session_id=session_id, graph=graph_history)
    except Exception as e:
        logger.error(f"Error getting memory: {str(e)}")
        raise

@cl.on_chat_start
async def on_chat_start():
    logger.info("Chat session started")
    global chat_with_message_history, retriever 
    
    await cl.Message(content="🧠 Initializing medical assistant...").send()
    logger.debug("Sent initialization message")
    
    try:
        # Connect to Neo4j vector store
        logger.debug("Connecting to Neo4j vector store...")
        graph_store = Neo4jVector.from_existing_index(
            Embed_model,
            graph=graph,
            index_name="vector",
            embedding_node_property="Embedding",
            text_node_property="text",
            retrieval_query="""
            MATCH (node)-[:PART_OF]->(d:Document)
            WITH node, score, d
            MATCH (node)-[:HAS_ENTITY]->(e)
            MATCH p = (e)-[r]-(e2)
            WHERE (node)-[:HAS_ENTITY]->(e2)
            UNWIND relationships(p) as rels
            WITH node, score, d, collect(apoc.text.join(
                [labels(startNode(rels))[0], startNode(rels).id, type(rels), 
                labels(endNode(rels))[0], endNode(rels).id], " ")) as kg
            RETURN node.text as text, score,
                { document: d.id, entities: kg } AS metadata
            """
        )
        logger.info("Connected to Neo4j vector store")
        
        retriever = graph_store.as_retriever()
        logger.debug("Created retriever from vector store")
        
        # Build prompt
        logger.debug("Building prompt template...")
        prompt = ChatPromptTemplate.from_messages([
            ("system", CYPHER_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
        
        chain = prompt | LLM | StrOutputParser()
        logger.debug("Created language chain")
        
        chat_with_message_history = RunnableWithMessageHistory(
            chain,
            get_memory,
            input_messages_key="question",
            history_messages_key="chat_history",
        )
        logger.info("Chat pipeline with message history initialized")
        
        await cl.Message(content="✅ Medical assistant ready! Ask your question.").send()
        logger.debug("Sent ready message")
    except Exception as e:
        error_msg = f"Error during initialization: {str(e)}"
        logger.error(error_msg)
        await cl.Message(content=f"❌ Error initializing: {str(e)}").send()
@cl.on_message
async def on_message(message: cl.Message):
    logger.info(f"Received message: {message.content[:50]}...")
    global chat_with_message_history, retriever

    user_query = message.content

    try:
        # Retrieve context
        logger.debug("Getting context for query...")
        context = get_retrieved_context(user_query)

        # Send empty message object to stream into
        msg = cl.Message(content="")
        await msg.send()

        # Stream the response using astream
        logger.debug("Streaming response with astream...")
        async for chunk in chat_with_message_history.astream({
            "question": user_query,
            "context": context,
        }, config={
            "configurable": {"session_id": SESSION_ID},
            "callbacks":[langfuse_handler]
        }):
            await msg.stream_token(chunk)

        await msg.update()
        logger.info("Streaming completed")

    except Exception as e:
        error_message = f"Error processing query: {str(e)}"
        logger.error(error_message)
        await cl.Message(content=f"❌ Error: {error_message}").send()
