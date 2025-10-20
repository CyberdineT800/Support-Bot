import json

class MyCustomException(Exception):
    def __init__(self, message="Default error message"):
        self.message = message
        super().__init__(self.message)

def load_language_config(file_path='data/languages.json'):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            langs = json.load(file)
        return langs
    except Exception as e:
        print(f"data/translations -> load_language_config -> {e}")
        return {}

def get_text(language, key):
    language_config = load_language_config()

    if language in language_config and key in language_config[language]:
        return language_config[language][key]
    else:
        raise MyCustomException(f"Tarjimada xatolik, Til: '{language}' and Kalit: '{key}'")
    
def get_values_for_key(key):
    language_config = load_language_config()
    values = []

    for lang, translations in language_config.items():
        if key in translations:
            values.append(translations[key])

    return values

# print(get_values_for_key("register"))
# selected_language = 'uz_kirill'  
# requested_text_key = 'welcome'  

# result = get_text(selected_language, requested_text_key)
# print(result)
