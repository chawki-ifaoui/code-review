from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from logger import setup_logger
from code_analysis import CodeAnalyzer
from openai_client import OpenAIClient

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logger()

def validate_api_key() -> str:
    """Validate OpenAI API key is present and valid."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("OpenAI API key not found in environment variables")
        raise ValueError("OpenAI API key not found in environment variables")
    if not api_key.startswith('sk-'):
        logger.error("Invalid OpenAI API key format")
        raise ValueError("Invalid OpenAI API key format")
    return api_key

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Initialize components
try:
    api_key = validate_api_key()
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

if __name__ == '__main__':
    app.run(debug=True) 