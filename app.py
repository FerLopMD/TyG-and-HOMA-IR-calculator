import math
import streamlit as st

# =========================
# Configuración general
# =========================
st.set_page_config(
    page_title="Calculadora TyG & HOMA-IR",
    page_icon="🧪",
    layout="centered"
)

AUTHOR = "E.M. Fernando López"
LAST_UPDATED = "10 de enero de 2026"

# =========================
# Puntos de corte (Son et al., 2022)
# =========================
TYG_PREVALENCE = 8.718
HOMA_PREVALENCE = 1.8

TYG_INCIDENCE = 8.518
HOMA_INCIDENCE = 1.5

# =========================
# Conversión de unidades
# =========================
GLU_MMOL_TO_MGDL = 18
TG_MMOL_TO_MGDL = 88.57

# =========================
# Funciones
# =========================
def calculate_tyg(tg_mgdl, glucose_mgdl):
    return math.log((tg_mgdl * glucose_mgdl) / 2)

def calculate_homa(glucose, insulin, unit):
    if unit == "mg/dL":
        return (glucose * insulin) / 405
    else:
        return (glucose * insulin) / 22.5

# =========================
# ENCABEZADO
# =========================
st.title("🧪 Calculadora TyG & HOMA-IR")
st.write(
    "Herramienta educativa basada en evidencia científica. "
    "**No sustituye la valoración de un médico.**"
)

st.markdown("---")

# =========================
# CALCULADORA
# =========================
st.header("Calculadora")

unit = st.radio(
    "Unidades para glucosa y triglicéridos:",
    ["mg/dL", "mmol/L"],
    index=0
)

tg = st.text_input(f"Triglicéridos en ayuno ({unit})")
glucose = st.text_input(f"Glucosa en ayuno ({unit})")
insulin = st.text_input("Insulina en ayuno (µU/mL)")

if st.button("Calcular"):
    try:
        tg = float(tg)
        glucose = float(glucose)
        insulin = float(insulin)

        if tg <= 0 or glucose <= 0 or insulin <= 0:
            st.error("Todos los valores deben ser mayores a 0.")
        else:
            if unit == "mmol/L":
                tg_mgdl = tg * TG_MMOL_TO_MGDL
                glucose_mgdl = glucose * GLU_MMOL_TO_MGDL
            else:
                tg_mgdl = tg
                glucose_mgdl = glucose

            tyg = calculate_tyg(tg_mgdl, glucose_mgdl)
            homa = calculate_homa(glucose, insulin, unit)

            st.markdown("---")
            st.subheader("Resultados")

            col1, col2 = st.columns(2)
            col1.metric("Índice TyG", f"{tyg:.3f}")
            col2.metric("HOMA-IR", f"{homa:.3f}")

            st.markdown("### Interpretación")

            if tyg >= TYG_INCIDENCE and homa >= HOMA_INCIDENCE:
                st.error(
                    "Ambos indicadores se encuentran elevados en comparación con valores poblacionales. "
                    "En estudios científicos, esta combinación se ha asociado con mayor riesgo metabólico. "
                    "**Se recomienda acudir con un médico para una evaluación integral.**"
                )
            elif tyg >= TYG_INCIDENCE or homa >= HOMA_INCIDENCE:
                st.warning(
                    "Uno de los indicadores se encuentra elevado en comparación con valores poblacionales. "
                    "Podría ser útil repetir estudios y consultar con un médico."
                )
            else:
                st.success(
                    "Los resultados se encuentran dentro de rangos bajos observados en estudios poblacionales. "
                    "Mantener hábitos saludables y seguimiento médico es importante."
                )

            st.info(
                "⚠️ Esta herramienta es informativa y educativa. "
                "No realiza diagnósticos ni sustituye la valoración médica."
            )

    except ValueError:
        st.error("Por favor ingresa solo valores numéricos.")

# =========================
# DEFINICIÓN DE SÍNDROME METABÓLICO
# =========================
st.markdown("---")
st.header("¿Qué es el síndrome metabólico?")

st.write(
    "De acuerdo con el consenso internacional armonizado (Alberti et al., 2009), "
    "el síndrome metabólico se define por la presencia de **3 de los siguientes 5 criterios**:"
)

st.markdown(
    """
- Circunferencia de cintura elevada (dependiente de población)
- Triglicéridos ≥150 mg/dL o tratamiento
- HDL bajo (<40 mg/dL en hombres, <50 mg/dL en mujeres) o tratamiento
- Presión arterial ≥130/85 mmHg o tratamiento
- Glucosa en ayuno ≥100 mg/dL o tratamiento
"""
)

st.caption(
    "Esta calculadora no diagnostica síndrome metabólico. "
    "Solo orienta con base en marcadores indirectos."
)

# =========================
# REFERENCIAS
# =========================
st.markdown("---")
st.header("Referencias")

st.markdown(
    """
1. Son DH et al. *Nutrition, Metabolism and Cardiovascular Diseases*. 2022.  
2. D’Elia L et al. *Minerva Medica*. 2024.  
3. Wan H et al. *Scientific Reports*. 2024.  
4. Seo MW et al. *Obesity Research & Clinical Practice*. 2023.  
5. Hosseinkhani S et al. *Endocrine, Metabolic & Immune Disorders Drug Targets*. 2024.  
6. Alberti KGMM et al. *Circulation*. 2009.
"""
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(f"**Creado por {AUTHOR}**")
st.markdown(f"**Última actualización:** {LAST_UPDATED}")
st.caption("Herramienta educativa basada en evidencia científica. No sustituye la valoración médica.")
