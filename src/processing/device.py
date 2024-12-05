import os
import sys
sys.path.append(os.getcwd())
import json

import pandas as pd

from src.de.elasctic_module import ElasticSearchHelper
from src.schemas import DeviceRequest
from src.handlers import RequestError
from src.config import (
    ES_HOST,
    ES_USERNAME,
    ES_PASSWORD,
    ES_INDEX_NAME,
    marks_mapping,
)


async def get_device_info(body: DeviceRequest):
    es_client = ElasticSearchHelper(ES_HOST, ES_USERNAME, ES_PASSWORD)
    hits = es_client.search_documents(ES_INDEX_NAME, field="fullname", query_string=body.user_query)
    if len(hits):
        notes, counts = [], {i: 0 for i in range(1, 6)}
        for hit in hits:
            hit_data = hit.get("_source")
            
            for review in hit_data.get("feedbacks"):
                counts[review["rating"]] += 1

            notes.append(
                {
                    **{
                        label: mark 
                        for label, mark in zip(marks_mapping, hit_data.get("mean_mark"))
                    },
                    **{
                        field: hit_data.get(field)
                        for field in ["fullname", "rating", "price", "link"]
                    }, 
                }
            )
        
        total_reviews = sum(list(counts.values()))
        counts = {i: v / total_reviews for i, v in counts.items()}

        data = pd.DataFrame(notes)
        for field in ["rating", "price"] + marks_mapping:
            counts[f"mean_{field}"] = data[field].mean()
        counts["mean_non_zero_rating"] = data.query("rating != 0")["rating"].mean()
        
        data["review_rating"] = data[marks_mapping].mean(axis=1)

        data.dropna(inplace=True)

        return {
            "price_order": (
                data.sort_values(by="price")
                .head(body.top_k)
                .to_dict("records")
            ), 
            "rating_order": (
                data.sort_values(
                    by=["rating", "review_rating"], 
                    ascending=[False, False]
                ).head(body.top_k)
                .to_dict("records")
            ),
            "statistics": counts,
        }

    raise RequestError(body.user_query)