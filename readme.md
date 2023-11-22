# GitHub Pull Request Automation Tool

## Overview

This script automates the process of checking and merging open pull requests in GitHub repositories. It's designed for
users or organizations looking to streamline their code integration workflow on GitHub.

## Features

- **Automatic Repository Fetching**: Retrieves all repositories for a specified user or organization.
- **Pull Request Management**: Lists and evaluates open pull requests in each repository.
- **Automated Merging**: Merges pull requests that have passed all status checks.

## Prerequisites

- **Python Environment**: Ensure Python is installed on your system.
- **Required Libraries**: The script uses `github` and `dotenv`. Install them via pip:
  ```
  pip install -r requirements.txt
  ```

## Setup

1. **GitHub Token**: You need a personal access token from GitHub with appropriate permissions to access repositories
   and manage pull requests.

2. **Environment Variable**:
    - Create a `.env` file in your project directory.
    - Add your GitHub token to this file:
      ```
      GITHUB_TOKEN=your_github_token_here
      ```

## Usage

1. **Run the Script**: Execute the script in your Python environment.
2. **Enter Repository Owner**: Input the username or organization name whose repositories you want to manage when
   prompted.
3. **Automated Processing**: The script will automatically fetch repositories, list open pull requests, and attempt to
   merge those that meet the criteria (all checks passed).

## Note

- This tool will only merge pull requests that have all status checks completed successfully.
- It differentiates between private and public repositories, listing them accordingly.
- The script provides detailed output for each step, including success or failure messages for pull request mergers.

## Disclaimer

- Use this tool responsibly and ensure you have the correct permissions to manage repositories and pull requests.
- Always review the impact of automated merging in your workflow, especially in production environments.