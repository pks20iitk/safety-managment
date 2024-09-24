# import os
# import base64
# import json
# import logging
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.documentintelligence import DocumentIntelligenceClient

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class DocumentProcessor:
#     """Processes documents using Azure Document Intelligence."""

#     def __init__(self, endpoint: str, key: str):
#         self.client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

#     def analyze_document(self, file_path: str) -> dict:
#         """Analyze the document and return the result as a dictionary.

#         Args:
#             file_path (str): The path to the PDF file to analyze.

#         Returns:
#             dict: The analysis result.
#         """
#         with open(file_path, "rb") as file:
#             base64_encoded_pdf = base64.b64encode(file.read()).decode("utf-8")

#         analyze_request = {"base64Source": base64_encoded_pdf}
#         poller = self.client.begin_analyze_document("prebuilt-layout", analyze_request=analyze_request)
#         result = poller.result()

#         result_dict = {
#             "filename": file_path,
#             "analyze_result": result.as_dict()
#         }

#         output_file_path = os.path.splitext(file_path)[0] + "_analysis.json"
#         with open(output_file_path, "w") as json_file:
#             json.dump(result_dict, json_file, indent=4)

#         logger.info(f"Analysis result saved to {output_file_path}")
#         return result_dict