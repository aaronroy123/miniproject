ive import os

def concat_code(source_dir, output_file):
    ignore_dirs = {
        'venv', '.git', '.gradle', 'build', '.idea', '__pycache__', 
        'data', 'models', 'app/build'
    }
    include_exts = {'.py', '.html', '.css', '.js', '.md'}
    
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [
                d for d in dirs 
                if d not in ignore_dirs 
                and not d.endswith('__pycache__') 
                and d != 'build'
                and not (d == 'static' and 'app' in root)
            ]
            
            for file in files:
                if any(file.endswith(ext) for ext in include_exts):
                    if file in ['package-lock.json', 'subscriptions.json']:
                        continue
                        
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, source_dir)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as in_f:
                            content = in_f.read()
                        
                        out_f.write(f"\n\n{'='*80}\n")
                        out_f.write(f"FILE: {rel_path}\n")
                        out_f.write(f"{'='*80}\n\n")
                        out_f.write(content)
                    except Exception as e:
                        print(f"Skipping {rel_path} due to error: {e}")
                        
if __name__ == '__main__':
    project_dir = r"d:\waterborne-disease-ai"
    output_txt = r"d:\waterborne-disease-ai\project_source_code.txt"
    concat_code(project_dir, output_txt)
    size_mb = os.path.getsize(output_txt) / (1024 * 1024)
    print(f"Created {output_txt} (Size: {size_mb:.2f} MB)")
