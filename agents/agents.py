"""
Agents for processing documents and images without requiring specific tools that may not be available.
"""

from crewai import Agent, Task, Crew, LLM
from datetime import datetime
from typing import Dict, List
import os
from dotenv import load_dotenv
import base64
from PIL import Image
import io
import PyPDF2
import fitz  # PyMuPDF for better PDF processing

# Load environment variables
# Specify the path to the .env file explicitly since we've reorganized the directory structure
env_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path=env_path)

class EnhancedMetadataExtractorTool:
    def __init__(self):
        self.name = "enhanced_metadata_extractor"
        self.description = "Extracts comprehensive metadata and content from uploaded documents"
    
    def extract_metadata(self, file_path: str) -> Dict:
        """Extract comprehensive metadata from a file including content analysis"""
        try:
            file_stats = os.stat(file_path)
            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1]
            
            base_metadata = {
                "file_name": file_name,
                "file_path": file_path,
                "file_size": file_stats.st_size,
                "file_extension": file_extension,
                "created_date": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                "modified_date": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                "file_type": self._determine_file_type(file_extension)
            }
            
            # Add content analysis for PDFs
            if file_extension.lower() == '.pdf':
                pdf_content = self._extract_pdf_content(file_path)
                base_metadata.update(pdf_content)
            
            return base_metadata
        except Exception as e:
            return {"error": f"Failed to extract metadata: {str(e)}"}
    
    def _determine_file_type(self, extension: str) -> str:
        """Determine file category based on extension"""
        doc_types = {
            '.pdf': 'PDF Document',
            '.doc': 'Word Document',
            '.docx': 'Word Document',
            '.txt': 'Text File',
            '.xlsx': 'Excel Spreadsheet',
            '.xls': 'Excel Spreadsheet',
            '.pptx': 'PowerPoint Presentation',
            '.jpg': 'Image',
            '.jpeg': 'Image',
            '.png': 'Image',
            '.gif': 'Image',
            '.bmp': 'Image',
            '.tiff': 'Image'
        }
        return doc_types.get(extension.lower(), 'Unknown')
    
    def _extract_pdf_content(self, file_path: str) -> Dict:
        """Extract detailed content from PDF files"""
        try:
            # Use PyMuPDF for better content extraction
            doc = fitz.open(file_path)
            
            content_analysis = {
                "pdf_analysis": {
                    "total_pages": len(doc),
                    "has_text": False,
                    "has_images": False,
                    "text_content": "",
                    "page_details": [],
                    "extraction_method": "PyMuPDF"
                }
            }
            
            full_text = ""
            total_images = 0
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                page_text = page.get_text()
                full_text += page_text + "\n"
                
                # Check for images
                image_list = page.get_images()
                page_images = len(image_list)
                total_images += page_images
                
                content_analysis["pdf_analysis"]["page_details"].append({
                    "page_number": page_num + 1,
                    "text_length": len(page_text),
                    "has_text": len(page_text.strip()) > 0,
                    "image_count": page_images
                })
            
            # Update analysis
            content_analysis["pdf_analysis"]["has_text"] = len(full_text.strip()) > 0
            content_analysis["pdf_analysis"]["has_images"] = total_images > 0
            content_analysis["pdf_analysis"]["total_images"] = total_images
            content_analysis["pdf_analysis"]["text_content"] = full_text[:2000] + "..." if len(full_text) > 2000 else full_text
            content_analysis["pdf_analysis"]["character_count"] = len(full_text)
            content_analysis["pdf_analysis"]["word_count"] = len(full_text.split())
            
            doc.close()
            return content_analysis
            
        except Exception as e:
            # Fallback to PyPDF2 if PyMuPDF fails
            try:
                return self._extract_pdf_content_fallback(file_path)
            except Exception as e2:
                return {
                    "pdf_analysis": {
                        "error": f"PDF extraction failed: {str(e)} | Fallback error: {str(e2)}",
                        "extraction_method": "failed"
                    }
                }
    
    def _extract_pdf_content_fallback(self, file_path: str) -> Dict:
        """Fallback PDF extraction using PyPDF2"""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            content_analysis = {
                "pdf_analysis": {
                    "total_pages": len(pdf_reader.pages),
                    "extraction_method": "PyPDF2_fallback",
                    "text_content": "",
                    "has_text": False
                }
            }
            
            full_text = ""
            for page in pdf_reader.pages:
                try:
                    text = page.extract_text()
                    full_text += text + "\n"
                except:
                    continue
            
            content_analysis["pdf_analysis"]["text_content"] = full_text[:2000] + "..." if len(full_text) > 2000 else full_text
            content_analysis["pdf_analysis"]["has_text"] = len(full_text.strip()) > 0
            content_analysis["pdf_analysis"]["character_count"] = len(full_text)
            content_analysis["pdf_analysis"]["word_count"] = len(full_text.split())
            
            return content_analysis

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini LLM
gemini_llm = LLM(
    model='gemini/gemini-2.0-flash',
    api_key=api_key,
    temperature=0.0
)

