import requests
import os
from pathlib import Path
from datetime import datetime
import hashlib

# Configuration
DOWNLOAD_FOLDER = Path("downloaded_pdfs")
LOG_FILE = Path("README.md")

def ensure_folder_exists():
    """Create download folder if it doesn't exist"""
    DOWNLOAD_FOLDER.mkdir(exist_ok=True)

def download_pdf(url, filename=None):
    """Download a PDF from URL with timestamp"""
    try:
        print(f"📥 Downloading: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Check if it's actually a PDF
        if 'application/pdf' not in response.headers.get('content-type', ''):
            print(f"⚠️  Warning: {url} might not be a PDF")
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not filename:
            # Extract base name from URL
            base_name = url.split('/')[-1]
            if 'export=download' in url:  # Handle Google Drive URLs
                base_name = "document"
            if not base_name or base_name == 'download':
                base_name = "pdf_file"
            
            # Remove .pdf extension if it exists, we'll add it with timestamp
            if base_name.endswith('.pdf'):
                base_name = base_name[:-4]
            
            filename = f"{base_name}_{timestamp}.pdf"
        else:
            # Add timestamp to provided filename
            name_parts = filename.rsplit('.', 1)
            if len(name_parts) == 2 and name_parts[1].lower() == 'pdf':
                filename = f"{name_parts[0]}_{timestamp}.pdf"
            else:
                filename = f"{filename}_{timestamp}.pdf"
        
        filepath = DOWNLOAD_FOLDER / filename
        
        # Save the PDF (no duplicate checking since we use timestamps)
        filepath.write_bytes(response.content)
        file_size = len(response.content)
        
        print(f"✅ Downloaded: {filename} ({file_size:,} bytes)")
        return True, filename, file_size
        
    except Exception as e:
        print(f"❌ Error downloading {url}: {str(e)}")
        return False, None, 0

def update_log(downloads):
    """Update the download log"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_str = now.strftime("%B %d, %Y")
    
    if LOG_FILE.exists():
        content = LOG_FILE.read_text(encoding="utf-8")
    else:
        content = """# 📄 PDF Download Log

Automated PDF downloads via GitHub Actions

## 📊 Download Statistics
- **Total Downloads:** 0
- **Last Run:** Never
- **Status:** 🟢 Active

## 📝 Recent Downloads
"""
    
    # Count successful downloads
    successful_downloads = sum(1 for success, _, _ in downloads if success)
    total_size = sum(size for success, _, size in downloads if success)
    
    # Update statistics in header
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('- **Last Run:**'):
            lines[i] = f'- **Last Run:** {timestamp}'
        elif line.startswith('- **Total Downloads:**'):
            # Extract current count and add new downloads
            try:
                current_count = int(line.split('**')[2].strip())
                new_total = current_count + successful_downloads
                lines[i] = f'- **Total Downloads:** {new_total}'
            except:
                lines[i] = f'- **Total Downloads:** {successful_downloads}'
    
    content = '\n'.join(lines)
    
    # Add new log entry
    log_entry = f"""
### 🔄 Run - {timestamp}
- **Date:** {date_str}
- **Time:** {now.strftime("%I:%M:%S %p")} UTC
- **Downloads:** {successful_downloads}
- **Total Size:** {total_size:,} bytes
- **Files:**
"""
    
    for success, filename, size in downloads:
        if success and filename:
            log_entry += f"  - ✅ {filename} ({size:,} bytes)\n"
        else:
            log_entry += f"  - ❌ Download failed\n"
    
    # Insert at the beginning of recent downloads
    if "## 📝 Recent Downloads" in content:
        content = content.replace("## 📝 Recent Downloads", f"## 📝 Recent Downloads{log_entry}")
    else:
        content += log_entry
    
    LOG_FILE.write_text(content, encoding="utf-8")

def main():
    """Main function - add your PDF URLs here"""
    print("📄 Starting PDF Download Job...")
    print(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    ensure_folder_exists()
    
    # 🎯 ADD YOUR PDF URLs HERE
    pdf_urls = [
        "https://drive.google.com/uc?id=1zLLgjPl71FSBnSxrq7XV0XbfJ_HzcckX&export=download",
        "https://drive.google.com/uc?id=1JVnMYLWGKb10n0-_-952jDB7zHqU-bI4&export=download"
        # Add more URLs as needed
    ]
    
    downloads = []
    
    for url in pdf_urls:
        success, filename, size = download_pdf(url)
        downloads.append((success, filename, size))
    
    # Update log
    update_log(downloads)
    
    print(f"\n🎉 Job completed! Downloaded {sum(1 for s, _, _ in downloads if s)} new files")

if __name__ == "__main__":
    main()