# Customer Onboarding KYC Verification System

An AI-powered document processing system for customer onboarding and KYC (Know Your Customer) verification. This system uses specialized AI agents to analyze documents and extract key information for compliance and verification purposes.

## Features

- **Document Analysis**: AI-powered analysis of PDFs, text files, and other document types
- **Metadata Extraction**: Comprehensive file metadata extraction
- **Text Content Extraction**: PDF text extraction using PyMuPDF and PyPDF2
- **KYC Information Extraction**: Automatic identification of personal information, identification documents, account details, and risk assessment data
- **JSON Output**: Structured analysis results in JSON format
- **Command-Line Interface**: Easy-to-use CLI for processing documents

## Prerequisites

- Python 3.9 or higher
- Google Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google Gemini API key:
   - Get your API key from [Google AI Studio](https://aistudio.google.com/)
   - Add it to the `.env` file:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

## Usage

### Command-Line Interface

Process documents using the command-line interface:

```bash
python main.py documents/file1.pdf documents/file2.txt
```

You can also specify an output file:

```bash
python main.py -o output/my_analysis.json documents/file1.pdf documents/file2.txt
```

### Processing Multiple Files

The system can process multiple files at once:

```bash
python main.py documents/*.pdf documents/*.txt
```

### Output

The system generates a JSON file with comprehensive analysis results, including:
- File metadata
- Extracted text content
- AI-powered document analysis
- Key information extraction
- Risk assessment data

## Test Suite

Run the test suite to verify that all components are working correctly:

```bash
cd ../pytest
python test.py
```

## File Structure

- `agents/`: Directory containing AI agents and processing logic
- `config/`: Configuration files including API keys
- `documents/`: Sample documents for testing
- `output/`: Directory where analysis results are saved
- `main.py`: Command-line interface
- `requirements.txt`: Python dependencies

Sample files for testing (in the `documents/` directory):
  - `sample_kyc_document.pdf`: Sample PDF document for testing
  - `sample_kyc_document.txt`: Sample text document for testing

## Supported File Types

- PDF documents
- Text files
- Other document types (Word, Excel, etc.) - metadata only

## How It Works

1. **File Processing**: The system categorizes files by type and extracts metadata
2. **Text Extraction**: For PDFs, it extracts text content using PyMuPDF
3. **AI Analysis**: Specialized AI agents analyze the content and extract key information
4. **Results Compilation**: All results are compiled into a structured JSON report

## Example Use Cases

- Customer onboarding verification
- KYC compliance processing
- Document analysis for financial institutions
- Automated data extraction from forms