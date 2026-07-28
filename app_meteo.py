import streamlit as st
import requests

# ==========================================
# INTERFAȚA GRAFICĂ (Streamlit)
# ==========================================
st.title("🌤️ Asistent Meteo Inteligent")
st.write("Află vremea în timp real și primește recomandări de vestimentație, folosind un API gratuit!")

st.divider()

# Căsuța pentru oraș
oras = st.text_input("Introdu numele orașului (ex: Bucuresti, Londra, Tokyo, Paris):")

if st.button("Verifică Vremea", type="primary"):
    
    # 1. BAZA PYTHON: Verificăm dacă utilizatorul a scris ceva în căsuță
    if oras:
        
        # 2. GESTIONAREA ERORILOR: Blocul Try/Except
        try:
            # 3. API-UL (Chelnerul 1): Căutăm coordonatele geografice (Latitudine / Longitudine) ale orașului
            url_locatie = f"https://geocoding-api.open-meteo.com/v1/search?name={oras}&count=1&language=ro&format=json"
            raspuns_locatie = requests.get(url_locatie).json()
            
            # Dacă orașul a fost găsit în baza de date
            if "results" in raspuns_locatie:
                lat = raspuns_locatie["results"][0]["latitude"]
                lon = raspuns_locatie["results"][0]["longitude"]
                nume_oras = raspuns_locatie["results"][0]["name"]
                tara = raspuns_locatie["results"][0]["country"]
                
                # 4. API-UL (Chelnerul 2): Cerem vremea exactă pentru acele coordonate
                url_vreme = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                raspuns_vreme = requests.get(url_vreme).json()
                
                # Extragem temperatura din cutia de memorie (variabila) trimisă de API
                temperatura = raspuns_vreme["current_weather"]["temperature"]
                viteza_vant = raspuns_vreme["current_weather"]["windspeed"]
                
                # Afișăm datele frumos pe ecran
                st.success(f"📍 Vremea în **{nume_oras}**, {tara}")
                
                col1, col2 = st.columns(2)
                col1.metric(label="Temperatura Actuală", value=f"{temperatura} °C")
                col2.metric(label="Viteza Vântului", value=f"{viteza_vant} km/h")
                
                st.divider()
                
                # 5. LOGICA PYTHON (If / Else): Inteligența aplicației
                st.subheader("👕 Recomandarea Asistentului:")
                
                if temperatura < 0:
                    st.info("❄️ Este îngheț! Ia-ți o geacă foarte groasă, fular, mănuși și o căciulă.")
                elif 0 <= temperatura <= 10:
                    st.info("🥶 Este destul de frig. O geacă de toamnă/iarnă și un pulover sunt necesare.")
                elif 11 <= temperatura <= 20:
                    st.info("🌤️ Vreme plăcută, răcoroasă. Un hanorac sau o jachetă subțire sunt perfecte.")
                elif 21 <= temperatura <= 30:
                    st.info("☀️ Este cald! Un tricou și pantaloni subțiri sunt ideali.")
                else:
                    st.info("🔥 Este caniculă! Îmbracă-te cât mai lejer, bea multă apă și poartă ochelari de soare.")
                    
            else:
                # Erori prinse cu eleganță (fără ecran roșu general)
                st.error("❌ Nu am putut găsi acest oraș. Te rog să verifici cum ai scris numele.")
                
        except Exception as e:
            # Dacă pică internetul sau serverul Meteo este închis
            st.error("🚨 A apărut o eroare tehnică la conectarea cu API-ul Meteo.")
            
    else:
        st.warning("⚠️ Te rog să scrii un nume de oraș mai întâi.")