import streamlit as st
import pandas as pd

@st.cache_data
def read_data():
    modellen = pd.read_excel('data_kopie.xlsx', sheet_name = 'modellen')
    return modellen

# Function to get color based on the scale
def get_color(value):
    # Customize the color scale as needed
    if value == 'A':
        return 'green'
    elif value == 'B':
        return 'light green'
    elif value == 'C':
        return 'yellow'
    elif value == 'D':
        return 'orange'
    elif value == 'E':
        return 'red'
    else:
        return 'yellow'

def get_label(type_huis, orientatie, perc_glas, zonwering, soort_glas, isolatie, modellen):
    g_waarde_glas = 0.6 if soort_glas == "enkel, dubbel, HR+ of HR++ glas" else 0.3

    try: 
        beste_model, label,NDH,TaMax, ATGAB = modellen.loc[(
            (modellen['Woningtype'] == type_huis) &
            (modellen['Oriëntatie'] == orientatie) &
            (modellen['Glaspercentage'] == perc_glas) & 
            (modellen['Zonwering'] == zonwering) &
            (modellen['g-waarde glas'] == g_waarde_glas) & 
            (modellen['Isolatie/infiltratie'] == isolatie)
            ),['Model met beste score','Label','NDH','TaMax','ATGAB']].iloc[0]
    except IndexError:
        label = 'Geen label berekend, wijzig glassoort'
    return label

# Streamlit app
def main():

    modellen = read_data()
    
    st.title("Hittelabel App")

    c1, c2 = st.columns(2)

    with c1:

        # Input fields and dropdowns for the first column
        
        st.header("Bereken het hittelabel van uw woning")
        type_huis = st.selectbox("Type huis", ['Tussenappartement enkelzijdig', 'Tussenappartement doorzon', 'Hoekwoning','Tussenwoning','Appartement onder dak enkelzijdig', 'Appartement onder dak doorzon'], index = 5)
        orientatie = st.selectbox("Orientatie", ['Noord','Oost' ,'Zuid', 'West'], index = 0)
        perc_glas = st.selectbox("% glas", [0.3, 0.5 ,0.7], index = 1)
        zonwering = st.selectbox("Zonwering", ['Binnen slecht', 'Binnen goed', 'Buiten','Overstek','Buiten & overstek','Binnen slecht & overstek', 'Binnen goed & overstek'], index = 2)
        soort_glas = st.selectbox("Soort glas", ['zonwerend of triple glas', 'enkel, dubbel, HR+ of HR++ glas'], index = 1)
        isolatie = st.selectbox("Isolatie", ['Goed','Matig','Slecht'], index = 1)

        # Perform calculation and display results for column 1
        label = get_label(type_huis, orientatie, perc_glas, zonwering, soort_glas, isolatie, modellen)

        st.markdown(f"Uw woning heeft hittelabel:")
        color = get_color(label)
        st.markdown(f'<div style="background-color:{color}; padding: 10px;"><b>{label}</b></div>', unsafe_allow_html=True)

    
    with c2:
 
        # Input fields and dropdowns for the first column
        st.header("Vergelijk met een andere woning")
        type_huis2 = st.selectbox("Type huis", ['Tussenappartement enkelzijdig', 'Tussenappartement doorzon', 'Hoekwoning','Tussenwoning','Appartement onder dak enkelzijdig', 'Appartement onder dak doorzon'], index = 4, key = 'typehuis2')
        orientatie2 = st.selectbox("Orientatie", ['Noord','Oost' ,'Zuid', 'West'], index = 0, key = 'orientatie2')
        perc_glas2 = st.selectbox("% glas", [0.3, 0.5 ,0.7], index = 1, key = 'perc_glas2')
        zonwering2 = st.selectbox("Zonwering", ['Binnen slecht', 'Binnen goed', 'Buiten','Overstek','Buiten & overstek','Binnen slecht & overstek', 'Binnen goed & overstek'], index = 3, key = 'zonwering2')
        soort_glas2 = st.selectbox("Soort glas", ['zonwerend of triple glas', 'enkel, dubbel, HR+ of HR++ glas'], index = 0, key = 'soort_glas2')
        isolatie2 = st.selectbox("Isolatie", ['Goed','Matig','Slecht'], index = 0, key = 'isolatie2')

        # Perform calculation and display results for column 1
        label2 = get_label(type_huis2, orientatie2, perc_glas2, zonwering2, soort_glas2, isolatie2, modellen)

        st.markdown(f"Bovenstaande woning heeft hittelabel")
        color = get_color(label2)
        st.markdown(f'<div style="background-color:{color}; padding: 10px;"><b>{label2}</b></div>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()
