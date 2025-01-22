# GQL CLASSES
class PullRequest:
    def __init__(self, orgs, username, since):
        self.orgs_to_query = " ".join([f"org:{org}" for org in orgs])
        self.username = username
        self.since = since

    def get_query(self):
        """Returns the GraphQL query for fetching pull requests."""
        return f"""
            query {{
                search(query: "{self.orgs_to_query} commenter:{self.username} updated:>{self.since}", type: ISSUE, first: 10) {{
                    edges {{
                        node {{
                            __typename
                            ... on Issue {{
                                title
                                url
                                repository {{ name owner {{ login }} }}
                                updatedAt
                            }}
                            ... on PullRequest {{
                                title
                                url
                                repository {{ name owner {{ login }} }}
                                updatedAt
                            }}
                        }}
                    }}
                }}
            }}
        """

    @staticmethod
    def format_response(data):
        """Formats the raw response into a list of pull request dictionaries."""
        pull_requests = []
        for edge in data["data"]["search"]["edges"]:
            node = edge["node"]
            pull_requests.append({
                "type": node["__typename"],
                "title_or_url": node.get("title") or node.get("url"),
                "url": node.get("url"),
                "repository": {
                    "owner": node["repository"]["owner"]["login"],
                    "name": node["repository"]["name"]
                },
                "updated_at": node.get("updatedAt")
            })
        return pull_requests

class Issue:
    def __init__(self, orgs, username, since):
        self.orgs_to_query = " ".join([f"org:{org}" for org in orgs])
        self.username = username
        self.since = since

    def get_query(self):
        """Returns the GraphQL query for fetching issues."""
        return f"""
            query {{
                search(query: "{self.orgs_to_query} author:{self.username} created:>{self.since} is:issue", type: ISSUE, first: 10) {{
                    edges {{
                        node {{
                            __typename
                            ... on Issue {{
                                title
                                url
                                repository {{ name owner {{ login }} }}
                                createdAt
                                updatedAt
                            }}
                        }}
                    }}
                }}
            }}
        """

    @staticmethod
    def format_response(data):
        """Formats the raw response into a list of issue dictionaries."""
        issues = []
        for edge in data["data"]["search"]["edges"]:
            node = edge["node"]
            issues.append({
                "type": node["__typename"],
                "title_or_url": node.get("title") or node.get("url"),
                "url": node.get("url"),
                "repository": node.get("repository"),
                "created_at": node.get("createdAt"),
                "updated_at": node.get("updatedAt"),
            })
        return issues

class IssueComment:
    def __init__(self, orgs, username, since):
        self.orgs_to_query = " ".join([f"org:{org}" for org in orgs])
        self.username = username
        self.since = since

    def get_query(self):
        """Returns the GraphQL query for fetching issue comments."""
        return f"""
            query {{
                search(query: "{self.orgs_to_query} commenter:{self.username} updated:>{self.since} is:issue", type: ISSUE, first: 10) {{
                    edges {{
                        node {{
                            __typename
                            ... on Issue {{
                                title
                                url
                                repository {{
                                    name
                                    owner {{
                                        login
                                    }}
                                }}
                                updatedAt
                            }}
                        }}
                    }}
                }}
            }}
        """

    @staticmethod
    def format_response(data):
        """Formats the raw response into a list of issue comment dictionaries."""
        comments = []
        for edge in data["data"]["search"]["edges"]:
            node = edge["node"]
            comments.append({
                "type": "IssueComment",
                "title_or_url": node.get("title") or node.get("url"),
                "url": node.get("url"),
                "repository": {
                    "owner": node["repository"]["owner"]["login"],
                    "name": node["repository"]["name"]
                } if "repository" in node else None,
                "updated_at": node.get("updatedAt"),
            })
        return comments

class PRComment:
    def __init__(self, orgs, username, since):
        self.orgs_to_query = " ".join([f"org:{org}" for org in orgs])
        self.username = username
        self.since = since

    def get_query(self):
        """Returns the GraphQL query for fetching pull request comments."""
        return f"""
            query {{
                search(query: "{self.orgs_to_query} commenter:{self.username} updated:>{self.since} is:pr", type: ISSUE, first: 10) {{
                    edges {{
                        node {{
                            __typename
                            ... on PullRequest {{
                                title
                                url
                                repository {{
                                    name
                                    owner {{
                                        login
                                    }}
                                }}
                                updatedAt
                            }}
                        }}
                    }}
                }}
            }}
        """

    @staticmethod
    def format_response(data):
        """Formats the raw response into a list of pull request comment dictionaries."""
        comments = []
        for edge in data["data"]["search"]["edges"]:
            node = edge["node"]
            comments.append({
                "type": "PRComment",
                "title_or_url": node.get("title") or node.get("url"),
                "url": node.get("url"),
                "repository": {
                    "owner": node["repository"]["owner"]["login"],
                    "name": node["repository"]["name"]
                } if "repository" in node else None,
                "updated_at": node.get("updatedAt"),
            })
        return comments

class DiscussionComment:
    def __init__(self, orgs, username, since):
        self.orgs_to_query = " ".join([f"org:{org}" for org in orgs])
        self.username = username
        self.since = since

    def get_query(self):
        """Returns the GraphQL query for fetching discussion comments."""
        return f"""
            query {{
                search(query: "{self.orgs_to_query} commenter:{self.username} updated:>{self.since} is:discussion", type: DISCUSSION, first: 10) {{
                    edges {{
                        node {{
                            __typename
                            ... on Discussion {{
                                title
                                url
                                repository {{
                                    name
                                    owner {{
                                        login
                                    }}
                                }}
                                updatedAt
                            }}
                        }}
                    }}
                }}
            }}
        """

    @staticmethod
    def format_response(data):
        """Formats the raw response into a list of discussion comment dictionaries."""
        comments = []
        for edge in data["data"]["search"]["edges"]:
            node = edge["node"]
            comments.append({
                "type": "DiscussionComment",
                "title_or_url": node.get("title") or node.get("url"),
                "url": node.get("url"),
                "repository": {
                    "owner": node["repository"]["owner"]["login"],
                    "name": node["repository"]["name"]
                } if "repository" in node else None,
                "updated_at": node.get("updatedAt"),
            })
        return comments
