import json
import glob
import os

NEW_KEYS_EN = {
    "view_mode": "View",
    "view_treemap": "Treemap",
    "view_matrix": "Scatter Matrix",
    "theme_toggle": "Toggle Theme",
    "export_png": "Export PNG",
    "filters_title": "Filters & Facets",
    "filter_sector": "Sector",
    "filter_all_sectors": "All Sectors",
    "filter_edu": "Education",
    "filter_all_edu": "All Levels",
    "filter_min_exposure": "Min. AI Exposure",
    "filter_reset": "Reset Filters",
    "rankings_title": "Occupational Rankings",
    "top_exposed": "Top AI-Exposed",
    "top_resilient": "Most AI-Resilient",
    "drawer_title": "Occupation Profile",
    "isco_code": "ISCO Code",
    "ai_risk_score": "AI Exposure Score",
    "ai_rationale": "AI Assessment Rationale",
    "country_pay": "Median Pay (Region)",
    "eu_benchmark_pay": "EU27 Benchmark Pay",
    "workforce_share": "Workforce Share",
    "share_link": "Copy Link",
    "link_copied": "Copied to clipboard!",
    "view_esco_portal": "View on ESCO Portal",
    "close": "Close",
    "quadrant_q1": "High Pay · High Exposure",
    "quadrant_q2": "High Pay · Low Exposure",
    "quadrant_q3": "Low Pay · Low Exposure",
    "quadrant_q4": "Low Pay · High Exposure",
    "quadrant_q1_desc": "High-value digital knowledge work facing major AI restructuring.",
    "quadrant_q2_desc": "High-value technical, clinical, and physical roles with high resilience.",
    "quadrant_q3_desc": "Physical, manual, and service trades shielded by manual dexterity.",
    "quadrant_q4_desc": "Routine clerical, support, and repetitive digital processing roles."
}

NEW_KEYS_ES = {
    "view_mode": "Vista",
    "view_treemap": "Treemap",
    "view_matrix": "Matriz Cuadrante",
    "theme_toggle": "Cambiar Tema",
    "export_png": "Exportar PNG",
    "filters_title": "Filtros y Facetas",
    "filter_sector": "Sector",
    "filter_all_sectors": "Todos los sectores",
    "filter_edu": "Educación",
    "filter_all_edu": "Todos los niveles",
    "filter_min_exposure": "Exp. IA Mínima",
    "filter_reset": "Limpiar filtros",
    "rankings_title": "Rankings de Ocupaciones",
    "top_exposed": "Más Expuestas a IA",
    "top_resilient": "Más Resilientes / Seguras",
    "drawer_title": "Ficha de Ocupación",
    "isco_code": "Código ISCO",
    "ai_risk_score": "Índice de Exposición a IA",
    "ai_rationale": "Evaluación y Razonamiento IA",
    "country_pay": "Sueldo Medio (Región)",
    "eu_benchmark_pay": "Sueldo Medio UE27",
    "workforce_share": "Cuota del Empleo",
    "share_link": "Copiar Enlace",
    "link_copied": "¡Copiado al portapapeles!",
    "view_esco_portal": "Ver en Portal Oficial ESCO",
    "close": "Cerrar",
    "quadrant_q1": "Alto Sueldo · Alta Exposición",
    "quadrant_q2": "Alto Sueldo · Baja Exposición",
    "quadrant_q3": "Bajo Sueldo · Baja Exposición",
    "quadrant_q4": "Bajo Sueldo · Alta Exposición",
    "quadrant_q1_desc": "Empleos de alto valor digital con fuerte reestructuración por IA.",
    "quadrant_q2_desc": "Especialistas técnicos, clínicos y físicos de alta resiliencia.",
    "quadrant_q3_desc": "Oficios manuales, de servicio y físicos protegidos por destreza real.",
    "quadrant_q4_desc": "Puestos administrativos y de procesamiento digital repetitivo bajo presión."
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
