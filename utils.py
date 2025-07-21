import os
from dotenv import load_dotenv
load_dotenv()
from azure.ai.documentintelligence import DocumentIntelligenceClient
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