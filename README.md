
# GitHub Repo Comparison Tool

This project provides a web-based tool to compare two GitHub repositories, identify duplicate code, highlight differences, and allow the user to approve changes to prefix AI-generated code with "AI-" before committing to the repository.

## Features

- Clone two GitHub repositories (one human-coded and one AI-generated).
- Compare the files side by side.
- Highlight duplicate lines and differences.
- Approve changes to prefix AI-generated code with "AI-".
- Commit and push approved changes to the GitHub repository.

## Requirements

- Python 3.x
- `git` installed and available in the PATH.

## Python Libraries

Install the required Python libraries using pip:

```sh
pip install Flask Flask-Cors GitPython
```

## Folder Structure

```
project/
│
├── app.py
└── templates/
    └── index.html
```

## How to Run

1. **Clone the repository** to your local machine.

    ```sh
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. **Install the required Python libraries**:

    ```sh
    pip install Flask Flask-Cors GitPython
    ```

3. **Run the Flask application**:

    ```sh
    python app.py
    ```

4. **Open your web browser** and navigate to `http://127.0.0.1:5000`.

## Usage

1. **Enter the URLs** of the human-coded and AI-generated GitHub repositories in the form fields.
2. **Click the Compare button** to start the comparison process.
3. **View the comparison results** displayed side by side with highlighted differences.
4. **Approve changes** by clicking the Approve button to prefix AI-generated code with "AI-" and commit the changes to the repository.

## Files

- `app.py`: The Flask backend that handles cloning repositories, comparing files, and approving changes.
- `templates/index.html`: The frontend HTML file that provides the user interface.

## Notes

- Ensure that you have the necessary permissions to clone, commit, and push to the specified GitHub repositories.
- The comparison process works with `.html` and `.css` files. Modify the `file_extensions` list in `app.py` to include other file types if needed.

## Troubleshooting

- If you encounter a `PermissionError` while cloning repositories, ensure that no other process is using the repository directory and that you have the necessary permissions.
- Check the console for error messages and adjust the code or dependencies as needed.

---

This `README.md` file provides a comprehensive guide for new users to understand, set up, and run the project. It includes installation instructions, usage guidelines, and troubleshooting tips.
