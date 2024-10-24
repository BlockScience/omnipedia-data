import json
from pymongo import MongoClient

connection_string = ''

client = MongoClient(connection_string)
db = client['omnipedia']

def query_collection(collection_name, query={}):
    # Get the collection
    collection = db[collection_name]
    
    # Perform the query
    results = collection.find(query)
    
    # Print the results
    for document in results:
        print(document)

# Query each collection
# query_collection('adcyap1_wikipedia')
# query_collection('adcyap1_wikicrow')
# query_collection('agk_wikipedia')
# query_collection('agk_wikicrow')
# query_collection('atf1_wikipedia')
# query_collection('atf1_wikicrow')



def upload_json_to_mongodb(file_path, collection_name):
    # Read JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Get or create collection
    collection = db[collection_name]
    
    # Insert data
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    
    print(f"Uploaded {file_path} to {collection_name}")


upload_json_to_mongodb('Documents/ANLN-wikipedia.json', 'anln_wikipedia')
upload_json_to_mongodb('Documents/ANLN-wikicrow.json', 'anln_wikicrow')


