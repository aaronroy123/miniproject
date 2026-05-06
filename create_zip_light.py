import os
import zipfile

def get_files_to_zip(source_dir):
    files_to_zip = []
    
    # Highly restrictive ignore list for directories
    ignore_dirs = {
        'venv', '.git', '.gradle', 'build', '.idea', '__pycache__', 
        'data', 'models' # Ignoring 'data' because it might have many files
    }
    
    # Only include these file extensions (core logic files)
    include_exts = {'.py', '.html', '.js', '.css', '.md', '.txt', '.json', '.yml', '.yaml'}
    
    for root, dirs, files in os.walk(source_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [
            d for d in dirs 
            if d not in ignore_dirs 
            and not d.endswith('__pycache__') 
            and d != 'build'
            and not (d == 'static' and 'app' in root) # optional if static is too big
        ]
        
        for file in files:
            if file in ['package-lock.json', 'subscriptions.json']:
                continue # Skip large/unnecessary JSONs
                
            if any(file.endswith(ext) for ext in include_exts):
                file_path = os.path.join(root, file)
                files_to_zip.append(file_path)
            
    return files_to_zip

def create_zip(source_dir, output_filename):
    print(f"Gathering files from {source_dir}...")
    files = get_files_to_zip(source_dir)
    print(f"Total files to zip: {len(files)}")
    
    print(f"Creating zip file: {output_filename}")
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            arcname = os.path.relpath(file, source_dir)
            zipf.write(file, arcname)
            
    size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"Successfully created {output_filename} (Size: {size_mb:.2f} MB)")

if __name__ == '__main__':
    project_dir = r"d:\waterborne-disease-ai"
    output_zip = r"d:\waterborne-disease-ai\project_source_code_light.zip"
    create_zip(project_dir, output_zip)
