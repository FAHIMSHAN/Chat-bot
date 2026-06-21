import pandas as pd
import faiss
import pickle

from sentence_transformers import SentenceTransformer

print("Loading EduPlatform course dataset...")

df = pd.read_excel("course_data.xlsx")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

documents = []

for _, row in df.iterrows():

    text = f"""
    Course Level: {row['Course Level']}
    Course Name: {row['Course Name']}
    Subject: {row['Subject']}
    Course Type: {row['Course Type']}
    Duration: {row['Duration (months)']}
    Fees: {row['Fees']}
    Language: {row['Language']}
    Description: {row['Description']}
    Course Link: {row['Course Link']}
    """

    documents.append(text)

embeddings = model.encode(
    documents,
    convert_to_numpy=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    "courses.index"
)

with open("courses.pkl", "wb") as f:
    pickle.dump(df, f)

print("EduPlatform Vector Database Created Successfully")
