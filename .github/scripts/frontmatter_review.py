import os
import sys
from github import Github

# Get environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
GITHUB_EVENT_PATH = os.getenv('GITHUB_EVENT_PATH')

if not (GITHUB_TOKEN and GITHUB_REPOSITORY and GITHUB_EVENT_PATH):
    print('Missing required environment variables.')
    sys.exit(1)

# Load event data
event = {}
with open(GITHUB_EVENT_PATH, 'r') as f:
    import json
    event = json.load(f)

pr_number = event.get('pull_request', {}).get('number')
if not pr_number:
    print('Not a pull request event.')
    sys.exit(0)

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)
pr = repo.get_pull(pr_number)

# Get changed files in the PR
changed_files = [f for f in pr.get_files() if f.filename.endswith(('.md', '.mdx'))]

print(f"Found {len(changed_files)} markdown files in PR:")
for f in changed_files:
    print(f"- {f.filename}")
    content = repo.get_contents(f.filename, ref=pr.head.ref)
    print(content.decoded_content.decode('utf-8')[:500])  # Print first 500 chars