# Enhanced Document Processing Agent
document_processor_agent = Agent(
    role='Advanced Document Content Analyzer',
    goal='Extract, analyze, and summarize comprehensive content from documents including text extraction, structure analysis, and content insights',
    backstory="""You are an advanced document content analyzer with expertise in extracting and analyzing 
    information from various document types. You can read PDF files, extract text content, analyze document 
    structure, identify key information, and provide comprehensive content summaries. You are particularly 
    skilled at understanding document context, extracting important data points, and organizing information 
    in a meaningful way. You work with file content directly and provide detailed analysis of what documents contain.""",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# Enhanced Document Processing Task
enhanced_document_processing_task = Task(
    description="""
    You will receive a list of documents with their content. Your task is to:
    
    1. ANALYZE each document's text content
    2. IDENTIFY key information, important data points, and document structure
    3. SUMMARIZE the main content and purpose of each document
    4. EXTRACT actionable insights and important details
    5. ORGANIZE findings in a structured, comprehensive report
    
    For each document, pay special attention to:
    - Main topics and themes
    - Important data, numbers, or statistics
    - Key names, dates, and locations
    - Document purpose and type (form, report, certificate, etc.)
    - Any structured data or tables
    
    Provide detailed analysis of the actual document content.
    
    Documents to analyze:
    {documents}
    
    Output: Comprehensive document content analysis with key findings, important information, and actionable insights for each processed document.
    """,
    agent=document_processor_agent,
    expected_output="Detailed document content analysis report with extracted information, key findings, document summary, and actionable insights for each processed document"
)

# Enhanced Crews
document_processing_crew = Crew(
    agents=[document_processor_agent], 
    tasks=[enhanced_document_processing_task],  
    verbose=True,
    manager_llm=gemini_llm
)

# Utility functions
def categorize_files_by_type(file_paths: List[str]) -> Dict[str, List[str]]:
    """Categorize files into different types for processing"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    document_extensions = ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx']
    
    categorized = {
        'images': [],
        'documents': [],
        'other': []
    }
    
    for file_path in file_paths:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in image_extensions:
            categorized['images'].append(file_path)
        elif ext in document_extensions:
            categorized['documents'].append(file_path)
        else:
            categorized['other'].append(file_path)
    
    return categorized

def get_image_metadata(image_path: str) -> Dict:
    """Get detailed metadata for image files"""
    try:
        with Image.open(image_path) as img:
            return {
                "dimensions": f"{img.size[0]}x{img.size[1]}",
                "format": img.format,
                "mode": img.mode,
                "has_transparency": img.mode in ('RGBA', 'LA') or 'transparency' in img.info
            }
    except Exception as e:
        return {"error": f"Could not read image metadata: {str(e)}"}

# Export the enhanced metadata extractor
metadata_extractor = EnhancedMetadataExtractorTool()