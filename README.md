<p align="center">
<b>the unibasedb vector database component</b>
</p>

<p align=center>
<a href="https://pypi.org/project/unibasedb/"><img alt="PyPI" src="https://img.shields.io/pypi/v/unibase?label=Release&style=flat-square"></a>
<a href="https://pypistats.org/packages/unibasedb"><img alt="PyPI - Downloads from official pypistats" src="https://img.shields.io/pypi/dm/unibasedb?style=flat-square"></a>
</p>

`unibase` is a vector database offering a comprehensive suite of [CRUD](#crud-support) (Create, Read, Update, Delete) operations and robust scalability options scaling-your-db, including sharding and replication. It is deployable across various environments: from [local development](#getting-started-with-unibase-locally) to [on-premise servers](#getting-started-with-unibase-as-a-service) and the cloud.

By leveraging the power of [DocArray](https://github.com/docarray/docarray) for vector logic and a powerful serving layer, `unibasedb` provides a lean, Pythonic design tailored for performance without unnecessary complexity.

## 🚀 Install

```bash
pip install unibasedb
```

<table>
  <tr>
    <td>
      <a href="#-getting-started-with-unibase-locally">
        <img src="https://raw.githubusercontent.com/Unibase-Labs/unibasedb/refs/heads/main/media/local.png" alt="Use unibasedb locally" width="100%">
      </a>
    </td>
    <td>
      <a href="#getting-started-with-unibase-as-a-service">
        <img src="https://raw.githubusercontent.com/Unibase-Labs/unibasedb/refs/heads/main/media/cloud.png" alt="Use unibasedb as a service" width="100%">
      </a>
    </td>
  </tr>
</table>



## 🎯 Getting started with `unibase` locally

This example demonstrates how to use `unibasedb` to build a **Book Recommendation Agent**. The agent retrieves similar books based on a user's query, highlighting the dynamic, reasoning-based applications of `unibasedb`.

### Step 1: Define a Document Schema

We begin by defining the schema for our data using [DocArray](https://docs.docarray.org/user_guide/representing/first_step/). In this example, our data consists of books with attributes such as title, author, description, and a vector embedding.

```python
from docarray import BaseDoc
from docarray.typing import NdArray

# Define a schema for books
class BookDoc(BaseDoc):
    title: str  # Title of the book
    author: str  # Author of the book
    description: str  # A brief description of the book
    embedding: NdArray[128]  # 128-dimensional embedding for the book
```

This schema lays the foundation for how data will be stored and queried in `unibasedb`.

---

### Step 2: Initialize the Database and Index Data

Next, we initialize a database and populate it with some simulated book data.

```python
from docarray import DocList
import numpy as np
from unibasedb import InMemoryExactNNUnibase

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
```

**Explanation**:
1. **Database Initialization**:
   - We use `InMemoryExactNNUnibase` to create an in-memory database. The `workspace` parameter specifies where data is stored.
2. **Indexing Data**:
   - A list of 100 books with fake data (random titles, authors, and embeddings) is created and indexed into the database.

---

### Step 3: Simulate a Book Recommendation Agent

We create a simple agent that accepts a user query and retrieves similar books from the database.

```python
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
```

**Explanation**:
- The `BookRecommendationAgent` encapsulates logic for querying the database and processing results.
- It takes a user's query (text and embedding) and searches the database for similar books.

---

### Step 4: Query the Agent with User Input

Finally, we simulate user input and use the agent to retrieve recommendations.

```python
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
```

**Explanation**:
1. **User Input**:
   - The user provides a query (e.g., "A gripping tale of adventure and discovery") and a simulated embedding.
2. **Recommendations**:
   - The agent queries the database and retrieves the top 3 similar books based on the embedding.
3. **Display Results**:
   - The results are formatted and printed for the user.

---

## Getting started with `unibase` as a service

`unibasedb` is designed to be easily served as a service, supporting `gRPC`, `HTTP`, and `Websocket` communication protocols. 

### Server Side

Server Side Example: A Book Recommendation Database.
On the server side, you would start the service as follows. 

```python
from docarray import BaseDoc, DocList
from docarray.typing import NdArray
import numpy as np

from unibasedb import InMemoryExactNNUnibase

# Define a Document schema for book information
class BookDoc(BaseDoc):
    title: str
    author: str
    description: str
    embedding: NdArray[128]  # Example: A 128-dimensional vector representing the book's content

# Initialize the database
db = InMemoryExactNNUnibase[BookDoc](workspace='./books_workspace')

# Generate fake data for books and index it
book_list = [
    BookDoc(
        title=f"Book {i}",
        author=f"Author {chr(65 + i % 26)}",
        description=f"A fascinating description of Book {i}.",
        embedding=np.random.rand(128)  # Random embeddings for demonstration
    )
    for i in range(100)  # Simulate 100 books
]

db.index(inputs=DocList[BookDoc](book_list))

# Serve the database as a gRPC service
if __name__ == '__main__':
    print("Starting the Book Recommendation Database...")
    with db.serve(protocol='grpc', port=12345, replicas=1, shards=1) as service:
        print("Book Recommendation Database is running on gRPC://localhost:12345")
        print("You can now query the database from a client.")
        service.block()



```

This command starts `unibase` as a service on port `12345`, using the `gRPC` protocol with `1` replica and `1` shard.

### Client Side

Once the **Book Recommendation Database** is running as a service on the server, you can access it from a client application. Here's how to query the service for recommendations:

```python
from docarray import BaseDoc, DocList
from docarray.typing import NdArray
import numpy as np
from unibasedb import Client

# Define the same schema used on the server
class BookDoc(BaseDoc):
    title: str
    author: str
    description: str
    embedding: NdArray[128]

# Instantiate a client connected to the server
# Replace '0.0.0.0' with the actual IP address of the server
client = Client[BookDoc](address='grpc://0.0.0.0:12345')

# Create a query book
query_book = BookDoc(
    title="User Query",
    author="N/A",
    description="An epic story of friendship and courage.",
    embedding=np.random.rand(128)  # Simulated query embedding
)

# Perform a search query
results = client.search(inputs=DocList[BookDoc]([query_book]), limit=5)

# Display the search results
print("Top 5 similar books:")
for match in results[0].matches:
    print(f"Title: {match.title}, Author: {match.author}, Description: {match.description}")
```

### Explanation of the Code:
1. **Schema Definition**:
   - The client defines the same `BookDoc` schema used on the server to ensure compatibility.

2. **Connecting to the Server**:
   - The `Client` connects to the `grpc://0.0.0.0:12345` address. Replace `0.0.0.0` with the server's actual IP address if running on a remote machine.

3. **Query Creation**:
   - The `query_book` represents a user's input, including a description and an embedding that simulates the query vector.

4. **Performing the Search**:
   - The `search` method sends the query to the server and retrieves the top 5 similar books.

5. **Displaying Results**:
   - The retrieved matches are printed, showing the titles, authors, and descriptions of the recommended books.

---


## Advanced Topics

### What is a vector database?

A vector database is a specialized type of database designed to store, manage, and retrieve vector embeddings—numerical representations of data such as text, images, audio, or other complex objects. Unlike traditional databases that rely on exact matches or keyword searches, vector databases excel at performing similarity searches. They use advanced algorithms to find data points that are semantically or contextually similar to a given query, even if the exact match doesn't exist.

### CRUD Support

Both local library usage and client-server interactions in `unibase` share the same API, providing `index`, `search`, `update`, and `delete` functionalities:

- **Index**: Accepts a `DocList` to index.
- **Search**: Takes a `DocList` of batched queries or a single `BaseDoc` as a query. Returns results with `matches` and `scores`, sorted by relevance.
- **Delete**: Accepts a `DocList` of documents to remove from the index. Only the `id` attribute is required, so ensure you track indexed IDs for deletion.
- **Update**: Replaces existing documents in the index with new attributes and payloads from the input `DocList`.

### Service Endpoint Configuration

You can configure and serve `unibase` with the following parameters:

- **Protocol**: The communication protocol, which can be `gRPC`, `HTTP`, `websocket`, or a combination. Default is `gRPC`.
- **Port**: The port(s) for accessing the service. Can be a single port or a list of ports for multiple protocols. Default is 8081.
- **Workspace**: The directory where the database persists its data. Default is the current directory (`.`).

### Scaling Your Database

`unibase` supports two key scaling parameters for deployment:

- **Shards**: The number of data shards. This reduces latency by ensuring documents are indexed in only one shard. Search queries are distributed across all shards, and results are merged.
- **Replicas**: The number of database replicas. Using the [RAFT](https://raft.github.io/) algorithm, `unibase` synchronizes indexes across replicas, improving availability and search throughput.

### Vector Search Configuration

#### InMemoryExactNNUnibase

This database performs exact nearest neighbor searches with minimal configuration:

- **Workspace**: The directory where data is stored.

```python
InMemoryExactNNUnibase[MyDoc](workspace='./unibasedb')
InMemoryExactNNUnibase[MyDoc].serve(workspace='./unibasedb')
```

#### HNSWUnibase

This database uses the HNSW (Hierarchical Navigable Small World) algorithm from [HNSWLib](https://github.com/nmslib/hnswlib) for approximate nearest neighbor searches. It offers several configurable parameters:

- **Workspace**: The directory for storing and persisting data.
- **Space**: The similarity metric (`l2`, `ip`, or `cosine`). Default is `l2`.
- **Max Elements**: The initial index capacity, which can grow dynamically. Default is 1024.
- **ef_construction**: Controls the speed/accuracy trade-off during index construction. Default is 200.
- **ef**: Controls the query time/accuracy trade-off. Default is 10.
- **M**: The maximum number of outgoing connections in the graph. Default is 16.
- **allow_replace_deleted**: Enables replacement of deleted elements. Default is `False`.
- **num_threads**: The number of threads used for `index` and `search` operations. Default is 1.

### Command Line Interface

`unibase` includes a straightforward CLI for serving and deploying your database:

| Description                     |                          Command | 
|---------------------------------|---------------------------------:|
| Serve your DB locally           | `unibasedb serve --db example:db` |

## Features

- **User-Friendly Interface**: Designed for simplicity, `unibase` caters to users of all skill levels.
- **Minimalistic Design**: Focuses on essential features, ensuring smooth transitions between local, server, and cloud environments.
- **Full CRUD Support**: Comprehensive support for indexing, searching, updating, and deleting operations.
- **DB as a Service**: Supports `gRPC`, `HTTP`, and `Websocket` protocols for efficient database serving and operations.
- **Scalability**: Features like sharding and replication enhance performance, availability, and throughput.
- **Serverless Capability**: Supports serverless deployment for optimal resource utilization.
- **Multiple ANN Algorithms**: Offers a variety of Approximate Nearest Neighbor (ANN) algorithms, including:
   - **InMemoryExactNNUnibase**: For exact nearest neighbor searches.
   - **HNSWUnibase**: Based on the HNSW algorithm for efficient approximate searches.

## Roadmap

We have exciting plans for `unibase`! Here’s what’s in the pipeline:

- **More ANN Algorithms**: Expanding support for additional ANN search algorithms.
- **Enhanced Filtering**: Improving filtering capabilities for more precise searches.
- **Customizability**: Making `unibase` highly customizable to meet specific user needs.
- **Expanded Serverless Capacity**: Enhancing serverless deployment options in the cloud.



