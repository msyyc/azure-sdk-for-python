import os
from azure.messaging.webpubsubclient import WebPubSubClient
from azure.messaging.webpubsubservice import WebPubSubServiceClient
from azure.messaging.webpubsubclient.models import OnGroupDataMessageArgs
from dotenv import load_dotenv

load_dotenv()


def on_group_message(msg: OnGroupDataMessageArgs):
    print("->" + msg.data)


service_client = WebPubSubServiceClient.from_connection_string(
    connection_string=os.getenv("WEBPUBSUB_CONNECTION_STRING"), hub="hub"
)
url = service_client.get_client_access_token(roles=["webpubsub.joinLeaveGroup", "webpubsub.sendToGroup"])["url"]
client = WebPubSubClient(credential=url)
client.on("group-message", on_group_message)

with client:
    group_name = "test"
    client.join_group(group_name)
    while True:
        question = input()
        if not question:
            break
        client.send_to_group(group_name, question, "text", no_echo=True, ack=True)
