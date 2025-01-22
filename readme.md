# GitHub Activity Fetcher

A Python script to fetch and display GitHub user activity, including pull requests, issues, comments, and discussions. The script queries GitHub's GraphQL API and provides output in multiple formats for easy analysis.

---

## Features
- Fetch activity for a specified GitHub user over the last 90 days.
- Supports pull requests, issues, issue comments, PR comments, and discussion comments.
- Flexible output options:
  - **Summary** (default): Displays counts of each activity type.
  - **Raw**: Displays the raw JSON output.
  - **Details**: Displays counts and titles/URLs for each activity type.
- Includes metadata: Username, date range, and queried organizations.

---

## Supported Organizations
By default, this script only checks activity in the following GitHub organizations:
- `github`
- `githubcustomers`

You can override the default by setting the `GITHUB_ORGS` environment variable with a comma-separated list of organizations:
```bash
export GITHUB_ORGS="myorg,anotherorg"
```

## Requirements
- Python 3.7+
- GitHub personal access token (with access to the repositories you want to query).

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/github-activity-fetcher.git
   cd github-activity-fetcher
   ```

2. Install dependencies
```sh
   pip install -r requirements.txt
```

3. Set required environment variables
```sh
   export GITHUB_TOKEN=$(gh auth token)
   export GITHUB_USERNAME="your_github_username"

   # Optional
   export GITHUB_ORGS="org1,org2"
```


## Usage

**Displays summary counts for each activity type:**
```sh
~ python main.py

{
  "username": "maxiscoding28",
  "since": "2024-10-24T10:39:53.636398",
  "activity": {
    "pull_requests": 10,
    "issues": 6,
    "issue_comments": 10,
    "pr_comments": 10,
    "discussion_comments": 1
  }
}
```

**Displays detailed counts for each activity type**
```sh
~ python main.py --details
{
  "username": "maxiscoding28",
  "since": "2024-10-25T12:34:56.789123",
  "activity": {
    "pull_requests": {
      "count": 10,
      "titles_or_urls": [
        "Fix a bug",
        "Add a feature"
      ]
    },
    "issues": {
      "count": 5,
      "titles_or_urls": [
        "Resolve a problem",
        "Improve performance"
      ]
    }
  }
}
```
**Displays raw JSON output**

```sh
~ python graphql.py --raw

{
  "username": "maxiscoding28",
  "since": "2024-10-25T12:34:56.789123",
  "activity": {
    "pull_requests": [
      {
        "type": "PullRequest",
        "title": "Add new feature",
        "url": "https://github.com/github/repo/pull/99",
        "repository": {
          "owner": "github",
          "name": "repo"
        },
        "updated_at": "2025-01-20T12:00:00Z"
      },
      {
        "type": "PullRequest",
        "title": "Fix bug in API",
        "url": "https://github.com/github/repo/pull/101",
        "repository": {
          "owner": "github",
          "name": "repo"
        },
        "updated_at": "2025-01-21T09:30:00Z"
      }
    ],
    "issues": [
      {
        "type": "Issue",
        "title": "Resolve performance issues",
        "url": "https://github.com/github/repo/issues/123",
        "repository": {
          "owner": "github",
          "name": "repo"
        },
        "created_at": "2025-01-18T15:30:00Z",
        "updated_at": "2025-01-20T16:00:00Z"
      }
    ],
    "issue_comments": [
      {
        "type": "IssueComment",
        "title_or_url": "https://github.com/github/repo/issues/123#comment-456",
        "url": "https://github.com/github/repo/issues/123#comment-456",
        "repository": {
          "owner": "github",
          "name": "repo"
        },
        "updated_at": "2025-01-19T10:15:00Z"
      }
    ],
    "pr_comments": [
      {
        "type": "PRComment",
        "title_or_url": "https://github.com/github/repo/pull/99#comment-789",
        "url": "https://github.com/github/repo/pull/99#comment-789",
        "repository": {
          "owner": "github",
          "name": "repo"
        },
        "updated_at": "2025-01-20T11:00:00Z"
      }
    ],
    "discussion_comments": [
      {
        "type": "DiscussionComment",
        "title_or_url": "https://github.com/github/repo/discussions/456#comment-123",
        "url": "https://github.com/github/repo/discussions/456#comment-123",
        "repository": {
          "owner": "github",
          "name": "repo"
        },
        "updated_at": "2025-01-20T13:00:00Z"
      }
    ]
  }
}
```