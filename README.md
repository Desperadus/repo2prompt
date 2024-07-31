# repo2prompt

`repo2prompt` is a command-line tool designed to fetch all files from a specified GitHub repository, allowing for selective file ignoring based on patterns. This tool is for users looking to quickly gather repository contents without manually cloning, downloading or copying each file.

## Installation

`repo2prompt` can be installed directly from this GitHub repository using `pip`. To install the latest version, run the following command:

```bash
pip install git+https://github.com/Desperadus/repo2prompt
```

Ensure you have `git` installed on your system and that it is accessible from your command line or terminal. Python 3.8+ is required to run the tool.

## Usage

After installation, `repo2prompt` can be run from the command line or terminal. The basic syntax for the tool is as follows:

```bash
repo2prompt <GitHub Repository URL> [options]
```

### Options

- `-t`, `--token`: Specify a GitHub API token to avoid rate limits. Highly recommended for repositories with many files or frequent accesses.
- `-i`, `--ignore`: Specify regex patterns for files to ignore (e.g., `*.md` or `*.txt`). Can be used multiple times to specify multiple patterns. LICENSE and .lock files are ignored by default.
- `l`, `--look`: Look only for these patterns. Can be used multiple times to specify multiple patterns. (e.g., `*.py` or `*.json`)

### Example

To fetch all files from this repository, for example, ignoring Markdown files, you might use:

```bash
repo2prompt https://github.com/Desperadus/repo2prompt -i "*.md"
```

## Contributing

Contributions to `repo2prompt` are welcome! Whether it's reporting a bug, discussing improvements, or contributing code.

Please feel free to report issues or open pull requests on my [GitHub repository](https://github.com/Desperadus/repo2prompt).

Or contact me at my email `tomgolf.jelinek@gmail.com`.

## License

`repo2prompt` is released under the GPL-3.0 License. See the LICENSE file in the GitHub repository for more details.
