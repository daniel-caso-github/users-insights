# GitHub User Insights API

A FastAPI-based API that provides insights into GitHub users, including their most-used languages, repositories with the most pull requests, monthly contributions, and active hours.

## 📌 Features

- 🚀 Retrieve GitHub user activity data
- 🔍 Analyze most-used programming languages
- 📊 Track repositories with the most pull requests
- 📆 Display monthly contribution history
- ⏰ Identify the user's most active hours

## 🛠️ Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/github-insights-api.git
cd github-insights-api
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### Install Dependencies

```bash
pip install -r requirements/requirements.txt
```

### Set Up Environment Variables
Create a .env file in the root directory and add the following:

```
GITHUB_API_URL=https://api.github.com
GITHUB_TOKEN=your_github_personal_access_token
```
### ⚠️ Generate a GitHub Token

To authenticate with the GitHub API, you need a **Personal Access Token (PAT)**. Follow these steps to generate one:

1. **Visit the GitHub token generation page:**  
   👉 [Generate a new personal access token](https://github.com/settings/personal-access-tokens/new)
   
2. **Under "Note",** give your token a meaningful name (e.g., `GitHub Insights API`).

3. **Set an expiration date** as needed.

4. **Under "Scopes (Permissions)", select the following:**
- ✅ **`repo`** → Full control of private repositories *(only if analyzing private repos)*
- ✅ **`read:user`** → Read access to user profile
- ✅ **`read:org`** → Read access to organization memberships
- ✅ **`public_repo`** → Access public repositories
- ✅ **`read:repo_hook`** → Read repository hooks *(optional)*
- ✅ **`read:packages`** → Read GitHub packages *(optional)*

5. Click **"Generate token"**, then copy and store it securely.

6. Replace `your_github_personal_access_token` in the `.env` file with your actual token.

### 🚀 Running the API
Start the FastAPI application with:

```bash
uvicorn main:app --reload
```

The API will be available at: http://127.0.0.1:8000

### 📜 API Documentation

Once the server is running, you can explore the API using interactive documentation:

- 📄 **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 🔥 Available Endpoints
```
GET /user-insights/{username}
```

Description:
Returns various metrics about a GitHub user’s activity.

```
{
  "most_used_languages": [
    {"language": "Python", "count": 10},
    {"language": "JavaScript", "count": 5}
  ],
  "repos_with_more_prs": [
    {"repository": "https://github.com/user/repo1", "count": 3}
  ],
  "monthly_contributions": [
    {"month": "2025-02", "pull_requests": 2, "issues": 3, "commits": 10}
  ],
  "hours_more_activity": [
    {"period": "morning", "count": 5},
    {"period": "afternoon", "count": 8},
    {"period": "evening", "count": 12}
  ]
}
```

### 📡 API Responses

- ✅ **200 OK** - Data retrieved successfully.
- ❌ **404 Not Found** - GitHub user not found.
- ⚠️ **500 Internal Server Error** - Unexpected error.

### 🧪 Running Tests

To run unit and integration tests:
```bash
pytest tests/
```

For verbose test output:

```bash
pytest -v
```

### 🔍 Logging & Error Handling
- ✅ Structured logging is implemented using `logging` to track API calls, warnings, and errors.
- ❌ Exception handling is integrated with FastAPI to return proper status codes and error messages.

### 🛠️ Future Improvements
- Caching API responses to reduce GitHub API calls
- Advanced user activity tracking
- More efficient data processing and aggregation


### 🤝 Contributing

Feel free to open issues or submit pull requests for improvements!


### 📜 License
This project is licensed under the MIT License.

### 🚀 Happy Coding!

Let me know if you need any modifications! 🚀
