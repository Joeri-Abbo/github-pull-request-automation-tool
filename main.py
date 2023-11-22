import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv('GITHUB_TOKEN')
if github_token is None:
    raise ValueError("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")

g = Github(github_token)

repo_owner = input("Enter the name of the user or organization whose repositories you want to check:")
all_repos = []

try:
    if g.get_user().login == repo_owner:
        repos = g.get_user().get_repos()
    else:
        repos = g.get_organization(repo_owner).get_repos()

    all_repos.extend(repos)

    while repos._couldGrow():
        repos = repos._grow()
        all_repos.extend(repos)

    for repo in all_repos:
        if repo.private:
            print(f"Private repository: {repo.full_name}")
        else:
            print(f"Public repository: {repo.full_name}")

        pull_requests = repo.get_pulls(state='open')
        if pull_requests.totalCount == 0:
            print("No open pull requests found.")
            continue
        for pull_request in pull_requests:
            check_runs = g.get_repo(repo.full_name).get_commit(pull_request.head.sha).get_check_runs()
            checks_passed = all(
                check_run.status == 'completed' and check_run.conclusion == 'success' for check_run in check_runs)

            if checks_passed:
                try:
                    pull_request.merge()
                    print(
                        f"Pull request #{pull_request.number} in repository {repo.full_name} has been successfully merged.")
                except Exception as e:
                    print(
                        f"Failed to merge pull request #{pull_request.number} in repository {repo.full_name}: {str(e)}")
            else:
                print(
                    f"Not all status checks have passed for pull request #{pull_request.number} in repository {repo.full_name}. It will not be merged.")
except Exception as e:
    print(f"Error fetching repositories: {e}")
