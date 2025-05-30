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
error_found = False
for f in changed_files:
    print(f"- {f.filename}")
    content = repo.get_contents(f.filename, ref=pr.head.ref)
    text = content.decoded_content.decode('utf-8')
    # Extract frontmatter
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            frontmatter = text[3:end+1].strip()
            print(f"Frontmatter for \"{f.filename}\":")
            print(frontmatter)
        else:
            print(f"ERROR: {f.filename} frontmatter not closed with '---'.")
            error_found = True
    else:
        print(f"ERROR: {f.filename} does not start with frontmatter block ('---').")
        error_found = True

if error_found:
    print("\nFrontmatter errors found. Failing the action.")
    sys.exit(1)
