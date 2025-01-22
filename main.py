import os
import requests
import json
import argparse
from datetime import datetime, timedelta
from gql_classes import *

# VARIABLES
GITHUB_GRAPHQL_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_ORGS = os.getenv("GITHUB_ORGS", "github,githubcustomers").split(",")

if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN is not set in the environment variables.")
GITHUB_GRAPHQL_API_URL = "https://api.github.com/graphql"
if not GITHUB_USERNAME:
    raise EnvironmentError("GITHUB_USERNAME is not set in the environment variables.")

# REQUEST LOGIC
def execute_query(query):
    headers = {"Authorization": f"bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_GRAPHQL_API_URL, json={"query": query}, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_user_activity(username):
    since = (datetime.now() - timedelta(days=90)).isoformat()

    queries = {
        "pull_requests": PullRequest(GITHUB_ORGS, username, since),
        "issues": Issue(GITHUB_ORGS, username, since),
        "issue_comments": IssueComment(GITHUB_ORGS, username, since),
        "pr_comments": PRComment(GITHUB_ORGS, username, since),
        "discussion_comments": DiscussionComment(GITHUB_ORGS, username, since),
    }

    results = {}
    for key, query in queries.items():
        query_result = execute_query(query.get_query())
        results[key] = query.format_response(query_result)

    return results

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch GitHub user activity.")
    parser.add_argument("--raw", action="store_true", help="Log raw output without formatting.")
    parser.add_argument("--details", action="store_true", help="Log the count and titles_or_urls for each query.")
    args = parser.parse_args()

    # Define username and date range
    username = GITHUB_USERNAME
    since = (datetime.now() - timedelta(days=90)).isoformat()

    # Fetch user activity
    activity = fetch_user_activity(username)

    # Common metadata for all outputs
    metadata = {
        "username": GITHUB_USERNAME,
        "since": since,
        "organizations": GITHUB_ORGS
    }

    # Handle output based on flags
    if args.raw:
        # Raw JSON output with metadata
        output = {**metadata, "activity": activity}
        print(json.dumps(output, indent=2))
    elif args.details:
        # Count and titles_or_urls for each query with metadata
        detailed_output = {
            query_type: {
                "count": len(results),
                "titles_or_urls": [item["title_or_url"] for item in results]
            }
            for query_type, results in activity.items()
        }
        output = {**metadata, "activity": detailed_output}
        print(json.dumps(output, indent=2))
    else:
        # Default: Only the count for each query with metadata
        summary_output = {
            query_type: len(results)
            for query_type, results in activity.items()
        }
        output = {**metadata, "activity": summary_output}
        print(json.dumps(output, indent=2))