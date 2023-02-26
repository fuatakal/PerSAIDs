import time
import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="FMF Predictor", page_icon=":hospital:", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>I am here to facilitate Familial Mediterranean Fever (FMF) diagnosis using machine learning.</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Please fill the form below and click the predict button to see how likely your patient has FMF.</h2>", unsafe_allow_html=True)

st.markdown("<br/><hr>", unsafe_allow_html=True)

_, c1, c2, _ = st.columns([1, 1, 1, 1])
input_df = []
with c1:
    Age_at_disease_Onset = st.number_input("Age at disease Onset", min_value=0.0, max_value=70.0, help="in years")
    Age_at_diagnosis = st.number_input("Age at diagnosis", min_value=0.0, max_value=70.0, help="in years")
    Headache = st.radio("Headache", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")
    Abdominal_pain = st.radio("Abdominal pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")
    Chest_pain = st.radio("Chest pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")

with c2:
    Age_at_last_visit = st.number_input("Age at last visit", min_value=0.0, max_value=70.0, help="in years")
    Disease_duration = st.number_input("Disease duration", min_value=0.0, max_value=70.0, help="in years")
    Gender = st.radio("Gender", ('Male', 'Female'), horizontal =True)
    Ethincity = st.radio("Ethnic group:", ('Arab', 'Jewish', 'Caucasian', 'Other'), horizontal =True)
    Arthralgia = st.radio("Joint pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")



# Create a three-column form layout
_, c3, c4, _ = st.columns([1, 1, 1, 1])

with c3:

    MucoCu = st.radio("Mucocutaneous manifestations? ", ('Yes', 'No'), horizontal =True)
    Cardio = st.radio("Cardiologic manifestations? ", ('Yes', 'No'), horizontal =True)
    Gastr = st.radio("Gastrointestinal manifestations? ", ('Yes', 'No'), horizontal =True)
    Drug = st.radio("Using therapy? ", ('Yes', 'No'), horizontal =True)
    Genito = st.radio("Genitourinary manifestations? ", ('Yes', 'No'), horizontal =True)

with c4:
    Neuro = st.radio("Neurologic manifestations? ", ('Yes', 'No'), horizontal =True)
    Musc = st.radio("Muscoloskeletal manifestations? ", ('Yes', 'No'), horizontal =True)
    Ocul = st.radio("Ocular manifestations? ", ('Yes', 'No'), horizontal =True)
    Const = st.radio("Costitutional manifestations? ", ('Yes', 'No'), horizontal =True)
    Infect = st.radio("Infection is identified as trigger? ", ('Yes', 'No'), horizontal =True)

def user_input_features():
    Gender_var = (1 if Gender == 'Female' else 0)
    MucoCu_var = (1 if MucoCu == 'Yes' else 0)
    Cardio_var = (1 if Cardio == 'Yes' else 0)
    Gastr_var = (1 if Gastr == 'Yes' else 0)
    Neuro_var = (1 if Neuro == 'Yes' else 0)
    Musc_var = (1 if Musc == 'Yes' else 0)
    Ocul_var = (1 if Ocul == 'Yes' else 0)
    Const_var = (1 if Const == 'Yes' else 0)
    Drug_var = (1 if Drug == 'Yes' else 0)
    Genito_var = (1 if Genito == 'Yes' else 0)
    Infect_var = (1 if Infect == 'Yes' else 0)
    # Ethincity
    if Ethincity == 'Arab':
        Arab = 1
        Jewish = 0
        Caucasian = 0
    elif Ethincity == 'Jewish':
        Arab = 0
        Jewish = 1
        Caucasian = 0
    elif Ethincity == 'Caucasian':
        Arab = 0
        Jewish = 0
        Caucasian = 1
    else:
        Arab = 0
        Jewish = 0
        Caucasian = 0

    # Headache
    if Headache == 'Sometimes or often':
        Head_1 = 1
        Head_2 = 0
    elif Headache == 'Always':
        Head_1 = 0
        Head_2 = 1
    else:
        Head_1 = 0
        Head_2 = 0

    # Abdominal pain
    if Abdominal_pain == 'Sometimes or often':
        Abd_1 = 1
        Abd_2 = 0
    elif Abdominal_pain == 'Always':
        Abd_1 = 0
        Abd_2 = 1
    else:
        Abd_1 = 0
        Abd_2 = 0

    # Chest pain
    if Chest_pain == 'Sometimes or often':
        Chest_1 = 1
        Chest_2 = 0
    elif Chest_pain == 'Always':
        Chest_1 = 0
        Chest_2 = 1
    else:
        Chest_1 = 0
        Chest_2 = 0

    # Arthralgia
    if Arthralgia == 'Sometimes or often':
        Arth_1 = 1
        Arth_2 = 0
    elif Arthralgia == 'Always':
        Arth_1 = 0
        Arth_2 = 1
    else:
        Arth_1 = 0
        Arth_2 = 0

    data = {
            'A_MucoCu': MucoCu_var,
            'F_Cardio': Cardio_var,
            'Chest pain_1.0': Chest_1,
            'D_Gastr': Gastr_var,
            'Ethincity_Jewish': Jewish,
            'G_Neuro': Neuro_var,
            'B_Musc': Musc_var,
            'Headache (anytime)_2.0': Head_2,
            'C_Ocul': Ocul_var,
            'Arthralgia_1.0': Arth_2,
            'Ethincity_Caucasian': Caucasian,
            'Age at last visit': Age_at_last_visit,
            'Arthralgia_2.0': Arth_2,
            'Age at disease Onset': Age_at_disease_Onset,
            'Gender': Gender_var,
            'I_Const': Const_var,
            'Ethincity_Arab': Arab,
            'Abdominal pain_1.0': Abd_1,
            'Disease duration': Disease_duration,
            'R_Drug': Drug_var,
            'Abdominal pain_2.0': Abd_2,
            'H_Genito': Genito_var,
            'Age at diagnosis': Age_at_diagnosis,
            'Infect': Infect_var,
            'Headache (anytime)_1.0': Head_1}
    features = pd.DataFrame(data, index=[0])
    return features


def clear_input_fields(input_data):
    for field in input_fields:
        input_data[field] = ''


st.markdown("<hr>", unsafe_allow_html=True)

left_button, right_button, _ = st.columns([1,1,6])
predicted = False
cleared = False

with left_button:
    if st.button("Predict"):
        st.spinner()
        input_df = user_input_features()
        model = pickle.load(open('/app/masterstudies/Streamlit_app/model.pkl', 'rb'))
        scaler = pickle.load(open('/app/masterstudies/Streamlit_app/scaler.pkl', 'rb'))
        scaled_input_df = scaler.transform(input_df)
        prediction = model.predict(scaled_input_df)
        prediction_proba = model.predict_proba(scaled_input_df)

        probas = [x * 100 for x in prediction_proba]
        predicted = True

with right_button:
    if st.button("Clear"):
        cleared = True

if predicted:

    st.markdown("<br/>", unsafe_allow_html=True)

    probabilityOfFMF = round(probas[0][1], 2)
    if probabilityOfFMF < 50:
        st.info('It is **unlikely** that your patient has FMF. Because, my calculations show **{}%** probability.'.format(str(probabilityOfFMF)))
    elif probabilityOfFMF <= 75 and probabilityOfFMF >= 50:
        st.warning('Sorry, I must stay neutral. Your patient may or may not have FMF. Because, my calculations show **{}%** probability for FMF.'.format(str(probabilityOfFMF)))
    elif probabilityOfFMF <= 90 and probabilityOfFMF > 75:
        st.success('It is **likely** that your patient may have FMF. Because, my calculations show **{}%** probability.'.format(str(probabilityOfFMF)))
    else:
        st.success('It is **very likely** that your patient has FMF. Because, my calculations show **{}%** probability.'.format(str(probabilityOfFMF)))

    st.error('By the way, do not forget that I am just a prototype! Don\'t take my word for it.')

if cleared =='True':
    st.experimental_rerun()
