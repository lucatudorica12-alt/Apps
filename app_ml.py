import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ==========================================
# 1. PREGĂTIREA DATELOR (Faza de Data Science)
# ==========================================
# Generăm un set de date "istoric" (100 de apartamente fictive)
# Fixăm "seed-ul" ca datele aleatorii să fie aceleași la fiecare rulare
np.random.seed(42) 

suprafata = np.random.randint(40, 150, 100) # între 40 și 150 mp
camere = np.random.randint(1, 5, 100)       # între 1 și 4 camere
an_constructie = np.random.randint(1980, 2024, 100)

# Creăm formula logică a prețului + adăugăm puțin zgomot aleatoriu (ca în viața reală)
pret_baza = (suprafata * 1200) + (camere * 5000) + ((an_constructie - 1980) * 800)
zgomot = np.random.randint(-10000, 10000, 100)
preturi = pret_baza + zgomot

# Creăm tabelul (DataFrame-ul) care conține datele noastre
date_apartamente = pd.DataFrame({
    'Suprafata (mp)': suprafata,
    'Numar Camere': camere,
    'An Constructie': an_constructie,
    'Pret (EUR)': preturi
})

# ==========================================
# 2. ANTRENAREA MODELULUI (Faza de Machine Learning)
# ==========================================
# Definim datele din care învățăm (X) și ce vrem să prezicem (y)
X = date_apartamente[['Suprafata (mp)', 'Numar Camere', 'An Constructie']]
y = date_apartamente['Pret (EUR)']

# Creăm algoritmul de Regresie Liniară și îl "antrenăm" pe datele noastre
model = LinearRegression()
model.fit(X, y) # Funcția .fit() este momentul în care AI-ul învață!

# ==========================================
# 3. INTERFAȚA APLICAȚIEI (Faza de Frontend)
# ==========================================
st.title("🏡 Predictor Imobiliar cu Machine Learning")
st.write("Această aplicație învață din date istorice pentru a estima prețul unui apartament, rulând 100% local!")

# Afișăm câteva rânduri din tabel pentru ca profesorii să vadă din ce învață modelul
st.subheader("Date istorice folosite pentru antrenament:")
st.dataframe(date_apartamente.head())

st.divider()

st.subheader("Introdu datele apartamentului dorit:")

# Creăm slidere (glisoare) pentru a lua date de la utilizator
input_suprafata = st.slider("Suprafața (mp):", min_value=30, max_value=200, value=65)
input_camere = st.slider("Număr camere:", min_value=1, max_value=5, value=2)
input_an = st.slider("Anul construcției:", min_value=1970, max_value=2024, value=2010)

# ==========================================
# 4. PREDICȚIA (Acțiunea)
# ==========================================
if st.button("Estimează Prețul", type="primary"):
    # Împachetăm datele utilizatorului exact în formatul cerut de model
    date_noi = pd.DataFrame({
        'Suprafata (mp)': [input_suprafata],
        'Numar Camere': [input_camere],
        'An Constructie': [input_an]
    })
    
    # Cerem modelului antrenat să facă predicția
    pret_estimat = model.predict(date_noi)[0]
    
    # Afișăm rezultatul
    st.success(f"Prețul estimat al apartamentului este de aproximativ: **{pret_estimat:,.0f} EUR**")