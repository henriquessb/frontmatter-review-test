# Frontmatter review test

This repository implements a GitHub Action test to review the frontmatter of Markdown files in pull requests. The Markdown files used for testing are from the VTEX Developer Portal.

The action tests the frontmatter with the following items:

|Item|Type|
|-|-|
|title|Non-empty `string`|
|slug|`string` with only lowercase letters, hyphens, and numbers|
|excerpt|`string`|
|createdAt|`string` with ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ)|
|updatedAt|`string` with ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ)|
|hidden|`boolean`|
|tags|`list`|

## Validation rules

All items are optional. The action verifies:

- If the frontmatter in each Markdown file of the PR follows the YAML format.
- For each item in the YAML, if it is one of the defined types and follows the rules of the type. Undefined types are not verified.
