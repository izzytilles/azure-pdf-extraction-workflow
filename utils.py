import os
from dotenv import load_dotenv
load_dotenv()
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeOutputOption, AnalyzeResult
from azure.core.credentials import AzureKeyCredential

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

    # create a client for azure doc intelligence
    document_intelligence_client = connect_to_azure_doc_intel()

    # set options for converter
    with open(uploaded_file, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            body=f,
            output=[AnalyzeOutputOption.FIGURES],
        )
    result: AnalyzeResult = poller.result()

    if result.figures:
        return result.figures
    else:
        print("No figures found in the document.")
        return []
