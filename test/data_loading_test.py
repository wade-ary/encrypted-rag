import pytest
import sys, os
sys.path.append(os.path.abspath(os.getcwd()))
from data_setup.document_loader.pdf_loader import PDFLoader
from data_setup.document_loader.docx_loader import DocxLoader
from data_setup.document_loader.txt_loader import TxtLoader
import os
import sys, os
SAMPLE_DIR = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/test/sample_text"

# ---------- PDF ----------
def test_pdf_loader_extracts_text():
    loader = PDFLoader()
    file_path = os.path.join(SAMPLE_DIR, "testing_doc.pdf")
    
    text = loader.load(file_path)
    metadata = loader.get_metadata(file_path)
    
    assert isinstance(text, str)
    assert len(text.strip()) > 0
    assert "file_type" in metadata and metadata["file_type"] == "pdf"
    assert "filename" in metadata
    assert metadata["filename"].endswith(".pdf")


# ---------- DOCX ----------
def test_docx_loader_extracts_text():
    loader = DocxLoader()
    file_path = os.path.join(SAMPLE_DIR, "testing_doc.docx")
    
    text = loader.load(file_path)
    metadata = loader.get_metadata(file_path)
    
    assert isinstance(text, str)
    assert len(text.strip()) > 0
    assert "file_type" in metadata and metadata["file_type"] == "docx"
    assert "filename" in metadata
    assert metadata["filename"].endswith(".docx")


# ---------- TXT ----------
def test_txt_loader_extracts_text():
    loader = TxtLoader()
    file_path = os.path.join(SAMPLE_DIR, "testing_doc.txt")
    
    text = loader.load(file_path)
    metadata = loader.get_metadata(file_path)
    
    assert isinstance(text, str)
    assert len(text.strip()) > 0
    assert "file_type" in metadata and metadata["file_type"] == "txt"
    assert "filename" in metadata
    assert metadata["filename"].endswith(".txt")


# ---------- ERROR HANDLING ----------
def test_invalid_file_type_raises_error():
    pdf_loader = PDFLoader()
    docx_loader = DocxLoader()
    txt_loader = TxtLoader()

    # Create a dummy path with wrong extension
    invalid_file = os.path.join(SAMPLE_DIR, "testing_doc.xyz")

    with pytest.raises(ValueError):
        pdf_loader.load(invalid_file)
    with pytest.raises(ValueError):
        docx_loader.load(invalid_file)
    with pytest.raises(ValueError):
        txt_loader.load(invalid_file)

print("HAHA")