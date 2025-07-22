import os
from dotenv import load_dotenv
load_dotenv()
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeOutputOption, AnalyzeResult, AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from io import BytesIO
from flask import jsonify
from pdf2image import convert_from_bytes

def connect_to_azure_doc_intel():
    """
    Connects to Azure Document Intelligence service using environment variables.
    
    Returns:
        document_intelligence_client (DocumentIntelligenceClient): an instance of DocumentIntelligenceClient connected to given Azure account
    
    Notes:
        Assumes that the environment variables DOC_INTELLIGENCE_ENDPOINT and DOC_INTELLIGENCE_KEY are set
    """
    # create a client for azure doc intelligence
    document_intelligence_client = DocumentIntelligenceClient(
                                        endpoint=os.getenv("DOC_INTELLIGENCE_ENDPOINT"), 
                                        credential=AzureKeyCredential(os.getenv("DOC_INTELLIGENCE_KEY"))
                                    )
    return document_intelligence_client

def extract_figures_from_pdf(uploaded_file):
    """
    Takes a file, extracts any figures found using Azure Document Intelligence layout mode, and returns the figure(s)
    Args:
        uploaded_file (string): a path to the file to be processed, expected to be a DOCX or PDF file
    Returns:
        figures (list of ???): a list of figures extracted from the file. If none are found, returns an empty list.

    Notes:
        Figures and images are interchangeable terms here, but Azure Document Intelligence refers to them as figures
    """
    file_bytes = uploaded_file.read()

    # create a client for azure doc intelligence
    document_intelligence_client = connect_to_azure_doc_intel()

    # set options for converter
    doc_to_analyze = AnalyzeDocumentRequest(bytes_source = file_bytes)
    poller = document_intelligence_client.begin_analyze_document(
        model_id="prebuilt-layout",
        analyze_request=doc_to_analyze,
        output=[AnalyzeOutputOption.FIGURES],
        output_content_format = "markdown"
    )
    result = poller.result()
    result_dict = result.as_dict()
    figures = result_dict.get("figures", [])
    return jsonify(result.as_dict())

def convert_pdf_to_image(uploaded_file):
    """
    Converts a PDF file to an image format using pdf2image.
    
    Args:
        uploaded_file (BytesIO): A BytesIO object containing the PDF file data.
    
    Returns:
        list (images): A list of images converted from the PDF.
    """
    images = convert_from_bytes(uploaded_file.read())
    return images