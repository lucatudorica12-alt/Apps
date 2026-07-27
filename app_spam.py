import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ==========================================
# 1. PREGĂTIREA DATELOR (Istoricul)
# ==========================================
# Creăm o listă de mesaje fictive pe care AI-ul le va folosi ca să învețe
date_mesaje = {
    'Text': [
        'Castiga acum un iPhone gratuit! Click pe link',
        'Salut, ne vedem maine la ora 10 pentru sedinta?',
        'Ai fost selectat pentru un premiu de 5000 de euro. Suna urgent',
        'Te rog sa imi trimiti documentele pentru contabilitate.',
        'Reduceri masive! Cumpara acum pastile de slabit la jumatate de pret',
        'La multi ani! Sa ai o zi superba alaturi de cei dragi.',
        'Imprumut rapid fara garantii. Doar cu buletinul. Aplica acum!',
        'Nu uita sa iei paine cand te intorci de la munca.'
    ],
    'Eticheta': [
        'Spam', 
        'Sigur', 
        'Spam', 
        'Sigur', 
        'Spam', 
        'Sigur', 
        'Spam', 
        'Sigur'
    ]
}

df_mesaje = pd.DataFrame(date_mesaje)

# ==========================================
# 2. ANTRENAREA MODELULUI (AI-ul local)
# ==========================================
# Transformăm cuvintele în numere (pentru că matematica nu înțelege litere)
vectorizator = CountVectorizer()
X = vectorizator.fit_transform(df_mesaje['Text'])
y = df_mesaje['Eticheta']

# Folosim algoritmul "Naive Bayes" - este standardul de aur pentru filtrarea de Spam
model = MultinomialNB()
model.fit(X, y)

# ==========================================
# 3. INTERFAȚA GRAFICĂ (Streamlit)
# ==========================================
st.title("🛡️ Filtru Anti-Spam Inteligent")
st.write("Acest model de Machine Learning învață local să recunoască mesajele nesolicitate.")

# Afișăm baza de date din care a învățat
with st.expander("Vezi baza de date de antrenament"):
    st.table(df_mesaje)

st.divider()

# Căsuța unde tu testezi un mesaj nou
mesaj_nou = st.text_area("Scrie un mesaj / email pentru a fi analizat:", height=100)

if st.button("Verifică Mesajul", type="primary"):
    
    if mesaj_nou:
        # 1. Traducem mesajul tău nou în limbaj matematic (folosind același vocabular)
        mesaj_vectorizat = vectorizator.transform([mesaj_nou])
        
        # 2. Cerem modelului să pună eticheta
        predictie = model.predict(mesaj_vectorizat)[0]
        
        # 3. Afișăm rezultatul frumos pe ecran
        if predictie == 'Spam':
            st.error("🚨 **ATENȚIE!** Acest mesaj a fost clasificat drept SPAM.")
        else:
            st.success("✅ **SIGUR!** Acest mesaj pare a fi legitim.")
    else:
        st.warning("Te rog să scrii un mesaj în căsuță.")