import os
import base64
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

endpoint = "https://safety-docs-test.cognitiveservices.azure.com/"
key = "b77fa63d92e04a0c8621a0022af03e68"

# file_path = r"C:\Users\I8924\projects\os_safety-ai-rules\Operating Rules Updated through 8-1-2024 1.pdf"
file_path = r"C:\Users\I8924\projects\os_safety-ai-rules\CSX Contractor Safety  Compliance Guide 11.27.23.pdf"

with open(file_path, "rb") as f:
    base64_encoded_pdf = base64.b64encode(f.read()).decode("utf-8")

analyze_request = {
    "base64Source": base64_encoded_pdf

}

document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

poller = document_intelligence_client.begin_analyze_document("prebuilt-layout", analyze_request=analyze_request)
result = poller.result()

result_dict = {
    "filename": file_path,
    "analyze_result": result.as_dict()
}

output_file_path = r"C:\Users\I8924\projects\os_safety-ai-rules\compliance_rules.json"
with open(output_file_path, "w") as json_file:
    json.dump(result_dict, json_file, indent=4)

print(f"Analysis result saved to {output_file_path}")
print(result.keys())