import argparse
import re
import requests
import time
from urllib.parse import urlparse
import os


def compile_patterns(patterns, default_patterns=None):
    """Compile a list of regex patterns from the glob-like patterns provided."""
    regex_patterns = [re.compile(pattern) for pattern in default_patterns or []]

    for pattern in patterns or []:
        regex_pattern = re.compile(re.escape(pattern).replace(r"\*", ".*"))
        regex_patterns.append(regex_pattern)
    return regex_patterns


def should_ignore(file_path, ignore_patterns, look_patterns=None):
    """Determine if the file path matches any of the ignore patterns or doesn't match look patterns."""
    # If look patterns are specified and the file doesn't match any, ignore it
    if look_patterns and not any(p.match(file_path) for p in look_patterns):
        return True
    # If the file matches any ignore patterns, also ignore it
    if any(p.match(file_path) for p in ignore_patterns):
        return True
    return False


def get_repo_files(api_url, token, ignore_patterns=None, look_patterns=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(api_url, headers=headers)
    files = []

    if response.status_code == 200:
        repo_contents = response.json()
        for item in repo_contents:
            if item["type"] == "file" and not should_ignore(
                item["path"], ignore_patterns, look_patterns
            ):
                file_response = requests.get(item["download_url"], headers=headers)
                if file_response.status_code == 200:
                    files.append(f'"{item["path"]}": "{file_response.text}"\n\n')
                time.sleep(0.1)  # Delay to avoid hitting GitHub API rate limit
            elif item["type"] == "dir":
                files.extend(
                    get_repo_files(
                        item["_links"]["self"], token, ignore_patterns, look_patterns
                    )
                )
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Fetch all files from a GitHub repo, with support for ignoring or specifically looking for files based on patterns."
    )
    parser.add_argument("repo", help="GitHub repository link")
    parser.add_argument("-t", "--token", help="GitHub API token to avoid rate limits")
    parser.add_argument(
        "-i",
        "--ignore",
        action="append",
        help="Regex pattern for files to ignore. Can be used multiple times.",
    )
    parser.add_argument(
        "-l",
        "--look",
        action="append",
        help="Regex pattern for files to specifically look for. Ignores others not matching the pattern. Can be used multiple times.",
    )
    args = parser.parse_args()

    parsed_url = urlparse(args.repo)
    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) != 2:
        print("Error: Invalid GitHub repository URL.")
        return

    if args.token is None:
        args.token = os.getenv("GITHUB_USER_TOKEN")

    api_url = f"https://api.github.com/repos/{path_parts[0]}/{path_parts[1]}/contents"
    ignore_patterns = compile_patterns(
        args.ignore, default_patterns=[r"LICENSE", r".*\.lock$"]
    )
    look_patterns = compile_patterns(args.look)

    files_string = get_repo_files(api_url, args.token, ignore_patterns, look_patterns)
    print("".join(files_string))


if __name__ == "__main__":
    main()
