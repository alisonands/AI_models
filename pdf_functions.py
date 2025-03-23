from openai import OpenAI
# from SECRETS import *
from google import genai
from google.genai import types
from mistralai import Mistral
import pathlib
import base64
import anthropic
import re
import os
mistral_api_key = os.getenv('mistral_api_key_render')

# file_path_example = "/Users/alisonandrade/Desktop/open_api_test/test_papers/ame.pdf"
# --------------------------
# --------MISTRAL-----------
# --------------------------
def mistral_pdf_parser(file_path):
    mistral_client = Mistral(api_key=mistral_api_key)

    pages = []
    uploaded_pdf = mistral_client.files.upload(
        file={"file_name":file_path, "content": open(file_path, "rb")},
        purpose="ocr"
    )

    mistral_client.files.retrieve(file_id=uploaded_pdf.id)
    signed_url = mistral_client.files.get_signed_url(file_id=uploaded_pdf.id)

    ocr_response = mistral_client.ocr.process(
        model="mistral-ocr-latest",
        document={"type":"document_url", "document_url":signed_url.url}
        )
    
    for page in ocr_response.pages:
        pages.append(page.markdown)
    return pages #return list of pages in markdown format
