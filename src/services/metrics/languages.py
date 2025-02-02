from collections import Counter

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class LanguagesMostUsed(BaseGitHubMetric):
    """
    A GitHub metric that infers the most used programming languages
    based on GitHub's language API and commit analysis.

    Methods:
        execute(username): Retrieves the user's most used languages.
        get_repositories(username): Fetches a list of repositories the user contributed to.
        get_languages_from_repo(username, repo): Uses GitHub's API to get language stats per repo.
    """

    def __init__(self):
        """Initializes the metric with a predefined execution order and logger."""
        super().__init__()
        self.order = OderService.language_most_used.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()

    def execute(self, username):
        """
        Retrieves the most used programming languages by analyzing repository statistics.
        """
        self.logger.info(f"📊 Starting language analysis for {username}")

        repos = self.get_repositories(username)
        if not repos:
            self.logger.warning(f"⚠️ No repositories found for {username}")
            return self.format_response("most_used_languages", [])

        language_counter = Counter()

        for repo in repos:
            self.logger.info(f"🔍 Fetching language stats for repository: {repo}")
            languages = self.get_languages_from_repo(username, repo)
            language_counter.update(languages)

        most_used = [
            {"language": lang, "count": count}
            for lang, count in language_counter.most_common(3)
        ]
        self.logger.info(f"✅ Top 3 languages for {username}: {most_used}")

        return self.format_response("most_used_languages", most_used)

    def get_repositories(self, username):
        """Fetches a list of repositories owned by the user."""
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

    def get_languages_from_repo(self, username, repo):
        """
        Uses GitHub's built-in API to fetch language statistics for a repository.

        Returns:
            Counter: A counter object with language usage counts.
        """
        path = f"/repos/{username}/{repo}/languages"
        data = self.github_client_service.request_with_rate_limit(path)

        if not data:
            self.logger.warning(f"⚠️ No language data found for repository: {repo}")
            return Counter()

        language_usage = Counter(data)

        self.logger.info(f"✅ Language stats for {repo}: {dict(language_usage)}")

        return language_usage

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
            ".pyw": "Python",
            ".java": "Java",
            ".class": "Java",
            ".jar": "Java",
            ".c": "C",
            ".h": "C/C++ Header",
            ".cpp": "C++",
            ".hpp": "C++ Header",
            ".cc": "C++",
            ".cs": "C#",
            ".html": "HTML",
            ".htm": "HTML",
            ".css": "CSS",
            ".scss": "SASS",
            ".sass": "SASS",
            ".less": "LESS",
            ".xml": "XML",
            ".xhtml": "XHTML",
            ".json": "JSON",
            ".js": "JavaScript",
            ".mjs": "JavaScript",
            ".cjs": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript (React)",
            ".jsx": "JavaScript (React)",
            ".php": "PHP",
            ".phtml": "PHP",
            ".swift": "Swift",
            ".m": "Objective-C",
            ".mm": "Objective-C++",
            ".rs": "Rust",
            ".go": "Go",
            ".rb": "Ruby",
            ".erb": "Embedded Ruby",
            ".rake": "Ruby Rakefile",
            ".pl": "Perl",
            ".pm": "Perl Module",
            ".sh": "Shell Script",
            ".bash": "Shell Script",
            ".zsh": "Zsh Script",
            ".ps1": "PowerShell",
            ".psm1": "PowerShell Module",
            ".kt": "Kotlin",
            ".kts": "Kotlin Script",
            ".dart": "Dart",
            ".ipynb": "Jupyter Notebook",
            ".yml": "YAML",
            ".yaml": "YAML",
            ".toml": "TOML",
            ".ini": "INI",
            ".cfg": "Config",
            ".sql": "SQL",
            ".csv": "CSV",
            ".tsv": "TSV",
            ".r": "R",
            ".rmd": "R Markdown",
            ".md": "Markdown",
            ".txt": "Text",
            ".rst": "reStructuredText",
            ".bat": "Batch File",
            ".dockerfile": "Dockerfile",
            ".makefile": "Makefile",
            ".gradle": "Gradle",
            ".groovy": "Groovy",
            ".cmake": "CMake",
            ".vbs": "VBScript",
            ".wsf": "Windows Script File",
            ".gml": "GameMaker Language",
            ".godot": "Godot Script",
            ".gd": "Godot Script",
            ".lua": "Lua",
            ".f90": "Fortran",
            ".f95": "Fortran",
            ".asm": "Assembly",
            ".s": "Assembly",
            ".clj": "Clojure",
            ".cljs": "ClojureScript",
            ".el": "Emacs Lisp",
            ".lisp": "Lisp",
            ".ml": "OCaml",
            ".hs": "Haskell",
            ".erl": "Erlang",
            ".ex": "Elixir",
            ".exs": "Elixir Script",
            ".scala": "Scala",
            ".v": "Verilog",
            ".sv": "SystemVerilog",
            ".vb": "Visual Basic",
            ".pas": "Pascal",
            ".d": "D",
            ".nim": "Nim",
        }
        for ext, lang in ext_to_lang.items():
            if filename.endswith(ext):
                return lang
        return None
