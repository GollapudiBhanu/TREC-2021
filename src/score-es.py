from elasticsearch import Elasticsearch

elastic_client = Elasticsearch()

# Take the user's parameters and put them into a Python
# dictionary structured like an Elasticsearch query:
query_body = {
 "query": {
    "bool" : {
      "should" : [
         { "term" : { "detailed_description_text_block": "melanoma" } },
         #{ "term" : { "detailed_description_text_block": "EGFR (D770N)" } }
      ],
    }
  }
}

result = elastic_client.search(index="2019-trec-precision-medicine", body=query_body)

print ("total hits:", len(result["hits"]["hits"]))
print(result)
