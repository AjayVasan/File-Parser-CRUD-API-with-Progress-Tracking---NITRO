# File Parser CRUD API

A Flask-based REST API that supports uploading, storing, parsing, and retrieving files with real-time progress tracking. The application provides complete CRUD functionality for file management with support for various file formats.

## Features

- ✅ **File Upload** - Support for multipart file uploads with unique ID assignment
- ✅ **Progress Tracking** - Real-time upload and processing progress monitoring
- ✅ **File Parsing** - Automatic content extraction using LlamaIndex
- ✅ **CRUD Operations** - Complete Create, Read, Update, Delete functionality
- ✅ **Metadata Storage** - File information including size, type, and timestamps
- ✅ **Error Handling** - Comprehensive error responses and validation

## Tech Stack

- **Backend Framework**: Flask
- **File Parsing**: LlamaIndex Core
- **Storage**: Local file system
- **Data Format**: JSON responses

## API Endpoints

### 1. Upload File
```http
POST /files
Content-Type: multipart/form-data

Body: file (form-data)
```

**Success Response (200):**
```json
{
  "message": "File uploaded successfully",
  "file id": 1234,
  "filename": "document.pdf",
  "File Type": "application/pdf",
  "File size": "2.45 MB",
  "Date Created": "2024-01-15T10:30:00"
}
```

**Error Response (400):**
```json
{
  "message": "File already uploaded",
  "Metadata": {
    "file id": 1234,
    "filename": "document.pdf",
    "status": "ready to use",
    "size": "2.45 MB",
    "progress": "100%"
  }
}
```

### 2. Get Upload Progress
```http
GET /files/{file_id}/progress
```

**Response (200):**
```json
{
  "file id": 1234,
  "filename": "document.pdf",
  "status": "processing",
  "Size": "2.45 MB",
  "Progress": "75%"
}
```

**Status Values:**
- `uploading` - File is being uploaded (0-19%)
- `processing` - File is being processed (20-99%)
- `ready to use` - File is ready for retrieval (100%)

### 3. Get File Content
```http
GET /files/{file_id}/
```

**Response (200):**
```json
{
  "file id": 1234,
  "filename": "document.pdf",
  "File Type": "application/pdf",
  "File size": "2.45 MB",
  "Date Created": "2024-01-15T10:30:00",
  "file content": [
    {
      "doc_id": "uuid-string",
      "text": "Extracted file content...",
      "metadata": {
        "page_label": "1",
        "text": "Page content..."
      }
    }
  ]
}
```

### 4. List All Files
```http
GET /files
```

**Response (200):**
```json
{
  "Complete Data Info": {
    "1234": ["document.pdf", "application/pdf", "2.45 MB", "2024-01-15T10:30:00"],
    "5678": ["spreadsheet.xlsx", "application/xlsx", "1.23 MB", "2024-01-15T11:00:00"]
  }
}
```

### 5. Delete File
```http
DELETE /files/{file_id}
```

**Response (200):**
```json
{
  "message": "File '/document.pdf' deleted successfully."
}
```

**Error Response (404):**
```json
{
  "error": "unknown file_id"
}
```

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/file-parser-crud-api.git
cd file-parser-crud-api
```

### 2. Install Dependencies
```bash
pip install flask llama-index-core
```

### 3. Configure Upload Directory
Update the `UPLOAD_FOLDER` path in the code to match your system:
```python
UPLOAD_FOLDER = 'C:/Users/kowsh/OneDrive/Desktop/NITRO'  # Update this path
```

### 4. Run the Application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Usage Examples

### Upload a File
```bash
curl -X POST \
  http://localhost:5000/files \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/document.pdf'
```

### Check Progress
```bash
curl -X GET http://localhost:5000/files/1234/progress
```

### Retrieve File Content
```bash
curl -X GET http://localhost:5000/files/1234/
```

### List All Files
```bash
curl -X GET http://localhost:5000/files
```

### Delete a File
```bash
curl -X DELETE http://localhost:5000/files/1234
```

## Project Structure
```
file-parser-crud-api/
│
├── app.py                 # Main Flask application
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── uploads/             # Directory for uploaded files (created automatically)
```

## Features Implemented

### ✅ Core Requirements
- [x] File upload with unique ID assignment
- [x] Progress tracking with status updates
- [x] Asynchronous file parsing simulation
- [x] Complete CRUD operations
- [x] Error handling and validation
- [x] JSON API responses

### ⚡ Additional Features
- [x] File size calculation and display
- [x] Timestamp tracking
- [x] Duplicate file detection
- [x] Automatic directory creation
- [x] Content type detection

## Error Handling

The API provides comprehensive error handling:

- **404 Not Found**: Invalid file ID
- **400 Bad Request**: Missing file or duplicate upload
- **500 Internal Server Error**: Server-side processing errors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Note**: This is a demonstration project. For production use, consider implementing additional security measures, database integration, and proper authentication mechanisms.
