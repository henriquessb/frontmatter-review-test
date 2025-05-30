import os
import sys
from github import Github
import yaml

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

# Get changed Markdown files in the PR (only in 'Test docs' folder)
changed_files = [f for f in pr.get_files() if (f.filename.endswith(('.md', '.mdx')) and f.filename.startswith('Test docs/'))]

print(f"Found {len(changed_files)} markdown files in PR:")
error_found = False
frontmatters = {}
for f in changed_files:
    print(f"- {f.filename}")
    content = repo.get_contents(f.filename, ref=pr.head.ref)
    text = content.decoded_content.decode('utf-8')
    # Extract frontmatter
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            frontmatter = text[3:end+1].strip()
            try:
                fm_dict = yaml.safe_load(frontmatter)
                if not isinstance(fm_dict, dict):
                    print(f"ERROR: Frontmatter in {f.filename} is not a valid YAML dictionary.")
                    error_found = True
                    fm_dict = {}
            except Exception as e:
                print(f"ERROR: Failed to parse YAML frontmatter in {f.filename}: {e}")
                error_found = True
                fm_dict = {}
            frontmatters[f.filename] = fm_dict
            print(f'Frontmatter dict for "{f.filename}":\n{{')
            for k, v in fm_dict.items():
                print(f'  {k}: {v}')
            print('}')
            # Validate required fields if present
            import re
            iso8601_regex = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
            for key, value in fm_dict.items():
                if key == 'title':
                    if not isinstance(value, str):
                        print(f"ERROR: '{key}' in {f.filename} must be a non-empty string.")
                        error_found = True
                if key == 'excerpt':
                    if not isinstance(value, str):
                        print(f"ERROR: '{key}' in {f.filename} must be a string.")
                        error_found = True
                if key == 'slug':
                    if not (isinstance(value, str) and re.fullmatch(r'[a-z0-9\-]+', value)):
                        print(f"ERROR: 'slug' in {f.filename} must contain only lowercase letters, numbers, and hyphens.")
                        error_found = True
                if key == 'hidden':
                    if not isinstance(value, bool):
                        print(f"ERROR: 'hidden' in {f.filename} must be a boolean (true or false).")
                        error_found = True
                if key == 'createdAt':
                    if not (isinstance(value, str) and iso8601_regex.match(value)):
                        print(f"ERROR: '{key}' in {f.filename} must be a string in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ).")
                        error_found = True
                if key == 'updatedAt':
                    if not (isinstance(value, str) and iso8601_regex.match(value)):
                        print(f"ERROR: '{key}' in {f.filename} must be a string in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ).")
                        error_found = True
        else:
            print(f"ERROR: {f.filename} frontmatter not closed with '---'.")
            error_found = True
    else:
        print(f"ERROR: {f.filename} does not start with frontmatter block ('---').")
        error_found = True

if error_found:
    print("\nFrontmatter errors found. Failing the action.")
    sys.exit(1)
