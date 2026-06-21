from googletrans import Translator  # veya deep_translator

translator = Translator()

def translate_text(text, target_lang='tr'):
    try:
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception:
        return text  # çeviri başarısız olursa orijinal