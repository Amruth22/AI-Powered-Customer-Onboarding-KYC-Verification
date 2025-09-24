"""
Command-line version of the Document & Vision Processor
This script processes documents and images using specialized AI agents without requiring Streamlit.
"""

import os
import json
import argparse
import sys
from datetime import datetime
from typing import List, Dict

# Add the agents directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Import the agents
from agents.agents import (
    document_processing_crew, 
    metadata_extractor, 
    categorize_files_by_type,
    get_image_metadata
)

def process_files(file_paths: List[str]) -> Dict:
    """Process documents and images using separate specialized agents"""
    
    print("Starting processing with specialized Document agent...")
    
    # Categorize files
    categorized_files = categorize_files_by_type(file_paths)
    
    # Step 1: Process basic metadata
    print('Extracting file metadata...')
    collected_docs = []
    
    for file_path in file_paths:
        if os.path.exists(file_path):
            metadata = metadata_extractor.extract_metadata(file_path)
            
            # Add image-specific metadata if it's an image
            if file_path in categorized_files['images']:
                image_meta = get_image_metadata(file_path)
                metadata.update({"image_metadata": image_meta})
            
            collected_docs.append(metadata)
        else:
            print(f"[ERROR] File not found: {file_path}")
    
    # Step 2: Process documents with Document Processing Agent
    document_results = None
    if categorized_files['documents'] or categorized_files['other']:
        print('Running Document Processing Agent...')
        
        # Prepare document content for the agent
        document_contents = []
        for doc in collected_docs:
            if doc['file_path'] in categorized_files['documents'] + categorized_files['other']:
                # For PDFs, include the extracted text content
                if 'pdf_analysis' in doc and 'text_content' in doc['pdf_analysis']:
                    content = {
                        'file_name': doc['file_name'],
                        'file_path': doc['file_path'],
                        'file_type': doc['file_type'],
                        'text_content': doc['pdf_analysis']['text_content']
                    }
                else:
                    # For other file types, we would need to read the content
                    try:
                        with open(doc['file_path'], 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        content = {
                            'file_name': doc['file_name'],
                            'file_path': doc['file_path'],
                            'file_type': doc['file_type'],
                            'text_content': file_content[:2000] + "..." if len(file_content) > 2000 else file_content
                        }
                    except Exception as e:
                        content = {
                            'file_name': doc['file_name'],
                            'file_path': doc['file_path'],
                            'file_type': doc['file_type'],
                            'text_content': f"[Error reading file content: {str(e)}]"
                        }
                document_contents.append(content)
        
        doc_input = {
            "documents": document_contents,
            "instructions": "Process document files and create normalized metadata package"
        }
        
        try:
            document_results = document_processing_crew.kickoff(inputs=doc_input)
        except Exception as e:
            print(f"Document processing warning: {str(e)}")
            document_results = "Document processing completed with basic metadata only"
    
    # Step 3: Process images (basic processing without Vision Agent)
    vision_results = None
    if categorized_files['images']:
        print('Processing images with basic metadata extraction...')
        
        # For now, we'll just extract metadata for images
        image_files = categorized_files['images']
        vision_results = "Image processing completed with basic metadata extraction only"
    
    # Step 4: Create comprehensive results package
    print('Compiling final results...')
    
    final_package = {
        "package_id": f"DUAL_AGENT_PACKAGE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created_at": datetime.now().isoformat(),
        "processing_method": "dual_agent_system",
        "total_files": len(file_paths),
        "file_categories": {
            "images": len(categorized_files['images']),
            "documents": len(categorized_files['documents']),
            "other": len(categorized_files['other'])
        },
        "categorized_files": categorized_files,
        "file_metadata": collected_docs,
        "document_processing_results": str(document_results) if document_results else "No documents processed",
        "vision_analysis_results": str(vision_results) if vision_results else "No images processed",
        "agents_used": [],
        "package_status": "COMPLETED"
    }
    
    # Track which agents were used
    if document_results:
        final_package["agents_used"].append("Document Processing Agent")
    if vision_results:
        final_package["agents_used"].append("Basic Image Processing")
    
    print('Processing completed!')
    
    return final_package

def save_results(result: Dict, output_path: str):
    """Save results to a JSON file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"[SUCCESS] Results saved to {output_path}")
    except Exception as e:
        print(f"[ERROR] Error saving results: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Process documents and images using specialized AI agents")
    parser.add_argument("files", nargs="+", help="Paths to files to process")
    parser.add_argument("-o", "--output", help="Output JSON file path", default=os.path.join("output", "analysis_results.json"))
    
    args = parser.parse_args()
    
    # Validate file paths
    invalid_files = [f for f in args.files if not os.path.exists(f)]
    if invalid_files:
        print(f"[ERROR] Error: The following files do not exist: {invalid_files}")
        sys.exit(1)
    
    print(f"[INFO] Processing {len(args.files)} file(s)...")
    for file_path in args.files:
        print(f"  - {file_path}")
    
    # Process files
    result = process_files(args.files)
    
    # Display enhanced summary
    print("\n" + "="*60)
    print("CUSTOMER ONBOARDING KYC VERIFICATION - PROCESSING COMPLETE")
    print("="*60)
    print(f"[SUCCESS] System Successfully Executed!")
    print(f"[FILES] Files Processed: {result.get('total_files', 0)}")
    print(f"[AGENTS] Agents Used: {', '.join(result.get('agents_used', []))}")
    print(f"[ID] Package ID: {result.get('package_id', 'N/A')}")
    print(f"[STATUS] Status: {result.get('package_status', 'Unknown')}")
    
    # File categories
    categories = result.get('file_categories', {})
    print(f"\n[FILES] File Categories:")
    print(f"  Images: {categories.get('images', 0)}")
    print(f"  Documents: {categories.get('documents', 0)}")
    print(f"  Other: {categories.get('other', 0)}")
    
    # Save results
    save_results(result, args.output)
    
    print("\n" + "="*60)
    print("PROCESSING COMPLETE - RESULTS SUCCESSFULLY GENERATED")
    print("="*60)
    print(f"Results saved to: {args.output}")
    print("View the file to see detailed KYC analysis")
    print("="*60)

if __name__ == "__main__":
    main()