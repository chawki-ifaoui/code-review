# AI-Powered Code Review Assistant

## Project Description
This project is an AI-powered code review assistant that analyzes code using the OpenAI API. It provides feedback on code quality, syntax, and best practices in both English and Arabic.

## Setup Instructions
1. **Clone the Repository**: 
   ```bash
   git clone <git@github.com:chawki-ifaoui/code-review.git>
   cd <codereview>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GITHUB_TOKEN=your_github_token
   FLASK_ENV=development
   ```

## Usage Instructions
1. **Run the Application**:
   ```bash
   python app/app.py
   ```

2. **Access the Web Interface**:
   Open a web browser and navigate to `http://localhost:8000`.

3. **Analyze Code**:
   - Paste your code into the input field.
   - Click the "Analyze Code" button to receive feedback.

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key.
- `GITHUB_TOKEN`: Your GitHub API token for webhook integration.
- `FLASK_ENV`: Set to `development` for debug mode, or `production` for production mode.

## API Documentation
### Endpoints
- **POST /analyze**: Analyze the provided code and return the analysis results.
  - **Request Body**: `code` (string)
  - **Response**: JSON object with analysis results.

- **POST /webhook**: Handle GitHub webhook events for pull requests.
  - **Request Body**: JSON object with pull request data.
  - **Response**: JSON object with status and message.

## Features

- Syntax highlighting for multiple programming languages
- Real-time code analysis using GPT-4
- Modern, responsive UI
- Detailed feedback on multiple aspects of code quality
- Markdown rendering for analysis results

## Security Note

- Never commit your `.env` file or expose your API keys
- The application is set up for development use. For production deployment, ensure proper security measures are in place

## Requirements

- Python 3.7+
- OpenAI API key
- Modern web browser
