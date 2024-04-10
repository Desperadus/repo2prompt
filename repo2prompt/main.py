import argparse
import re
import requests
import time
from urllib.parse import urlparse


def compile_ignore_patterns(patterns):
    """Compile a list of regex patterns from the glob-like patterns provided."""
    default_patterns = [r"LICENSE", r".*\.lock$"]
    regex_patterns = [re.compile(pattern) for pattern in default_patterns]

    for pattern in patterns or []:
        regex_pattern = re.compile(re.escape(pattern).replace(r"\*", ".*"))
        regex_patterns.append(regex_pattern)
    return regex_patterns


def should_ignore(file_path, ignore_patterns):
    """Determine if the file path matches any of the ignore patterns."""
    for pattern in ignore_patterns:
        if pattern.match(file_path):
            return True
    return False


def get_repo_files(api_url, token, ignore_patterns=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(api_url, headers=headers)
    files = []

    if response.status_code == 200:
        repo_contents = response.json()
        for item in repo_contents:
            if item["type"] == "file":
                if ignore_patterns and should_ignore(item["path"], ignore_patterns):
                    continue
                file_response = requests.get(item["download_url"], headers=headers)
                if file_response.status_code == 200:
                    files.append(
                        f'File: {item["path"]} with contents:\n{file_response.text}\n\n'
                    )
                time.sleep(0.1)  # Delay to avoid hitting GitHub API rate limit
            elif item["type"] == "dir":
                files.extend(
                    get_repo_files(item["_links"]["self"], token, ignore_patterns)
                )
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Fetch all files from a GitHub repo, with support for ignoring files based on patterns."
    )
    parser.add_argument("repo", help="GitHub repository link")
    parser.add_argument("-t", "--token", help="GitHub API token to avoid rate limits")
    parser.add_argument(
        "-i",
        "--ignore",
        action="append",
        help="Regex pattern for files to ignore (e.g., '*.md' or '*.txt'). Can be used multiple times.",
    )
    args = parser.parse_args()

    parsed_url = urlparse(args.repo)
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) != 2:
        print("Error: Invalid GitHub repository URL.")
        return

    api_url = f"https://api.github.com/repos/{path_parts[0]}/{path_parts[1]}/contents"
    ignore_patterns = compile_ignore_patterns(args.ignore)

    files_string = get_repo_files(api_url, args.token, ignore_patterns)
    print("".join(files_string))


if __name__ == "__main__":
    main()
