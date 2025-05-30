# Frontmatter review test

This repository implements a GitHub Action test to review the frontmatter of Markdown files in pull requests. The Markdown files used for testing are from the VTEX Developer Portal.

The action tests the frontmatter with the following items:

|Item|Type|
|-|-|
|title|`string`|
|slug|`string` with only lowercase letters, hyphens and numbers|
|excerpt|`string`|
|createdAt|`string` with ISO 8060 format (YYYY-MM-DDThh:mm:ss.sssZ)|
|updatedAt|`string` with ISO 8060 format (YYYY-MM-DDThh:mm:ss.sssZ)|
|hidden|`boolean`|
|tags|`list`|
