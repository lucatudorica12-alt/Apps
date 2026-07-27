import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# 1. PREGĂTIREA DATELOR
# ==========================================
# Creăm o mini bază de date cu filme și caracteristicile lor
date_filme = {
    'Titlu': [
        'The Matrix', 'Inception', 'Interstellar', 
        'Titanic', 'The Notebook', 'Pride and Prejudice', 
        'Avengers', 'Iron Man', 'Batman',
        'Toy Story', 'Shrek', 'Finding Nemo'
    ],
    'Etichete': [
        'SF actiune roboti viitor', 
        'SF actiune vise thriller', 
        'SF spatiu timp calatorie',
        'romance drama istoric vapor', 
        'romance drama dragoste lacrimi', 
        'romance drama epoca',
        'actiune supereroi Marvel', 
        'actiune supereroi Marvel tehnologie', 
        'actiune supereroi DC intunecat',
        'animatie comedie familie jucarii', 
        'animatie comedie familie capcaun', 
        'animatie comedie familie pesti ocean'
    ]
}
df_filme = pd.DataFrame(date_filme)

# ==========================================
# 2. ANTRENAREA ALGORITMULUI (Text -> Matematică)
# ==========================================
# Inteligența Artificială nu înțelege cuvinte, ci doar numere.
# CountVectorizer transformă cuvintele din etichete în vectori matematici (0 și 1).
vectorizator = CountVectorizer()
matrice_caracteristici = vectorizator.fit_transform(df_filme['Etichete'])

# cosine_similarity compară toate filmele între ele și le dă un scor de asemănare de la 0 la 1
scoruri_similaritate = cosine_similarity(matrice_caracteristici)

# ==========================================
# 3. INTERFAȚA GRAFICĂ
# ==========================================
st.title("🍿 Sistem Inteligent de Recomandare Filme")
st.write("Alege un film care îți place, iar AI-ul local îți va recomanda altele similare pe baza analizei textului!")

st.divider()

# Creăm un meniu drop-down din care utilizatorul să aleagă filmul
film_ales = st.selectbox("Alege un film:", df_filme['Titlu'])

if st.button("Găsește recomandări", type="primary"):
    
    # 1. Găsim ce număr de ordine (index) are filmul ales în tabelul nostru
    index_film = df_filme[df_filme['Titlu'] == film_ales].index[0]
    
    # 2. Luăm lista de scoruri de similaritate pentru filmul nostru
    scoruri = list(enumerate(scoruri_similaritate[index_film]))
    
    # 3. Sortăm lista descrescător (de la cel mai similar la cel mai puțin similar)
    scoruri_sortate = sorted(scoruri, key=lambda x: x[1], reverse=True)
    
    # 4. Afișăm primele 3 recomandări (sărim peste primul rezultat, care e chiar filmul ales)
    st.subheader(f"Dacă ți-a plăcut '{film_ales}', ți-ar putea plăcea și:")
    
    for i in range(1, 4):
        id_recomandat = scoruri_sortate[i][0]
        titlu_recomandat = df_filme.iloc[id_recomandat]['Titlu']
        scor = scoruri_sortate[i][1] * 100 # Transformăm scorul în procentaj
        
        # Afișăm titlul și procentul de potrivire calculat de AI
        st.write(f"🎬 **{titlu_recomandat}** - Potrivire: {scor:.0f}%")