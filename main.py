from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server
mcp = FastMCP("AI Sticky Notes")

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")

@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the sticky note file.

    Args:
        message (str): The note content to be added.

    Returns:
        str: Confirmation message indicating the note was saved.
    """
    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note saved!"

@mcp.tool()
def read_notes() -> str:
    """
    Read and return all notes from the sticky note file.

    Returns:
        str: All notes as a single string separated by line breaks.
             If no notes exist, a default message is returned.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    return content or "No notes yet."

@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the most recently added note from the sticky note file.

    Returns:
        str: The last note entry. If no notes exist, a default message is returned.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes yet."

@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize all current notes.

    Returns:
        str: A prompt string that includes all notes and asks for a summary.
             If no notes exist, a message will be shown indicating that.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    if not content:
        return "There are no notes yet."

    return f"Summarize the current notes: {content}"

# from mcp.server.fastmcp import FastMCP
# from typing import List, Dict, Optional
# import sqlite3
# from datetime import datetime
# import os
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# import json
# import io

# # Mock database for demonstration
# patients_db = {
#     "P001": {
#         "name": "John Doe",
#         "age": 45,
#         "departments": {
#             "cardiology": {
#                 "last_visit": "2025-09-15",
#                 "diagnosis": "Hypertension",
#                 "medications": ["Lisinopril", "Amlodipine"]
#             },
#             "orthopedics": {
#                 "last_visit": "2025-08-20",
#                 "diagnosis": "Osteoarthritis",
#                 "medications": ["Ibuprofen"]
#             }
#         }
#     },
#     "P002": {
#         "name": "Jane Smith",
#         "age": 32,
#         "departments": {
#             "neurology": {
#                 "last_visit": "2025-10-01",
#                 "diagnosis": "Migraine",
#                 "medications": ["Sumatriptan"]
#             }
#         }
#     }
# }

# # Google Drive setup
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# def get_google_drive_service():
#     creds = None
#     if os.path.exists('token.json'):
#         with open('token.json', 'r') as token:
#             creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
#     if not creds or not creds.valid:
#         flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
    
#     return build('drive', 'v3', credentials=creds)

# # Create MCP server
# mcp = FastMCP("HealthcareInfoSystem")

# # Tool: Get Patient Basic Information
# @mcp.tool()
# def get_patient_info(patient_id: str) -> str:
#     """Retrieve basic information about a patient"""
#     patient = patients_db.get(patient_id)
#     if patient:
#         return f"Patient {patient_id}: {patient['name']}, Age: {patient['age']}"
#     return "Patient ID not found."

# # Tool: Get Department History
# @mcp.tool()
# def get_department_history(patient_id: str, department: str) -> str:
#     """Get patient's history from a specific department"""
#     patient = patients_db.get(patient_id)
#     if not patient:
#         return "Patient ID not found."
    
#     dept_info = patient['departments'].get(department.lower())
#     if not dept_info:
#         return f"No records found for {department} department."
    
#     return f"""
# Patient: {patient['name']}
# Department: {department}
# Last Visit: {dept_info['last_visit']}
# Diagnosis: {dept_info['diagnosis']}
# Current Medications: {', '.join(dept_info['medications'])}
# """

# # Tool: Get All Department Records
# @mcp.tool()
# def get_all_departments(patient_id: str) -> str:
#     """Get patient's history from all departments"""
#     patient = patients_db.get(patient_id)
#     if not patient:
#         return "Patient ID not found."
    
#     departments = list(patient['departments'].keys())
#     return f"Patient {patient['name']} has records in: {', '.join(departments)}"

# # Tool: Search Medical Documents
# @mcp.tool()
# def search_medical_documents(patient_id: str, document_type: str) -> str:
#     """Search for patient's medical documents in Google Drive"""
#     try:
#         service = get_google_drive_service()
        
#         # Search in the specific folder for patient documents
#         query = f"name contains '{patient_id}' and name contains '{document_type}'"
#         results = service.files().list(
#             q=query,
#             pageSize=10,
#             fields="files(id, name, modifiedTime)"
#         ).execute()
        
#         files = results.get('files', [])
#         if not files:
#             return f"No {document_type} documents found for patient {patient_id}"
        
#         response = f"Found {len(files)} {document_type} document(s):\n"
#         for file in files:
#             response += f"- {file['name']} (Last modified: {file['modifiedTime']})\n"
#         return response
        
#     except Exception as e:
#         return f"Error accessing documents: {str(e)}"

# # Tool: Get Latest Lab Results
# @mcp.tool()
# def get_latest_lab_results(patient_id: str, test_type: Optional[str] = None) -> str:
#     """Retrieve patient's latest laboratory results"""
#     try:
#         service = get_google_drive_service()
        
#         # Search for lab results in Drive
#         query = f"name contains '{patient_id}' and name contains 'LAB'"
#         if test_type:
#             query += f" and name contains '{test_type}'"
            
#         results = service.files().list(
#             q=query,
#             pageSize=1,
#             orderBy="modifiedTime desc",
#             fields="files(id, name, modifiedTime)"
#         ).execute()
        
#         files = results.get('files', [])
#         if not files:
#             return "No lab results found."
            
#         file = files[0]
#         file_id = file['id']
        
#         # Download the content
#         request = service.files().get_media(fileId=file_id)
#         fh = io.BytesIO()
#         downloader = MediaIoBaseDownload(fh, request)
#         done = False
#         while done is False:
#             status, done = downloader.next_chunk()
            
#         content = fh.getvalue().decode('utf-8')
#         return f"Latest lab results from {file['modifiedTime']}:\n{content}"
        
#     except Exception as e:
#         return f"Error retrieving lab results: {str(e)}"

# # Resource: Greeting
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}! How can I assist you with patient information today?"

# if __name__ == "__main__":
#     # Configure the server to run on the standard Claude Desktop port
#     mcp.run(host="localhost", port=5004)