from collections import Counter

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class LanguagesMostUsed(BaseGitHubMetric):
    """
    A GitHub metric that infers the most used programming languages
    by analyzing the files modified in the user's commits.

    Unlike repository-wide language statistics, this method determines
    which languages the user has actually worked with by examining file extensions
    in commits.

    Attributes:
        MAX_COMMITS_PER_REPO (int): The maximum number of commits analyzed per repository (default: 10).
        MAX_FILES_PER_COMMIT (int): The maximum number of files analyzed per commit (default: 5).
        order (int): Defines the execution order of the metric (default: 1).
        logger (Logger): Logger instance for logging metric execution details.

    Methods:
        execute(username): Retrieves and processes the user's programming language usage.
        get_repositories(username): Fetches a list of repositories owned by the user.
        get_commit_languages(username, repo): Retrieves the languages used in a specific repository.
        get_commit_files(username, repo, sha): Fetches the list of files modified in a commit.
        infer_language(filename): Infers the programming language based on the file extension.
    """

    MAX_COMMITS_PER_REPO = 10
    MAX_FILES_PER_COMMIT = 5

    def __init__(
        self,
    ):
        """
        Initializes the metric with a predefined execution order and logger.
        """
        super().__init__()
        self.order = OderService.language_most_used.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()

    def execute(self, username):
        """
        Retrieves and processes the most used programming languages based on the user's commits.

        Args:
            username (str): The GitHub username to analyze.

        Returns:
            dict: A structured response containing the most used languages and their usage count.

        If no contributions are found, the response will contain an empty list.
        """
        self.logger.info(f"📊 Starting language analysis for {username}")

        repos = self.get_repositories(username)
        if not repos:
            self.logger.warning(f"⚠️ No repositories found for {username}")
            return self.format_response("most_used_languages", [])

        language_counter = Counter()

        for repo in repos:
            self.logger.info(
                f"🔍 Analyzing up to {self.MAX_COMMITS_PER_REPO} commits in repository: {repo}"
            )
            commits = self.get_commit_languages(username, repo)
            language_counter.update(commits)

            if sum(language_counter.values()) > 100:
                self.logger.info("✅ Sufficient data collected, stopping analysis.")
                break

        most_used = [
            {"language": lang, "count": count}
            for lang, count in language_counter.most_common(3)
        ]

        self.logger.info(f"✅ Inferred languages for {username}: {most_used}")
        return self.format_response("most_used_languages", most_used)

    def get_repositories(self, username):
        """
        Fetches a list of repositories owned by the user.

        Args:
            username (str): The GitHub username.

        Returns:
            list: A list of repository names.

        Limits the number of repositories fetched to 50 for performance optimization.
        """
        path = f"/users/{username}/repos?per_page=50"
        repos = self.github_client_service.request_with_rate_limit(path)

        if not repos:
            self.logger.warning(f"⚠️ No repositories found for {username}")
            return []

        repo_names = [repo["name"] for repo in repos]
        self.logger.info(
            f"🔍 {len(repo_names)} repositories found for {username}: {repo_names}"
        )

        return repo_names

    def get_commit_languages(self, username, repo):
        """
        Retrieves the programming languages used in a specific repository
        by analyzing modified file extensions in recent commits.

        Args:
            username (str): The GitHub username.
            repo (str): The repository name.

        Returns:
            Counter: A counter object with language usage counts.

        Limits the number of commits analyzed per repository to MAX_COMMITS_PER_REPO.
        """
        path = f"/repos/{username}/{repo}/commits?author={username}&per_page={self.MAX_COMMITS_PER_REPO}"
        commits = self.github_client_service.request_with_rate_limit(path)

        language_usage = Counter()

        if not commits:
            self.logger.warning(f"⚠️ No commits found in {repo} for {username}")
            return language_usage

        for commit in commits:
            commit_sha = commit["sha"]
            files = self.get_commit_files(username, repo, commit_sha)
            if not files:
                self.logger.warning(
                    f"⚠️ No files found in commit {commit_sha} of {repo}"
                )
                continue

            files = files[
                : self.MAX_FILES_PER_COMMIT
            ]  # Limit the number of files analyzed

            self.logger.info(
                f"📌 Commit {commit_sha} in {repo} contains {len(files)} analyzed files."
            )

            for file in files:
                lang = self.infer_language(file)
                if lang:
                    language_usage[lang] += 1
                    self.logger.info(f"📝 File: {file} → Inferred as {lang}")

        return language_usage

    def get_commit_files(self, username, repo, sha):
        """
        Fetches the list of files modified in a commit.

        Args:
            username (str): The GitHub username.
            repo (str): The repository name.
            sha (str): The commit SHA identifier.

        Returns:
            list: A list of filenames modified in the commit.
        """
        path = f"/repos/{username}/{repo}/commits/{sha}"
        commit_data = self.github_client_service.request_with_rate_limit(path)

        if "files" not in commit_data:
            return []

        return [file["filename"] for file in commit_data["files"]]

    @staticmethod
    def infer_language(filename):
        """
        Infers the programming language based on the file extension.

        Args:
            filename (str): The name of the file.

        Returns:
            str or None: The inferred programming language, or None if the extension is unknown.
        """
        ext_to_lang = {
            ".py": "Python",
            ".js": "JavaScript",
            ".java": "Java",
            ".cpp": "C++",
            ".c": "C",
            ".rs": "Rust",
            ".go": "Go",
            ".php": "PHP",
            ".ts": "TypeScript",
            ".swift": "Swift",
            ".kt": "Kotlin",
            ".rb": "Ruby",
            ".cs": "C#",
            ".html": "HTML",
            ".css": "CSS",
        }
        for ext, lang in ext_to_lang.items():
            if filename.endswith(ext):
                return lang
        return None
