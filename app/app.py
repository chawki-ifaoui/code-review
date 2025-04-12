from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from logger import setup_logger
from code_analysis import CodeAnalyzer
from openai_client import OpenAIClient
import requests

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logger()

def get_api_key() -> str:
    """
    Retrieve the OpenAI API key from environment variables.
    Raises ValueError if the API key is not found.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    return api_key

def validate_api_key(api_key: str) -> bool:
    """
    Validate the OpenAI API key format.
    Raises ValueError if the API key format is invalid.
    """
    if not api_key.startswith('sk-'):
        raise ValueError("Invalid OpenAI API key format")
    return True

def fetch_pull_request_code(pull_request_url: str, github_token: str) -> str:
    """
    Fetch the code from a pull request using the GitHub API.
    Raises requests.exceptions.RequestException if the request fails.
    """
    response = requests.get(pull_request_url, headers={'Authorization': f'token {github_token}'})
    if response.status_code != 200:
        raise requests.exceptions.RequestException(f"Failed to fetch pull request: {response.status_code}")
    pull_request_data = response.json()
    return pull_request_data.get('body', '')

def post_comment_to_pull_request(pull_request_url: str, comment: str, github_token: str) -> None:
    """
    Post a comment to a pull request using the GitHub API.
    Raises requests.exceptions.RequestException if the request fails.
    """
    comments_url = f"{pull_request_url}/comments"
    response = requests.post(comments_url, json={'body': comment}, headers={'Authorization': f'token {github_token}'})
    if response.status_code != 201:
        raise requests.exceptions.RequestException(f"Failed to post comment: {response.status_code}")

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Initialize components
try:
    api_key = get_api_key()
    validate_api_key(api_key)
    openai_client = OpenAIClient(api_key)
    code_analyzer = CodeAnalyzer()
except ValueError as e:
    logger.error(f"Initialization error: {str(e)}")
    # You might want to handle this error differently in production

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze the provided code using the OpenAI API.
    Returns the analysis results in both English and Arabic.
    """
    try:
        code = request.form.get('code', '')
        if not code:
            logger.warning("No code provided in request")
            return jsonify({
                'error': 'No code provided',
                'status': 'error'
            }), 400
        
        # Detect code type
        code_type = code_analyzer.detect_code_type(code)
        logger.info(f"Detected code type: {code_type}")
        
        # Highlight the code
        highlighted_code, css_styles = code_analyzer.highlight_code(code)
        
        # Get AI analysis in both languages
        analysis_en = openai_client.analyze_code(code, code_type, "English")
        analysis_ar = openai_client.analyze_code(code, code_type, "Arabic")
        
        # Convert markdown to HTML for both languages
        analysis_html_en = code_analyzer.convert_markdown_to_html(analysis_en)
        analysis_html_ar = code_analyzer.convert_markdown_to_html(analysis_ar)
        
        logger.info("Code analysis completed successfully")
        return jsonify({
            'status': 'success',
            'highlighted_code': highlighted_code,
            'css_styles': css_styles,
            'analysis_en': analysis_html_en,
            'analysis_ar': analysis_html_ar
        })
    except Exception as e:
        logger.error(f"Error during code analysis: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle GitHub webhook events for pull requests.
    Fetches code from the pull request, analyzes it, and posts comments back to the pull request.
    """
    data = request.json
    if data.get('action') == 'opened' and 'pull_request' in data:
        try:
            # Fetch code from the pull request
            pull_request_url = data['pull_request']['url']
            code = fetch_pull_request_code(pull_request_url, os.getenv('GITHUB_TOKEN'))
            
            # Analyze the code
            analysis = openai_client.analyze_code(code, 'python', 'English')
            if not analysis:
                logger.error("Failed to analyze code")
                return jsonify({'status': 'error', 'message': 'Failed to analyze code'}), 500
            
            # Post comments back to the pull request
            post_comment_to_pull_request(pull_request_url, analysis, os.getenv('GITHUB_TOKEN'))
            
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'ignored'}), 200

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'development':
        app.run(debug=True)
    else:
        app.run(debug=False) 