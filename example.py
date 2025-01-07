from docarray import BaseDoc
from docarray.typing import NdArray

from docarray import DocList
import numpy as np
from unibasedb import InMemoryExactNNUnibase


# Define a schema for books
class BookDoc(BaseDoc):
    title: str  # Title of the book
    author: str  # Author of the book
    description: str  # A brief description of the book
    embedding: NdArray[128]  # 128-dimensional embedding for the book


# Step 1: Initialize the database
db = InMemoryExactNNUnibase[BookDoc](workspace='./book_workspace')

# Step 2: Generate book data and index it
book_list = [
    BookDoc(
        title=f"Book {i}",
        author=f"Author {chr(65 + i % 26)}",  # Rotate through letters A-Z
        description=f"A fascinating story of Book {i}.",
        embedding=np.random.rand(128)  # Simulated embedding
    )
    for i in range(100)  # Create 100 books
]
db.index(inputs=DocList[BookDoc](book_list))


# Step 3: Simulate an AI agent
class BookRecommendationAgent:
    def __init__(self, database):
        self.database = database

    def recommend_books(self, query_text: str, query_embedding: np.ndarray, limit=5):
        # Simulate reasoning: Query the database for recommendations
        query_doc = BookDoc(
            title="User Query",
            author="N/A",
            description=query_text,
            embedding=query_embedding
        )
        results = self.database.search(inputs=DocList[BookDoc]([query_doc]), limit=limit)

        # Process results
        recommendations = [
            {
                "title": result.title,
                "author": result.author,
                "description": result.description
            }
            for result in results[0].matches
        ]
        return recommendations


# Step 4: Use the agent
agent = BookRecommendationAgent(db)

# Simulated user input
user_query = "A gripping tale of adventure and discovery."
user_embedding = np.random.rand(128)  # Simulated embedding for the query

recommendations = agent.recommend_books(query_text=user_query, query_embedding=user_embedding, limit=3)

# Step 5: Display recommendations
print("Recommended books:")
for i, rec in enumerate(recommendations, start=1):
    print(f"{i}. Title: {rec['title']}, Author: {rec['author']}, Description: {rec['description']}")