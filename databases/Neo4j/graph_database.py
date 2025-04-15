import os 

from langchain_neo4j import Neo4jGraph

from dotenv import load_dotenv
load_dotenv()

#graph for knowledge base
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

# graph for chat history 
graph_history = Neo4jGraph(
    url=os.getenv("NEO4J_URI_2"),
    username=os.getenv("NEO4J_USERNAME_2"),
    password=os.getenv("NEO4J_PASSWORD_2")
)