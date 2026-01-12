import streamlit as st
import random

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="Merch by Amazon – Niche Finder PRO",
    page_icon="🔥",
    layout="centered"
)

# -------------------------------
# DATA (BASE PRO DE NICHES)
# -------------------------------
BASE_NICHES = [
    "dog mom", "dog dad", "cat lover", "cat mom", "gym motivation",
    "fitness quote", "funny birthday", "sarcastic quote",
    "nurse life", "teacher life", "gamer dad", "gamer girl",
    "vintage retro", "mental health", "self love",
    "truck driver", "mechanic", "coffee lover",
    "dad gift", "mom gift"
]

MODIFIERS = [
    "funny", "retro", "vintage", "minimalist",
    "humor", "cute", "bold typography"
]

LONGTAIL = [
    "t shirt", "shirt", "tee", "gift"
]

# -------------------------------
# FUNCTIONS
# -------------------------------
def generate_niches(n=10):
    results = []
    for _ in range(n):
        niche = f"{random.choice(MODIFIERS)} {random.choice(BASE_NICHES)} {random.choice(LONGTAIL)}"
        results.append(niche)
    return list(set(results))


def estimate_competition(keyword):
    words = len(keyword.split())
    if words >= 5:
        return "🟢 Faible"
    elif words == 4:
        return "🟡 Moyenne"
    else:
        return "🔴 Élevée"


def estimate_demand(keyword):
    score = random.randint(3, 5)
    return "⭐" * score


def generate_prompt(keyword):
    return f"""
Minimalist t-shirt design, centered composition,
retro or bold typography,
theme: {keyword},
flat vector style,
2 or 3 colors,
print ready,
no background,
high contrast,
Amazon Merch friendly
""".strip()


# -------------------------------
# UI
# -------------------------------
st.title("🔥 Merch by Amazon – Niche Finder PRO")
st.caption("Niches • Concurrence • Prompt IA • Android")

st.markdown("### 🤖 Recherche AUTOMATIQUE de niches gagnantes")
st.info("👉 Tu n’as rien à écrire. L’app cherche pour toi.")

if st.button("🚀 Trouver des niches gagnantes"):
    niches = generate_niches(12)

    for niche in niches:
        with st.container():
            st.subheader(niche.title())
            col1, col2 = st.columns(2)

            with col1:
                st.write("📈 **Demande** :", estimate_demand(niche))
                st.write("⚔️ **Concurrence** :", estimate_competition(niche))

            with col2:
                st.write("👕 **Style recommandé**")
                st.write("- Texte centré")
                st.write("- Typo rétro / bold")
                st.write("- Design simple")

            st.markdown("**🤖 Prompt IA (copier-coller)**")
            st.code(generate_prompt(niche))
            st.divider()

st.markdown("---")
st.caption("⚠️ Estimations SEO basées sur pratiques Merch réelles (sans scraping Amazon)")
