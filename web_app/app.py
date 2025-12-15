

import streamlit as st
import pandas as pd
from database import init_db, get_last_detections, get_stats
from mqtt_client import send_command
import time

st.set_page_config(page_title="TN Currency Detection", layout="wide")

# Initialisation de la base
init_db()

# CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header">
    <h1>💰 TN Currency Detection</h1>
    <p>Dashboard IoT & IA – MP2L</p>
</div>
""", unsafe_allow_html=True)

# DONNÉES
rows = get_last_detections(50)
df = pd.DataFrame(
    rows,
    columns=["Monnaie", "Confiance", "Image", "Date"]
)

stats = get_stats()
df_stats = pd.DataFrame(stats, columns=["Monnaie", "Nombre"])

# KPI
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"<div class='card'><h3>📸 Total</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

with c2:
    last = df.iloc[0]["Monnaie"] if not df.empty else "—"
    st.markdown(f"<div class='card'><h3>💰 Dernière</h3><h2>{last}</h2></div>", unsafe_allow_html=True)

with c3:
    conf = round(df["Confiance"].max(), 2) if not df.empty else 0
    st.markdown(f"<div class='card'><h3>🎯 Confiance max</h3><h2>{conf}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# TABLE
st.subheader("📋 Dernières détections")
st.dataframe(df, use_container_width=True)

# GRAPH
st.subheader("📊 Statistiques")
st.bar_chart(df_stats.set_index("Monnaie"))

# ACTIONS
st.markdown("---")
st.subheader("🎮 Actions sur l’objet connecté")

b1, b2, b3 = st.columns(3)

with b1:
    if st.button("🔓 Ouvrir porte"):
        send_command("open_door")
        st.success("Commande envoyée")

with b2:
    if st.button("🔒 Fermer porte"):
        send_command("close_door")
        st.success("Commande envoyée")

with b3:
    if st.button("🚨 Alerte"):
        send_command("alert")
        st.success("Alerte envoyée")

# ===============================
# AUTO REFRESH toutes les 5 secondes
# ===============================
if 'last_rerun' not in st.session_state:
    st.session_state.last_rerun = time.time()

if time.time() - st.session_state.last_rerun > 5:
    st.session_state.last_rerun = time.time()
    st.experimental_rerun()

# EXPORT CSV
st.markdown("### 📤 Export des données")
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Télécharger CSV",
    data=csv,
    file_name="detections.csv",
    mime="text/csv"
)
