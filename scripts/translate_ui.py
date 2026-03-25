import json
import os
import time
from google import genai
from google.genai import types

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("ERROR: Set GEMINI_API_KEY in .env or as an environment variable.")
client = genai.Client(api_key=api_key)

# The base English dictionary
with open("site/i18n/en.json", "r", encoding="utf-8") as f:
    en_dict = json.load(f)

# The 23 other EU languages
languages = {
    "bg": "Bulgarian",
    "cs": "Czech",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "ga": "Irish",
    "hr": "Croatian",
    "hu": "Hungarian",
    "it": "Italian",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mt": "Maltese",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sv": "Swedish"
}

os.makedirs("site/i18n", exist_ok=True)

# Generate JSON schema from the keys of en_dict
schema_properties = {k: {"type": "string"} for k in en_dict.keys()}
response_schema = {
    "type": "object",
    "properties": schema_properties,
    "required": list(en_dict.keys())
}

for code, lang in languages.items():
    output_path = f"site/i18n/{code}.json"
    
    if os.path.exists(output_path):
        print(f"[{code}] {lang} already exists, skipping.")
        continue
        
    print(f"Translating to {lang} ({code})...", end=" ", flush=True)
    
    prompt = f"""
    You are an expert technical translator. Translate the following JSON object containing UI text for a data visualization web application from English into {lang}.
    
    CRITICAL RULES:
    1. Translate the VALUES only. Ensure the KEYS remain exactly the same.
    2. The values belong strictly to web UI elements like buttons, charts, titles, strings, tooltips, and labels.
    3. Keep any HTML formatting (like <b>, <em>, <a href="...">) exactly intact in the translated output! Do not modify URLs.
    4. Provide the exact structure back in valid JSON format.
    5. Translate naturally to native {lang}.

    Source JSON:
    {json.dumps(en_dict, indent=2)}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        
        translated_json = json.loads(response.text)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(translated_json, f, ensure_ascii=False, indent=2)
            
        print("OK")
        time.sleep(4.5) # Slight delay to avoid hammering the API (15 RPM free tier)
    except Exception as e:
        print(f"FAILED: {e}")

print("\nTranslation complete.")
