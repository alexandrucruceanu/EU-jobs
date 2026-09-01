import json
import glob
import os

NEW_KEYS_EN = {
    "quiz_btn": "⚡ Check Your Job",
    "quiz_modal_title": "Personal AI Job Impact Calculator",
    "quiz_modal_sub": "Find out your AI exposure score, salary rank, and risk level across the European labor market.",
    "quiz_step1_label": "1. Select your occupation:",
    "quiz_search_placeholder": "Type job title (e.g. Software, Nurse, Accountant)...",
    "quiz_step2_label": "2. Select country:",
    "quiz_step3_label": "3. Optional: Your annual salary (€):",
    "quiz_calculate_btn": "Generate Career Impact Card",
    "quiz_result_badge_high": "High AI Exposure · Restructuring",
    "quiz_result_badge_mid": "Moderate Exposure · Augmentation",
    "quiz_result_badge_low": "Resilient Role · Shielded",
    "quiz_download_card": "Download Image (PNG)",
    "quiz_copy_post": "Copy Share Text",
    "quiz_share_x": "Share on X",
    "quiz_share_linkedin": "Share on LinkedIn",
    "quiz_explore_in_treemap": "Explore in Treemap"
}

NEW_KEYS_ES = {
    "quiz_btn": "⚡ ¿Qué tan expuesto está tu empleo?",
    "quiz_modal_title": "Calculadora de Impacto de IA Personal",
    "quiz_modal_sub": "Descubre tu nivel de exposición a la IA, rango salarial y nivel de riesgo en el mercado laboral europeo.",
    "quiz_step1_label": "1. Selecciona tu profesión:",
    "quiz_search_placeholder": "Escribe tu empleo (ej. Software, Enfermero, Contable)...",
    "quiz_step2_label": "2. Selecciona país:",
    "quiz_step3_label": "3. Opcional: Tu sueldo anual (€):",
    "quiz_calculate_btn": "Generar Mi Tarjeta de Impacto",
    "quiz_result_badge_high": "Alta Exposición a IA · Reestructuración",
    "quiz_result_badge_mid": "Exposición Moderada · Aumento",
    "quiz_result_badge_low": "Profesión Resiliente · Protegida",
    "quiz_download_card": "Descargar Imagen (PNG)",
    "quiz_copy_post": "Copiar Texto para Redes",
    "quiz_share_x": "Compartir en X",
    "quiz_share_linkedin": "Compartir en LinkedIn",
    "quiz_explore_in_treemap": "Ver en el Treemap"
}

def update_all_i18n():
    i18n_dir = os.path.join(os.path.dirname(__file__), "..", "site", "i18n")
    for filepath in glob.glob(os.path.join(i18n_dir, "*.json")):
        lang = os.path.basename(filepath).replace(".json", "")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        keys_to_use = NEW_KEYS_ES if lang == "es" else NEW_KEYS_EN
        for k, v in keys_to_use.items():
            if k not in data:
                data[k] = v
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {lang}.json")

if __name__ == "__main__":
    update_all_i18n()
