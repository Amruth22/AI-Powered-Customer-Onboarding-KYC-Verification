# Customer Onboarding KYC Verification System - Student Project Template

**Learning Project**: Build an AI-powered document processing system for customer onboarding and KYC (Know Your Customer) verification. You will create specialized AI agents to analyze documents and extract key information for compliance and verification purposes.

## Features You Will Implement

- **Document Analysis**: Build AI-powered analysis of PDFs, text files, and other document types
- **Metadata Extraction**: Implement comprehensive file metadata extraction
- **Text Content Extraction**: Create PDF text extraction using PyMuPDF and PyPDF2
- **KYC Information Extraction**: Develop automatic identification of personal information, identification documents, account details, and risk assessment data
- **JSON Output**: Generate structured analysis results in JSON format
- **Command-Line Interface**: Build easy-to-use CLI for processing documents

## Prerequisites

- Python 3.9 or higher
- Google Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/))
- Understanding of CrewAI framework
- Basic knowledge of document processing and AI agents

## Getting Started

### Setup Instructions
1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google Gemini API key:
   - Get your API key from [Google AI Studio](https://aistudio.google.com/)
   - Create a `config/.env` file:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

4. Start implementing the empty template files following the instructions below

### Testing Your Implementation
- Run tests: `python tests.py`
- Test with sample documents: `python main.py documents/sample_kyc_document.pdf`
- Process multiple files: `python main.py documents/*.pdf documents/*.txt`

## Project Structure & Implementation Guide

**Your Task**: Implement the functionality in each of these files. The structure is provided, but the files contain only templates and TODOs.

```
AI-Powered-Customer-Onboarding-KYC-Verification/
├── agents/                         # AI agent implementations
│   ├── __init__.py                # Package initialization
│   └── agents.py                  # IMPLEMENT: CrewAI agents and tools
│
├── documents/                      # Sample documents and test files
│   ├── sample_kyc_document.pdf    # Sample PDF for testing
│   ├── sample_kyc_document copy.pdf # Backup sample PDF
│   └── sample_kyc_document.txt    # Sample text document
│
├── config/                        # Configuration directory
│   └── .env                       # CREATE: Environment configuration
│
├── output/                        # Output directory
│   └── analysis_results.json      # Generated analysis results
│
├── main.py                        # IMPLEMENT: Command-line interface
├── agents.py                      # IMPLEMENT: Legacy agent definitions
├── tests.py                      # IMPLEMENT: Comprehensive test suite
├── requirements.txt              # Python dependencies
├── sample_kyc_document.pdf       # Root-level sample PDF
├── sample_kyc_document copy.pdf  # Root-level backup PDF
├── sample_kyc_document.txt       # Root-level sample text
├── test_kyc_document.txt         # Test document for validation
├── README.md                     # This file
└── ARCHITECTURE.md               # System architecture documentation
```

## Implementation Instructions by Component

### Core Components to Implement

#### `agents/agents.py`
**Implement**: CrewAI agents and document processing tools
- Create `EnhancedMetadataExtractorTool` class
  - Implement `extract_metadata(file_path)` method
  - Add PDF content extraction using PyMuPDF and PyPDF2 fallback
  - Create file type determination logic
  - Build comprehensive metadata analysis
- Create `document_processor_agent` using CrewAI Agent
  - Define role as "Advanced Document Content Analyzer"
  - Set goal for KYC document analysis and information extraction
  - Configure with Gemini 2.0 Flash LLM
- Implement `enhanced_document_processing_task`
  - Create task for document content analysis
  - Define KYC-specific information extraction requirements
  - Set expected output format
- Build utility functions:
  - `categorize_files_by_type()`: File categorization logic
  - `get_image_metadata()`: Image metadata extraction

#### `main.py`
**Implement**: Command-line interface and orchestration
- Create `process_files(file_paths)` function
  - Implement file categorization workflow
  - Build metadata extraction pipeline
  - Integrate CrewAI agent processing
  - Create comprehensive results compilation
- Implement `save_results(result, output_path)` function
  - JSON output generation and formatting
  - Error handling for file operations
- Build command-line argument parsing
  - File path validation
  - Output path configuration
  - Help and usage information
- Create main execution workflow
  - File processing orchestration
  - Results display and summary
  - Error handling and reporting

#### `tests.py`
**Implement**: Comprehensive test suite
- Create `TestCustomerOnboardingKYC` class
- Implement test methods:
  - `test_env_api_key_configuration()`: Environment setup validation
  - `test_metadata_extraction()`: File metadata extraction testing
  - `test_file_categorization()`: File type categorization testing
  - `test_crew_initialization()`: CrewAI agent initialization testing
  - `test_document_processing()`: End-to-end document processing
  - `test_output_json_generation()`: JSON output validation
- Add test fixtures and sample data
- Implement comprehensive error scenario testing

### KYC-Specific Implementation Requirements

#### Document Analysis Features
**Your Task**: Implement AI-powered analysis to extract:

**Personal Information**:
- Full name and aliases
- Date of birth
- Address (current and previous)
- Phone numbers and email addresses
- Nationality and citizenship

**Identification Documents**:
- ID numbers (passport, driver's license, national ID)
- Issue and expiration dates
- Issuing authorities
- Document verification status

**Account Information**:
- Account types and purposes
- Initial deposit amounts
- Source of funds documentation
- Expected transaction volumes

**Risk Assessment Data**:
- Customer risk level classification
- PEP (Politically Exposed Person) status
- Sanctions screening results
- AML (Anti-Money Laundering) flags

**Compliance Verification**:
- Declaration completeness
- Signature validation
- Document authenticity checks
- Regulatory compliance status

### Technical Implementation Details

#### PDF Processing Implementation
**Your Task**: Build robust PDF processing with:
- **Primary Method**: PyMuPDF (fitz) for advanced text extraction
- **Fallback Method**: PyPDF2 for compatibility
- **Features to Implement**:
  - Page-by-page text extraction
  - Image detection and counting
  - Text statistics (character count, word count)
  - Page analysis and structure detection
  - Error handling with graceful degradation

#### CrewAI Agent Configuration
**Your Task**: Configure AI agents with:
- **LLM Integration**: Gemini 2.0 Flash model
- **Agent Role**: Advanced Document Content Analyzer
- **Task Definition**: Structured KYC information extraction
- **Output Format**: JSON-structured analysis results
- **Error Handling**: Comprehensive error recovery

#### File Processing Pipeline
**Your Task**: Build processing workflow:
1. **File Categorization**: Classify by type (documents, images, other)
2. **Metadata Extraction**: Extract comprehensive file information
3. **Content Processing**: Analyze document content with AI
4. **Results Compilation**: Generate structured output
5. **Quality Assurance**: Validate and verify results

## Learning Objectives

By completing this project, you will learn:

### Technical Skills
- **CrewAI Framework**: Multi-agent system development and orchestration
- **Document Processing**: Advanced PDF and text file processing techniques
- **AI Integration**: Large Language Model integration with Gemini AI
- **Metadata Extraction**: Comprehensive file analysis and information extraction
- **JSON Processing**: Structured data generation and manipulation
- **Error Handling**: Robust error handling and graceful degradation

### Domain Knowledge
- **KYC Processes**: Know Your Customer verification procedures
- **Compliance Requirements**: Financial services regulatory compliance
- **Document Analysis**: Automated document processing and validation
- **Risk Assessment**: Customer risk profiling and classification
- **Data Extraction**: Intelligent information extraction from unstructured documents

### Software Engineering Practices
- **Modular Design**: Clean architecture with separation of concerns
- **Testing Strategies**: Comprehensive unit and integration testing
- **Configuration Management**: Environment-based configuration
- **Command-Line Interfaces**: Professional CLI development
- **Documentation**: Technical documentation and architecture design

## Submission Guidelines

### Implementation Requirements
1. All core components must be fully implemented
2. CrewAI agents must be properly configured and functional
3. PDF processing must work with both PyMuPDF and PyPDF2 fallback
4. KYC information extraction must be comprehensive and accurate
5. JSON output must be properly structured and validated
6. Command-line interface must be fully functional
7. All tests must pass successfully

### Code Quality Standards
- Follow PEP 8 Python style guidelines
- Include comprehensive docstrings for all classes and methods
- Implement robust error handling throughout the system
- Add type hints where appropriate
- Write clear and maintainable code

### Testing Requirements
- All unit tests must pass: `python tests.py`
- System must process sample documents successfully
- Error handling must be comprehensive
- Output JSON must be valid and well-structured

### Documentation Requirements
- Code must be well-documented with clear comments
- README updates with implementation notes
- Architecture understanding demonstrated through code organization

## Dependencies

**Required Python Packages** (already in requirements.txt):
- Python 3.9+
- crewai>=0.11.0
- python-dotenv>=1.0.0
- Pillow>=10.0.0
- PyPDF2>=3.0.1
- PyMuPDF>=1.23.0

**External Services Required**:
- Google Gemini API Key from AI Studio

## Additional Resources

- **Architecture Documentation**: See `ARCHITECTURE.md` for detailed system design
- **CrewAI Documentation**: [CrewAI Official Docs](https://docs.crewai.com/)
- **Gemini AI Documentation**: [Google AI Studio](https://aistudio.google.com/)
- **PyMuPDF Documentation**: [PyMuPDF Docs](https://pymupdf.readthedocs.io/)

---

**Good luck building your AI-Powered KYC Verification System!**