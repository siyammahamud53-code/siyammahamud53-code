"""
SYNAPSE AI - Language Router Module
এই মডিউল ইউজারের ইনপুটের ভাষা শনাক্ত করে এবং সেই ভাষায় উত্তর তৈরির নির্দেশনা দেয়।
"""

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import re

# ভাষা ডিটেকশনের জন্য সিড সেট করা (নির্ভুলতার জন্য)
DetectorFactory.seed = 0

class LanguageRouter:
    def __init__(self):
        # ===== সাপোর্টেড ভাষার তালিকা =====
        self.supported_languages = {
            "bn": {
                "name": "বাংলা",
                "flag": "🇧🇩",
                "prompt_suffix": "অনুগ্রহ করে আপনার উত্তর সম্পূর্ণ বাংলায় দিন।",
                "is_native": True
            },
            "en": {
                "name": "English",
                "flag": "🇬🇧",
                "prompt_suffix": "Please respond in English only.",
                "is_native": False
            },
            "hi": {
                "name": "हिन्दी",
                "flag": "🇮🇳",
                "prompt_suffix": "कृपया अपना उत्तर पूरी तरह से हिंदी में दें।",
                "is_native": False
            },
            "ar": {
                "name": "العربية",
                "flag": "🇸🇦",
                "prompt_suffix": "يرجى الرد باللغة العربية فقط.",
                "is_native": False
            },
            "es": {
                "name": "Español",
                "flag": "🇪🇸",
                "prompt_suffix": "Por favor, responda solo en español.",
                "is_native": False
            },
            "fr": {
                "name": "Français",
                "flag": "🇫🇷",
                "prompt_suffix": "Veuillez répondre uniquement en français.",
                "is_native": False
            },
            "de": {
                "name": "Deutsch",
                "flag": "🇩🇪",
                "prompt_suffix": "Bitte antworten Sie nur auf Deutsch.",
                "is_native": False
            },
            "ja": {
                "name": "日本語",
                "flag": "🇯🇵",
                "prompt_suffix": "日本語のみで応答してください。",
                "is_native": False
            },
            "zh-cn": {
                "name": "中文 (简体)",
                "flag": "🇨🇳",
                "prompt_suffix": "请仅用中文回复。",
                "is_native": False
            }
        }

    def detect_language(self, text: str) -> dict:
        """
        টেক্সটের ভাষা শনাক্ত করে ভাষার তথ্য রিটার্ন করে।
        """
        if not text or len(text.strip()) < 2:
            # খুব ছোট টেক্সটের জন্য ডিফল্ট বাংলা
            return self.supported_languages["bn"]

        try:
            # ভাষা ডিটেক্ট করার চেষ্টা
            detected_lang = detect(text)
            
            # যদি ডিটেক্ট করা ভাষা আমাদের সাপোর্টেড তালিকায় থাকে
            if detected_lang in self.supported_languages:
                return self.supported_languages[detected_lang]
            
            # যদি সাপোর্টেড না হয়, তাহলে ডিফল্ট ইংরেজি
            print(f"⚠️ Language '{detected_lang}' not supported, defaulting to English")
            return self.supported_languages["en"]
            
        except LangDetectException:
            # ডিটেক্ট করতে না পারলে বাংলা (ডিফল্ট)
            print("⚠️ Could not detect language, defaulting to Bengali")
            return self.supported_languages["bn"]

    def get_language_specific_prompt(self, text: str, base_prompt: str) -> str:
        """
        ভাষা অনুযায়ী প্রম্পট তৈরি করে।
        """
        # ১. ভাষা ডিটেক্ট
        lang_info = self.detect_language(text)
        lang_code = [k for k, v in self.supported_languages.items() if v == lang_info][0]
        
        # ২. ভাষা-নির্দিষ্ট প্রম্পট তৈরি
        prompt = f"{base_prompt}\n\n{lang_info['prompt_suffix']}"
        
        # ৩. বাংলা হলে নিজের নাম যোগ করে দেওয়া (ব্যক্তিগতকরণ)
        if lang_code == "bn":
            prompt = f"{prompt}\nআপনি বাংলাদেশের একজন বন্ধু।"
        
        return prompt

    def translate_text_prompt(self, text: str) -> str:
        """
        ভাষা ডিটেক্ট করে সেই ভাষায় 'অনুবাদ করো' প্রম্পট তৈরি করে।
        """
        lang_info = self.detect_language(text)
        lang_code = [k for k, v in self.supported_languages.items() if v == lang_info][0]
        
        translation_prompts = {
            "bn": "অনুগ্রহ করে নিচের টেক্সটটি বাংলায় অনুবাদ করুন:\n",
            "en": "Please translate the following text into English:\n",
            "hi": "कृपया निम्नलिखित पाठ का हिंदी में अनुवाद करें:\n",
            "ar": "يرجى ترجمة النص التالي إلى العربية:\n",
            "es": "Por favor, traduzca el siguiente texto al español:\n",
            "fr": "Veuillez traduire le texte suivant en français:\n",
            "de": "Bitte übersetzen Sie den folgenden Text ins Deutsche:\n",
            "ja": "次のテキストを日本語に翻訳してください:\n",
            "zh-cn": "请将以下文本翻译成中文:\n"
        }
        
        return translation_prompts.get(lang_code, translation_prompts["en"])

    def get_detected_language_info(self, text: str) -> dict:
        """
        ডিটেক্ট করা ভাষার সম্পূর্ণ তথ্য রিটার্ন করে (UI-তে দেখানোর জন্য)।
        """
        lang_info = self.detect_language(text)
        lang_code = [k for k, v in self.supported_languages.items() if v == lang_info][0]
        
        return {
            "language_code": lang_code,
            "language_name": lang_info["name"],
            "flag": lang_info["flag"],
            "text": text[:50] + ("..." if len(text) > 50 else "")
        }

# ===== ফাইলটি ডাইরেক্ট রান করলে টেস্ট =====
if __name__ == "__main__":
    router = LanguageRouter()
    
    test_texts = [
        "আমি বাংলায় কথা বলি।",
        "I speak English.",
        "मैं हिंदी बोलता हूँ।",
        "أنا أتحدث العربية.",
        "Hola, ¿cómo estás?",
        "Bonjour, comment ça va?",
        "こんにちは、お元気ですか？"
    ]
    
    print("🌐 Language Router Test Results:\n" + "="*50)
    
    for text in test_texts:
        info = router.get_detected_language_info(text)
        print(f"📝 '{text}' → {info['flag']} {info['language_name']} ({info['language_code']})")
    
    print("\n" + "="*50)
    print("\n✅ Example Prompt Generation:")
    
    base_prompt = "You are a helpful AI assistant."
    test_msg = "আমি একটি নতুন গান লিখতে চাই।"
    generated_prompt = router.get_language_specific_prompt(test_msg, base_prompt)
    print(f"📌 Input: {test_msg}")
    print(f"📌 Generated Prompt:\n{generated_prompt}")
