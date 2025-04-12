from typing import Dict, Tuple, Optional
import re
from pygments import highlight
from pygments.lexers import guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter
from markdown import markdown

class CodeAnalyzer:
    """Class to handle code analysis operations."""
    
    def __init__(self):
        self.patterns: Dict[str, Tuple[str, str]] = {
            'html': (r'<[^>]+>', 'HTML'),
            'css': (r'{[^}]+}|@media|@import|#[\w-]+\s*{', 'CSS'),
            'javascript': (r'function\s+\w+|const|let|var|=>|window\.|document\.', 'JavaScript'),
            'python': (r'def\s+\w+|import\s+\w+|class\s+\w+|if\s+__name__\s*==|print\(', 'Python'),
            'sql': (r'SELECT|INSERT|UPDATE|DELETE|CREATE TABLE|ALTER TABLE', 'SQL'),
        }
    
    def detect_code_type(self, code: str) -> str:
        """Detect the type of code and any obvious syntax issues."""
        if not code or not isinstance(code, str):
            return "Unknown"
        
        # Count matches for each language to find the best match
        matches: Dict[str, int] = {}
        for lang, (pattern, name) in self.patterns.items():
            count = len(re.findall(pattern, code, re.IGNORECASE))
            matches[name] = count
        
        # Return the language with the most matches, or Unknown if no matches
        if matches:
            return max(matches.items(), key=lambda x: x[1])[0]
        return "Unknown"
    
    def highlight_code(self, code: str) -> Tuple[str, str]:
        """Highlight code with syntax highlighting and error handling."""
        if not code or not isinstance(code, str):
            return "", ""
        
        try:
            # Try to guess the lexer, fall back to TextLexer if can't determine
            try:
                lexer = guess_lexer(code)
            except:
                lexer = TextLexer()
            
            formatter = HtmlFormatter(
                style='monokai',
                linenos=True,
                cssclass='highlight',
                lineanchors='line',
                wrapcode=True
            )
            return highlight(code, lexer, formatter), formatter.get_style_defs('.highlight')
        except Exception as e:
            return code, ""
    
    def convert_markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown text to HTML."""
        if not markdown_text:
            return ""
        return markdown(markdown_text) 