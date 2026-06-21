import faiss
import pickle

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "courses.index"
)

with open(
    "courses.pkl",
    "rb"
) as f:

    courses = pickle.load(f)


def search_courses(
    query,
    top_k=5
):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        results.append(
            courses.iloc[idx].to_dict()
        )

    return results