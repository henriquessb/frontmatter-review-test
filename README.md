# Frontmatter review test

This repository implements a GitHub Action test to review the frontmatter of Markdown files in pull requests. The Markdown files used for testing are from the VTEX Developer Portal.

## Validation rules

### Field types

The action validates the frontmatter with the following fields:

|Field|Type|
|-|-|
|`title`|Non-empty `string`|
|`slug`|`string` with only lowercase letters, hyphens, and numbers. Must be equal the filename without extension.|
|`excerpt`|`string`|
|`createdAt`|`string` with ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ)|
|`updatedAt`|`string` with ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ)|
|`hidden`|`boolean`|
|`tags`|`list`|
|`type`|`string` with release note type. Must be one of: added, deprecated, fixed, improved, info, removed.|

### Documentation types

The action validates the frontmatter fields for each documentation type as below:

|Field|Release note|Guide|Troubleshooting|FastStore|
|-|:-:|:-:|:-:|:-:|
|`title`|⭕|⭕|⭕|⭕|
|`slug`|⭕|⭕|⭕|❌|
|`excerpt`|⭕|⭕|⭕|❌|
|`createdAt`|⭕|⭕|⭕|❌|
|`updatedAt`|⭕|⭕|⭕|❌|
|`hidden`|⭕|⭕|⭕|❌|
|`tags`|✅|✅|⭕|❌|
|`type`|⭕|❌|❌|❌|

Legend:

- ⭕: Mandatory
- ✅: Allowed
- ❌: Prohibited
