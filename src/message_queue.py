import os
import json
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient
from azure.identity import ClientSecretCredential

from settings import app_settings

load_dotenv()

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID") 
client_secret = os.getenv("AZURE_CLIENT_SECRET")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

servicebus_client = ServiceBusClient(app_settings.service_bus_host, credential=credential, logging_enable=True)

# def process_message(message):

#     if hasattr(message, 'body') and isinstance(message.body, (bytes, bytearray)):
#         message_body = message.body.decode('utf-8')
#         message_data = json.loads(message_body)
#     # message_body = message.body.decode('utf-8')
#     # message_data = json.loads(message_body)

#         document_id = message_data.get("documentId")
#         document_name = message_data.get("documentName")
#         effective_date = message_data.get("effectiveDate")
#         document_type = message_data.get("documentType")
#         division = message_data.get("division")
#         subdivision = message_data.get("subdivision")
#         subFolder = message_data.get("subFolder")
#         source_type = message_data.get("type")
#         document_version = message_data.get("documentVersion")
#         rail_carrier_code = message_data.get("railCarrierCode")
#         ecmDocumentName = message_data.get("ecmDocumentName")
#         expiration_date = message_data.get("expirationDate")
#         documentExpired = message_data.get("documentExpired")
    
#         return document_id, document_name, effective_date, document_type, document_version, rail_carrier_code

with servicebus_client:
    receiver = servicebus_client.get_subscription_receiver(topic_name=app_settings.service_bus_topic_name, subscription_name=app_settings.service_bus_subscription_name)
    with receiver:
        for msg in receiver:
            if msg.content_type == "application/json":
                message = json.loads(str(msg))
                document_name = message["documentName"]
                
                print(message)
                break
#             document_id, document_name, effective_date, document_type, document_version, rail_carrier_code = process_message(msg)
#             print(f"Received: {document_name}, ID: {document_id}, Effective Date: {effective_date}, Type: {document_type}, Version: {document_version}, Carrier Code: {rail_carrier_code}")
#             # receiver.complete_message(msg)  # Remove the message from the subscription