"""
Elasticsearch client configuration and utilities
"""

from elasticsearch import AsyncElasticsearch
from app.core.config import settings


# Create async Elasticsearch client
es_client = AsyncElasticsearch(
    hosts=[settings.elasticsearch_host],
    verify_certs=False,  # Disable SSL verification for local development
    ssl_show_warn=False,
)


async def create_indices():
    """
    Create Elasticsearch indices with mappings
    """
    # Jobs index mapping
    jobs_mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "title": {
                    "type": "text",
                    "analyzer": "standard",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "company": {
                    "type": "text",
                    "analyzer": "standard",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "location": {"type": "text", "analyzer": "standard"},
                "type": {"type": "keyword"},
                "remote": {"type": "boolean"},
                "salary_min": {"type": "float"},
                "salary_max": {"type": "float"},
                "currency": {"type": "keyword"},
                "description": {"type": "text", "analyzer": "standard"},
                "requirements": {"type": "text", "analyzer": "standard"},
                "benefits": {"type": "text", "analyzer": "standard"},
                "tags": {"type": "keyword"},
                "posted_date": {"type": "date"},
                "expiry_date": {"type": "date"},
                "featured": {"type": "boolean"},
                "category": {"type": "keyword"}
            }
        }
    }

    # Records index mapping
    records_mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "title": {"type": "text", "analyzer": "standard"},
                "description": {"type": "text", "analyzer": "standard"},
                "source": {"type": "keyword"},
                "category": {"type": "keyword"},
                "published_date": {"type": "date"},
                "url": {"type": "keyword"},
                "created_at": {"type": "date"}
            }
        }
    }

    try:
        # Create jobs index
        if not await es_client.indices.exists(index=settings.elasticsearch_index_jobs):
            await es_client.indices.create(
                index=settings.elasticsearch_index_jobs,
                body=jobs_mapping
            )
            print(f"Created Elasticsearch index: {settings.elasticsearch_index_jobs}")

        # Create records index
        if not await es_client.indices.exists(index=settings.elasticsearch_index_records):
            await es_client.indices.create(
                index=settings.elasticsearch_index_records,
                body=records_mapping
            )
            print(f"Created Elasticsearch index: {settings.elasticsearch_index_records}")

    except Exception as e:
        print(f"Error creating Elasticsearch indices: {e}")


async def index_job(job_data: dict):
    """
    Index a job document in Elasticsearch
    """
    try:
        await es_client.index(
            index=settings.elasticsearch_index_jobs,
            id=job_data["id"],
            document=job_data
        )
    except Exception as e:
        print(f"Error indexing job {job_data.get('id')}: {e}")


async def index_record(record_data: dict):
    """
    Index a record document in Elasticsearch
    """
    try:
        await es_client.index(
            index=settings.elasticsearch_index_records,
            id=record_data["id"],
            document=record_data
        )
    except Exception as e:
        print(f"Error indexing record {record_data.get('id')}: {e}")


async def search_jobs(query: str, filters: dict = None, page: int = 1, limit: int = 20):
    """
    Search jobs in Elasticsearch
    """
    if filters is None:
        filters = {}

    # Build search query
    search_body = {
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        },
        "from": (page - 1) * limit,
        "size": limit,
        "sort": [{"posted_date": {"order": "desc"}}]
    }

    # Add text search
    if query:
        search_body["query"]["bool"]["must"].append({
            "multi_match": {
                "query": query,
                "fields": ["title^3", "company^2", "description", "tags", "location"],
                "fuzziness": "AUTO"
            }
        })

    # Add filters
    if filters.get("location"):
        search_body["query"]["bool"]["filter"].append({
            "match": {"location": filters["location"]}
        })

    if filters.get("type"):
        search_body["query"]["bool"]["filter"].append({
            "term": {"type": filters["type"]}
        })

    if filters.get("remote") is not None:
        search_body["query"]["bool"]["filter"].append({
            "term": {"remote": filters["remote"]}
        })

    if filters.get("category"):
        search_body["query"]["bool"]["filter"].append({
            "term": {"category": filters["category"]}
        })

    if filters.get("salary_min") or filters.get("salary_max"):
        salary_filter = {"range": {"salary_min": {}}}
        if filters.get("salary_min"):
            salary_filter["range"]["salary_min"]["gte"] = filters["salary_min"]
        if filters.get("salary_max"):
            salary_filter["range"]["salary_min"]["lte"] = filters["salary_max"]
        search_body["query"]["bool"]["filter"].append(salary_filter)

    try:
        response = await es_client.search(
            index=settings.elasticsearch_index_jobs,
            body=search_body
        )
        return {
            "jobs": [hit["_source"] for hit in response["hits"]["hits"]],
            "total": response["hits"]["total"]["value"],
            "page": page,
            "total_pages": (response["hits"]["total"]["value"] + limit - 1) // limit
        }
    except Exception as e:
        print(f"Error searching jobs: {e}")
        return {"jobs": [], "total": 0, "page": page, "total_pages": 0}


async def search_records(query: str, filters: dict = None, page: int = 1, limit: int = 20):
    """
    Search records in Elasticsearch
    """
    if filters is None:
        filters = {}

    # Build search query
    search_body = {
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        },
        "from": (page - 1) * limit,
        "size": limit,
        "sort": [{"published_date": {"order": "desc"}}]
    }

    # Add text search
    if query:
        search_body["query"]["bool"]["must"].append({
            "multi_match": {
                "query": query,
                "fields": ["title^3", "description", "source"],
                "fuzziness": "AUTO"
            }
        })

    # Add category filter
    if filters.get("category"):
        search_body["query"]["bool"]["filter"].append({
            "term": {"category": filters["category"]}
        })

    try:
        response = await es_client.search(
            index=settings.elasticsearch_index_records,
            body=search_body
        )
        return {
            "records": [hit["_source"] for hit in response["hits"]["hits"]],
            "total": response["hits"]["total"]["value"],
            "page": page,
            "total_pages": (response["hits"]["total"]["value"] + limit - 1) // limit
        }
    except Exception as e:
        print(f"Error searching records: {e}")
        return {"records": [], "total": 0, "page": page, "total_pages": 0}
