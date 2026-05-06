import os
import zipfile

def get_files_to_zip(source_dir):
    files_to_zip = []
    
    # Directories to completely ignore to save space
    ignore_dirs = {
        'venv', '.git', '.gradle', 'build', '.idea', '__pycache__', 
        'app/build'
    }
    
    # File extensions to ignore
    ignore_exts = {'.apk', '.aab', '.log', '.idsig', '.keystore'}
    
    for root, dirs, files in os.walk(source_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.endswith('__pycache__') and not d == 'build']
        
        for file in files:
            # Skip specific files and extensions
            if any(file.endswith(ext) for ext in ignore_exts):
                continue
                
            file_path = os.path.join(root, file)
            files_to_zip.append(file_path)
            
    return files_to_zip

def create_zip(source_dir, output_filename):
    print(f"Gathering files from {source_dir}...")
    files = get_files_to_zip(source_dir)
    
    print(f"Creating zip file: {output_filename}")
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            # Create a relative arcname so it unzips nicely
            arcname = os.path.relpath(file, source_dir)
            zipf.write(file, arcname)
            
    size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"Successfully created {output_filename} (Size: {size_mb:.2f} MB)")

if __name__ == '__main__':
    project_dir = r"d:\waterborne-disease-ai"
    output_zip = r"d:\waterborne-disease-ai\project_source_code.zip"
    create_zip(project_dir, output_zip)
