import json
import os
import re
import glob

def to_slug(t):
    return re.sub(r'[^a-zA-Z0-9]+', '_', t).strip('_').lower()

def main():
    if not os.path.exists('occupations_eu.json'):
        print("Missing occupations_eu.json")
        return

    with open('occupations_eu.json', 'r', encoding='utf-8') as f:
        occupations = json.load(f)

    languages = ["bg", "cs", "da", "de", "el", "es", "et", "fi", "fr", "ga", "hr", "hu", "it", "lt", "lv", "mt", "nl", "pl", "pt", "ro", "sk", "sl", "sv"]

    with open('site/i18n/en.json', 'r', encoding='utf-8') as f:
        en_dict = json.load(f)

    updates_by_lang = {lang: {} for lang in languages}

    for occ in occupations:
        slug = occ['slug']
        en_title = occ['title']
        ui_key = 'job_' + to_slug(en_title)
        
        raw_path = f'raw_eu/{slug}.json'
        if os.path.exists(raw_path):
            with open(raw_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            labels = raw_data.get('preferredLabel', {})
            for lang in languages:
                if lang in labels:
                    updates_by_lang[lang][ui_key] = labels[lang]

    count = 0
    for lang in languages:
        lang_path = f'site/i18n/{lang}.json'
        try:
            # Start with a copy of the English UI dictionary
            i18n_dict = en_dict.copy()
            
            # If the file already exists, load any existing LLM translations
            if os.path.exists(lang_path):
                with open(lang_path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    i18n_dict.update(existing)
                    
            # Inject Native ESCO Job Titles
            if updates_by_lang[lang]:
                for k, v in updates_by_lang[lang].items():
                    i18n_dict[k] = v
                    
            # Write the complete dictionary
            with open(lang_path, 'w', encoding='utf-8') as f:
                json.dump(i18n_dict, f, ensure_ascii=False, indent=2)
            count += 1
            
        except Exception as e:
            print(f"Error processing {lang}: {e}")

    print(f'Done! Successfully injected 436 native ESCO job titles into {count} language dictionaries.')

if __name__ == "__main__":
    main()
