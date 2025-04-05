# AI-Powered Code Review Assistant

An intelligent code review assistant that uses AI to analyze code and provide detailed feedback on code quality, best practices, potential bugs, security concerns, and performance improvements.

## Features

- Syntax highlighting for multiple programming languages
- Real-time code analysis using GPT-4
- Modern, responsive UI
- Detailed feedback on multiple aspects of code quality
- Markdown rendering for analysis results

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd codereview
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
python app/app.py
```
3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Paste your code into the input textarea on the left side
2. Click the "Analyze Code" button
3. Wait for the analysis to complete
4. Review the highlighted code and AI-generated feedback on the right side

## Security Note

- Never commit your `.env` file or expose your API keys
- The application is set up for development use. For production deployment, ensure proper security measures are in place

## Requirements

- Python 3.7+
- OpenAI API key
- Modern web browser # code-review
