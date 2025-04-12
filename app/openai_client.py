import openai
from typing import Dict, Optional
from .logger import setup_logger

logger = setup_logger()

class OpenAIClient:
    """Class to handle OpenAI API interactions."""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI client with API key."""
        self.api_key = api_key
        openai.api_key = api_key
    
    def analyze_code(self, code: str, code_type: str, language: str = "English") -> str:
        """Analyze code using OpenAI API."""
        if not code or not isinstance(code, str):
            logger.error("Invalid code input")
            return "Error: Invalid code input"
        
        if language not in ["English", "Arabic"]:
            logger.error(f"Unsupported language: {language}")
            return "Error: Unsupported language"
        
        try:
            system_prompt = self._get_system_prompt(code_type, language)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please review this code:\n\n{code}"}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message['content']
            
        except openai.error.RateLimitError:
            logger.error("OpenAI API rate limit exceeded")
            return "Error: Rate limit exceeded. Please try again later."
        except openai.error.AuthenticationError:
            logger.error("Invalid OpenAI API key")
            return "Error: Invalid API key. Please check your configuration."
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"Error: OpenAI API error occurred. Please try again later."
        except Exception as e:
            logger.error(f"Unexpected error during code analysis: {str(e)}")
            return f"Error analyzing code: {str(e)}"
    
    def _get_system_prompt(self, code_type: str, language: str) -> str:
        """Get the appropriate system prompt based on language."""
        prompts = {
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
        return prompts.get(language, prompts["English"]) 