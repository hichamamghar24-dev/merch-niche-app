import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import requests
from PIL import Image
import numpy as np
import urllib.parse
from openai import OpenAI
import base64

# ================== CONFIG ==================
st.set_page_config(
    page_title="Merch Niche Finder PRO",
    layout="wide"
)

# ================== STYLE ==================
st.markdown("""
<style>
body { background-color: #0e1117; }
h1, h2, h3 { color: #00ffcc; }
.stButton>button {
    background-color: #00ffcc;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.title("🔥 Merch by Amazon – Niche Finder PRO")
st.write("Niches • Concurrence • Prompt IA • DALL·E • Android")

# ================== INPUT ==================
st.subheader("🧠 Recherche de niches")

keywords_text = st.text_area(
    "Entre les niches (1 par ligne)",
    "dog mom shirt\ncat lover shirt\ngym motivation shirt"
)

SERPAPI_KEY = st.text_input(
    "🔑 Clé SerpApi (Amazon concurrence)",
    type="password"
)

OPENAI_API_KEY = st.text_input(
    "🔑 Clé OpenAI (DALL·E)",
    type="password"
)

# ================== ANALYSE NICHES ==================
if st.button("🔍 Analyser les niches"):
    niches = [n.strip() for n in keywords_text.split("\n") if n.strip()]

    if not niches or not SERPAPI_KEY:
        st.error("Ajoute niches + clé SerpApi")
        st.stop()

    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(niches, timeframe="today 12-m")
    trends = pytrends.interest_over_time()

    results = []

    for n in niches:
        avg_trend = round(trends[n].mean(), 2)
        peak = trends[n].max()

        params = {
            "engine": "amazon",
            "k": n,
            "api_key": SERPAPI_KEY
        }
        data = requests.get("https://serpapi.com/search", params=params).json()
        competition = data.get("search_information", {}).get("total_results", 0)

        score = round((avg_trend * 0.6) - (competition * 0.0001), 2)

        results.append({
            "Niche": n,
            "Trend": avg_trend,
            "Concurrence": competition,
            "Score": score
        })

    df = pd.DataFrame(results).sort_values("Score", ascending=False)
    st.dataframe(df, use_container_width=True)

    st.session_state["best_niche"] = df.iloc[0]["Niche"]

# ================== IMAGE UPLOAD ==================
st.divider()
st.subheader("🖼️ Analyse design (upload)")

uploaded_image = st.file_uploader(
    "Upload image design",
    type=["png", "jpg", "jpeg"]
)

image_style = "N/A"
dominant_colors = "N/A"

if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, width=250)

    arr = np.array(img.resize((100, 100)))
    dominant_colors = f"RGB {arr.mean(axis=(0,1)).astype(int)}"
    image_style = "Illustration" if arr.std() > 50 else "Minimal"

    st.write("Style :", image_style)
    st.write("Couleurs :", dominant_colors)

# ================== PROMPT IA ==================
st.divider()
st.subheader("✨ Générateur de prompt IA")

style_choice = st.selectbox(
    "Style",
    ["Texte", "Illustration", "Vintage", "Minimal", "Cartoon"]
)

tone_choice = st.selectbox(
    "Ton",
    ["Humoristique", "Motivant", "Inspirant"]
)

if st.button("🧠 Générer le prompt"):
    niche = st.session_state.get("best_niche", "t-shirt niche")

    prompt = f"""
T-shirt design for niche "{niche}",
style {style_choice},
tone {tone_choice},
visual style {image_style},
colors {dominant_colors},
vector illustration,
bold typography,
centered,
print ready,
transparent background,
no trademark,
merch by amazon compliant
""".strip()

    st.text_area("📋 Prompt IA", prompt, height=220)

    ideogram = urllib.parse.quote(prompt)
    st.markdown(f"[🎨 Ouvrir Ideogram](https://ideogram.ai/?prompt={ideogram})")

# ================== DALL·E ==================
if OPENAI_API_KEY and st.button("🎨 Générer image avec DALL·E"):
    client = OpenAI(api_key=OPENAI_API_KEY)

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    img_bytes = base64.b64decode(result.data[0].b64_json)

    st.image(img_bytes, use_column_width=True)
    st.download_button(
        "📥 Télécharger PNG",
        img_bytes,
        "design_dalle.png",
        "image/png"
    )

# ================== MOCKUP ==================
st.divider()
st.subheader("👕 Mockup réaliste")

st.markdown("""
👉 Télécharge le design  
👉 Ouvre un générateur de mockup  
""")

st.markdown("[👕 Placeit](https://placeit.net)")
st.markdown("[👕 Printify Mockup](https://www.printify.com/mockup-generator/)")
import streamlit as st
from PIL import Image
import openai
import io

st.markdown("---")
st.header("👕 Analyse d’image de T-shirt (Mode PRO SEO)")

uploaded_image = st.file_uploader(
    "📤 Téléverse une image de t-shirt (PNG ou JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Image analysée", use_column_width=True)

    st.info("🧠 Analyse IA en cours...")

    try:
        prompt = """
Tu es un expert SEO Merch by Amazon.
Analyse ce design de t-shirt et fournis :

1. 5 niches possibles
2. 10 mots-clés SEO (anglais, Merch by Amazon)
3. Le type de client (ex: gift, humor, passion, job, hobby)
4. Un prompt DALL·E pour créer un design similaire MAIS ORIGINAL (pas de copie)

Réponds de manière structurée.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un expert Merch by Amazon et SEO."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content

        st.success("✅ Analyse terminée")
        st.markdown(result)

        st.download_button(
            label="📥 Télécharger l’analyse",
            data=result,
            file_name="analyse_tshirt_seo.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error("Erreur IA. Vérifie ta clé OpenAI.")
        st.write(e)
