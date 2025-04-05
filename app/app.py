from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
from pygments import highlight
from pygments.lexers import guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter
from markdown import markdown
import re

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',  # Point to templates directory in project root
           static_folder='../static')       # Point to static directory in project root

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def detect_code_type(code):
    """Detect the type of code and any obvious syntax issues."""
    patterns = {
        'html': (r'<[^>]+>', 'HTML'),
        'css': (r'{[^}]+}|@media|@import|#[\w-]+\s*{', 'CSS'),
        'javascript': (r'function\s+\w+|const|let|var|=>|window\.|document\.', 'JavaScript'),
        'python': (r'def\s+\w+|import\s+\w+|class\s+\w+|if\s+__name__\s*==|print\(', 'Python'),
        'sql': (r'SELECT|INSERT|UPDATE|DELETE|CREATE TABLE|ALTER TABLE', 'SQL'),
    }
    
    for pattern, lang in patterns.values():
        if re.search(pattern, code, re.IGNORECASE):
            return lang
    return "Unknown"

def analyze_code_with_language(code, language="English"):
    try:
        # Detect code type
        code_type = detect_code_type(code)
        
        system_prompt = {
            "English": f"""You are a code review expert specializing in {code_type}. Analyze the code and provide detailed feedback in the following format:

1. Code Type: [Detected programming language/framework]
2. Syntax Check:
   - List any syntax errors or invalid code
   - Highlight missing brackets, semicolons, or indentation issues
3. Code Quality Issues:
   - Point out any bad practices or anti-patterns
   - Identify unclear naming or poor structure
4. Suggested Improvements:
   - Provide specific code examples for better implementation
   - Show before/after comparisons where relevant
5. Best Practices:
   - List relevant best practices for this type of code
   - Include language-specific recommendations

If the input is not valid code or contains serious issues, explain why and provide guidance on proper implementation.""",

            "Arabic": f"""أنت خبير في مراجعة الكود متخصص في {code_type}. قم بتحليل الكود وتقديم ملاحظات مفصلة بالتنسيق التالي:

١. نوع الكود: [لغة البرمجة/الإطار المكتشف]
٢. فحص بناء الجملة:
   - سرد أي أخطاء في بناء الجملة أو الكود غير الصالح
   - تسليط الضوء على الأقواس المفقودة أو الفواصل المنقوطة أو مشاكل المسافة البادئة
٣. مشاكل جودة الكود:
   - الإشارة إلى أي ممارسات سيئة أو أنماط غير مرغوب فيها
   - تحديد التسميات غير الواضحة أو الهيكل الضعيف
٤. التحسينات المقترحة:
   - تقديم أمثلة محددة للكود للتنفيذ الأفضل
   - عرض مقارنات قبل/بعد حيثما كان ذلك مناسباً
٥. أفضل الممارسات:
   - سرد أفضل الممارسات ذات الصلة لهذا النوع من الكود
   - تضمين توصيات خاصة باللغة

إذا كان الإدخال ليس كوداً صالحاً أو يحتوي على مشاكل خطيرة، اشرح السبب وقدم إرشادات حول التنفيذ الصحيح."""
        }

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt[language]},
                {"role": "user", "content": f"Please review this code:\n\n{code}"}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error analyzing code: {str(e)}"

def highlight_code(code):
    try:
        # Try to guess the lexer, fall back to TextLexer if can't determine
        try:
            lexer = guess_lexer(code)
        except:
            lexer = TextLexer()
            
        formatter = HtmlFormatter(style='monokai', linenos=True)
        return highlight(code, lexer, formatter), formatter.get_style_defs('.highlight')
    except Exception:
        return code, ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form.get('code', '')
    if not code:
        return jsonify({'error': 'No code provided'})
    
    # Highlight the code
    highlighted_code, css_styles = highlight_code(code)
    
    # Get AI analysis in both languages
    analysis_en = analyze_code_with_language(code, "English")
    analysis_ar = analyze_code_with_language(code, "Arabic")
    
    # Convert markdown to HTML for both languages
    analysis_html_en = markdown(analysis_en)
    analysis_html_ar = markdown(analysis_ar)
    
    return jsonify({
        'highlighted_code': highlighted_code,
        'css_styles': css_styles,
        'analysis_en': analysis_html_en,
        'analysis_ar': analysis_html_ar
    })

if __name__ == '__main__':
    app.run(debug=True) 