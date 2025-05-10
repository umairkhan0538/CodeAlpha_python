import os
import shutil
from pathlib import Path
import time
import logging

def setup_logging():
    """Set up logging to track file organization activities."""
    logging.basicConfig(
        filename='file_organizer.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_downloads_folder():
    """Get the path to the user's Downloads folder."""
    return str(Path.home() / "Downloads")

def create_category_folders(base_path, categories):
    """Create subfolders for each file category if they don't exist."""
    for category in categories:
        folder_path = os.path.join(base_path, category)
        os.makedirs(folder_path, exist_ok=True)

def get_file_category(file_ext, categories):
    """Determine the category for a file based on its extension."""
    for category, extensions in categories.items():
        if file_ext.lower() in extensions:
            return category
    return "Others"

def handle_duplicate(dst_path):
    """Handle duplicate files by appending a timestamp to the filename."""
    if not os.path.exists(dst_path):
        return dst_path
    
    base, ext = os.path.splitext(dst_path)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    new_path = f"{base}_{timestamp}{ext}"
    return new_path

def organize_files():
    """Organize files in the Downloads folder into categorized subfolders."""
    downloads_folder = get_downloads_folder()
    
    # Define file categories and their extensions
    categories = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Audio": [".mp3", ".wav", ".ogg", ".flac"],
        "Others": []  # Catch-all for uncategorized files
    }

    # Create category folders
    create_category_folders(downloads_folder, categories)

    # Set up logging
    setup_logging()
    logging.info("Starting file organization in %s", downloads_folder)

    # Iterate through files in Downloads folder
    for filename in os.listdir(downloads_folder):
        src_path = os.path.join(downloads_folder, filename)
        
        # Skip directories and the log file
        if os.path.isdir(src_path) or filename == 'file_organizer.log':
            continue

        # Get file extension and determine category
        file_ext = os.path.splitext(filename)[1]
        category = get_file_category(file_ext, categories)
        dst_folder = os.path.join(downloads_folder, category)
        dst_path = os.path.join(dst_folder, filename)

        # Handle duplicates
        dst_path = handle_duplicate(dst_path)

        try:
            # Move the file to the appropriate folder
            shutil.move(src_path, dst_path)
            logging.info("Moved '%s' to '%s'", filename, dst_path)
        except (shutil.Error, OSError) as e:
            logging.error("Failed to move '%s': %s", filename, str(e))
            print(f"Error moving {filename}: {e}")

    logging.info("File organization completed.")
    print("File organization completed. Check 'file_organizer.log' for details.")

if __name__ == "__main__":
    organize_files()