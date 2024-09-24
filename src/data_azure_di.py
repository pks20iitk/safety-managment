import os
import base64
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

endpoint = "https://safety-docs-test.cognitiveservices.azure.com/"
key = "b77fa63d92e04a0c8621a0022af03e68"
file_path = r"C:\Users\I8924\projects\os_safety-ai-rules\data\Operating Rules Updated through 8-1-2024 1.pdf"



with open(file_path, "rb") as f:
    base64_encoded_pdf = base64.b64encode(f.read()).decode("utf-8")

    analyze_request = {
        "base64Source": base64_encoded_pdf
    }

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", analyze_request=analyze_request,
        # "prebuilt-layout", analyze_request=analyze_request, #output_content_format=ContentFormat.MARKDOWN,
    )

    result = poller.result()
    # ['apiVersion', 'modelId', 'stringIndexType', 'content', 'pages', 'tables', 'paragraphs', 'styles', 'contentFormat', 'sections', 'figures']

    content = result["content"]
    sections = result["sections"]
    paragraphs = result["paragraphs"]

    for d in content:
        print(d)
        break

    print("*********************")

    for section in sections:
        print(section)
        break 

    print("*********************")

    for p in paragraphs:
        print(p)
        break
    # print(result.analyzeResults)

    # for page_result in result.analyze_result.document_results:
    #     print(f"Page: {page_result.page_number}")
    #     for paragraph in page_result.paragraphs:
    #         # Print the text content of each paragraph
    #         print(f"Paragraph: {paragraph.content}")
    #         # Check if the paragraph is a header
    #         if paragraph.role == "header":
    #             print(f"Header: {paragraph.content}")

# def format_polygon(polygon):
#     if not polygon:
#         return "N/A"
#     return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

# def analyze_layout():
    

#     document_analysis_client = DocumentAnalysisClient(
#         endpoint=endpoint, credential=AzureKeyCredential(key)
#     )

#     with open(doc_path, "rb") as document:
#         poller = document_analysis_client.begin_analyze_document(
#             "prebuilt-layout",
#             AnalyzeDocumentRequest(document=document),
#             output_content_format=ContentFormat.MARKDOWN
#         )

#     result = poller.result()
#     print(result)

    # for idx, style in enumerate(result.styles):
    #     print(
    #         "Document contains {} content".format(
    #             "handwritten" if style.is_handwritten else "no handwritten"
    #         )
    #     )

# analyze_layout()