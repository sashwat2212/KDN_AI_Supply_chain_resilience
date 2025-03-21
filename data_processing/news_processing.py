import pandas as pd
from transformers import pipeline
from py2neo import Graph, Node

# Load news data
df = pd.read_csv("/Users/kdn_aisashwat/Desktop/supply_chain_resillience/extracted_news.csv")

# Use NLP model to classify risk
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

risk_labels = ["Geopolitical Risk", "Cybersecurity Risk", "Climate Risk", "Low Impact"]

graph = Graph("bolt://localhost:7687", auth=("neo4j", "Sashwat@22"))


for _, row in df.iterrows():
    title = row["title"]
    full_text = row["full_text"]
    
    # Handle missing values
    if pd.isna(full_text) or full_text is None:
        full_text = "NA"  

    # Combine title and full_text
    combined_text = f"{title}. {full_text}"
    
    # NLP Classification
    classification = classifier(combined_text, risk_labels)
    risk_type = classification["labels"][0]
    
    # Create Graph Node
    event_node = Node("RiskEvent", title=title, full_text=combined_text, risk_type=risk_type)
    graph.create(event_node)
