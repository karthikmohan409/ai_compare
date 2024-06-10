import os
import difflib
import shutil
from git import Repo, GitCommandError
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def handle_remove_readonly(func, path, excinfo):
    os.chmod(path, 0o777)
    func(path)

# Clone the repositories
def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir, onexc=handle_remove_readonly)
    return Repo.clone_from(repo_url, clone_dir)

# Get all file paths from a repository
def get_repo_files(repo_dir, file_extensions):
    files = []
    for root, _, filenames in os.walk(repo_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in file_extensions):
                files.append(os.path.join(root, filename))
    return files

# Compare two files and highlight differences
def compare_files(file1_path, file2_path):
    with (open(file1_path, 'r') as file1, open(file2_path, 'r') as file2):
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()
    
    differ = difflib.Differ()
    diff = list(differ.compare(file1_lines, file2_lines))
    return diff

# Highlight differences
def highlight_diffs(diffs):
    result = {'remove': [], 'add': []}
    for line in diffs:
        if line.startswith('- '):
            result['remove'].append(line[2:].rstrip())
        elif line.startswith('+ '):
            result['add'].append(line[2:].rstrip())
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    human_repo_url = data['human_repo_url']
    ai_repo_url = data['ai_repo_url']
    
    human_repo_dir = './human_repo'
    ai_repo_dir = './ai_repo'
    
    try:
        human_repo = clone_repo(human_repo_url, human_repo_dir)
        ai_repo = clone_repo(ai_repo_url, ai_repo_dir)
    except GitCommandError as e:
        return jsonify({'error': str(e)})
    
    file_extensions = ['.html', '.css']
    human_files = get_repo_files(human_repo_dir, file_extensions)
    ai_files = get_repo_files(ai_repo_dir, file_extensions)
    
    comparisons = {}
    for human_file in human_files:
        relative_path = os.path.relpath(human_file, human_repo_dir)
        ai_file = os.path.join(ai_repo_dir, relative_path)
        
        if os.path.exists(ai_file):
            diffs = compare_files(human_file, ai_file)
            comparisons[relative_path] = {
                'diffs': highlight_diffs(diffs),
                'human_content': open(human_file).read(),
                'ai_content': open(ai_file).read()
            }
    
    return jsonify(comparisons)

@app.route('/approve', methods=['POST'])
def approve():
    data = request.get_json()
    file_to_update = data['file']
    
    ai_repo_dir = './ai_repo'
    ai_file_path = os.path.join(ai_repo_dir, file_to_update)
    
    with open(ai_file_path, 'r') as file:
        lines = file.readlines()
    
    updated_lines = ["AI-" + line if line.startswith(' ') else line for line in lines]
    
    with open(ai_file_path, 'w') as file:
        file.writelines(updated_lines)
    
    repo = Repo(ai_repo_dir)
    repo.git.add(ai_file_path)
    repo.index.commit(f"Prefixed duplicate code with 'AI-' in {file_to_update}")
    origin = repo.remote(name='origin')
    origin.push()
    
    return jsonify({'status': 'success', 'message': f'{file_to_update} updated and pushed to GitHub'})

if __name__ == "__main__":
    app.run(debug=True)
