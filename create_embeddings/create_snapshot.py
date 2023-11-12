from qdrant_client import QdrantClient, models

from qdrant_client import QdrantClient, models

collection_name = "swiss_law"

client = QdrantClient("localhost")

snapshot_info = client.create_snapshot(collection_name=collection_name)
print(f'http://localhost:6333/collections/{collection_name}/snapshots/{snapshot_info["name"]}')

