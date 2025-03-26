import pandas as pd
from transformers import pipeline

# Load news data
df = pd.read_csv("/Users/kdn_aisashwat/Desktop/supply_chain_resillience/extracted_news.csv")


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


risk_labels = ["Geopolitical Risk", "Cybersecurity Risk", "Climate Risk", "Low Impact"]


risk_types = []

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
    risk_type = classification["labels"][0]  # Top classification result

    # Append the predicted risk type
    risk_types.append(risk_type)


df["risk_type"] = risk_types


output_path = "/Users/kdn_aisashwat/Desktop/supply_chain_resillience/classified_news.csv"
df.to_csv(output_path, index=False)

print(f"Classified news saved to {output_path}")