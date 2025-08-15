import requests
import os
from pathlib import Path
from datetime import datetime
import hashlib

# Configuration
DOWNLOAD_FOLDER = Path("downloaded_pdfs")
LOG_FILE = Path("download_log.md")

def ensure_folder_exists():
    """Create download folder if it doesn't exist"""
    DOWNLOAD_FOLDER.mkdir(exist_ok=True)

def download_pdf(url, filename=None):
    """Download a PDF from URL"""
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
        
        # Generate filename if not provided
        if not filename:
            filename = url.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename += '.pdf'
        
        filepath = DOWNLOAD_FOLDER / filename
        
        # Check if file already exists and is the same
        if filepath.exists():
            existing_hash = hashlib.md5(filepath.read_bytes()).hexdigest()
            new_hash = hashlib.md5(response.content).hexdigest()
            if existing_hash == new_hash:
                print(f"✅ File already exists and is identical: {filename}")
                return False, filename, len(response.content)
        
        # Save the PDF
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
    
    # Count new downloads
    new_downloads = sum(1 for success, _, _ in downloads if success)
    total_size = sum(size for success, _, size in downloads if success)
    
    # Add new log entry
    log_entry = f"""
### 🔄 Run - {timestamp}
- **Date:** {date_str}
- **Time:** {now.strftime("%I:%M:%S %p")} UTC
- **New Downloads:** {new_downloads}
- **Total Size:** {total_size:,} bytes
- **Files:**
"""
    
    for success, filename, size in downloads:
        if success and filename:
            log_entry += f"  - ✅ {filename} ({size:,} bytes)\n"
        elif filename:
            log_entry += f"  - ⚪ {filename} (already exists)\n"
    
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