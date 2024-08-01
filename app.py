from flask import Flask, Response
from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)

# .env ファイルから環境変数を読み込む
load_dotenv()

# Cosmos DBの設定
endpoint = os.getenv("AZURE_COSMOS_ACCOUNT_ENDPOINT")
key = os.getenv("AZURE_COSMOS_ACCOUNT_KEY")
database_name = os.getenv("AZURE_COSMOS_DB_NAME")
container_name = os.getenv("AZURE_COSMOS_DB_CONTAINER_NAME")

# Cosmos DBのクライアントとコンテナの設定
cosmos_client = CosmosClient(endpoint, key)
# cosmos_client = CosmosClient(
#     url=endpoint, credential=key, consistency_level="Session"
# )
database = cosmos_client.get_database_client(database_name)
cosmos_container = database.get_container_client(container_name)


@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        query = "SELECT c.user_id, c.timestamp, c.conversation[0].mode as mode, c.conversation[0].content as questiion, c.conversation[1].content as answer FROM c ORDER BY c.timestamp DESC"
        items = list(
            cosmos_container.query_items(
                query, enable_cross_partition_query=True
            )
        )
        json_data = json.dumps(items, ensure_ascii=False)
        return Response(json_data, mimetype='application/json')
    except exceptions.CosmosHttpResponseError as e:
        error_data = {"error": str(e)}
        json_error = json.dumps(error_data, ensure_ascii=False)
        return Response(json_error, mimetype='application/json', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
