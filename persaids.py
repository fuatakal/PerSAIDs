import time
import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="FMF Predictor", page_icon=":hospital:", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>Familial Mediterranean Fever (FMF) Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Please fill the form below and click the predict button to see <br/>how likely your patient has FMF</h2>", unsafe_allow_html=True)

st.markdown("<br/><hr>", unsafe_allow_html=True)

input_df = []


# Create a three-column form layout
_, c3, c4, c5, _ = st.columns([1.25, 1, 1, 1, 1.25])

with c3:
    Age_at_disease_Onset = st.number_input("Age at disease Onset", min_value=0.0, max_value=18.0, help="in years")
    Number_episodes = st.number_input("Number of episodes/year", min_value=0, max_value=30, help="in years")

with c4:
    Age_at_diagnosis = st.number_input("Age at diagnosis", min_value=0.0, max_value=18.0, help="in years")
    Duration_episodes = st.number_input("Duration of episodes (days)", min_value=0.0, max_value=18.0, help="in years")

with c5:
    Age_at_last_visit = st.number_input("Age at last visit", min_value=0.0, max_value=18.0, help="in years")
    Ethincity = st.radio("Ethnic group:", ('Arab', 'Jewish', 'Caucasian', 'Other'), horizontal =True)



# Create a three-column form layout
_, c6, c7, c8, _ = st.columns([1.25, 1, 1, 1, 1.25])

with c6:
    Drug = st.radio("Using therapy? ", ('Yes', 'No'), horizontal =True)
    Cardio = st.radio("Cardiologic manifestations? ", ('Yes', 'No'), horizontal =True)
    Gastr = st.radio("Gastrointestinal manifestations? ", ('Yes', 'No'), horizontal =True)
    Headache = st.radio("Headache", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")
    Abdominal_pain = st.radio("Abdominal pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")

with c7:
    Gender = st.radio("Gender", ('Male', 'Female'), horizontal =True)
    MucoCu = st.radio("Mucocutaneous manifestations? ", ('Yes', 'No'), horizontal =True)
    Infect = st.radio("Infection is identified as trigger? ", ('Yes', 'No'), horizontal =True)
    Arthralgia = st.radio("Joint pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")
    Ocul = st.radio("Ocular manifestations? ", ('Yes', 'No'), horizontal =True)

with c8:
    Genito = st.radio("Genitourinary manifestations? ", ('Yes', 'No'), horizontal =True)
    Const = st.radio("Costitutional manifestations? ", ('Yes', 'No'), horizontal =True)
    Neuro = st.radio("Neurologic manifestations? ", ('Yes', 'No'), horizontal =True)
    Chest_pain = st.radio("Chest pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")
    Musc = st.radio("Muscoloskeletal manifestations? ", ('Yes', 'No'), horizontal =True)

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
            'Gender': Gender_var,
            'Age at disease Onset': Age_at_disease_Onset,
            'Age at last visit': Age_at_last_visit,
            'Age at diagnosis': Age_at_diagnosis,
            'Number of episodes/year': Number_episodes,
            'duration of episodes (days)': Duration_episodes,
            'Infect': Infect_var,
            'A_MucoCu': MucoCu_var,
            'B_Musc': Musc_var,
            'C_Ocul': Ocul_var,
            'D_Gastr': Gastr_var,
            'F_Cardio': Cardio_var,
            'G_Neuro': Neuro_var,
            'H_Genito': Genito_var,
            'I_Const': Const_var,
            'R_Drug': Drug_var,
            'Ethnicity_Arab': Arab,
            'Ethnicity_Caucasian': Caucasian,
            'Ethnicity_Jewish': Jewish,
            'Arthralgia_1.0': Arth_1,
            'Arthralgia_2.0': Arth_2,
            'Abdominal pain_1.0': Abd_1,
            'Abdominal pain_2.0': Abd_2,
            'Chest pain_1.0': Chest_1,
            'Chest pain_2.0': Chest_2,
            'Headache (anytime)_1.0': Head_1,
            'Headache (anytime)_2.0': Head_2}
    features = pd.DataFrame(data, index=[0])

    return features






st.markdown("<hr>", unsafe_allow_html=True)

_, left_button, right_button, _ = st.columns([6,1,1,6])
predicted = False
cleared = False

with left_button:
    if st.button("Predict"):
        st.spinner()

        # Check if at least one feature (other than ethnicity) has been provided
        if (Age_at_disease_Onset == 0 and Number_episodes == 0 and
            Age_at_diagnosis == 0 and Age_at_last_visit == 0 and
            Duration_episodes == 0 and Headache == 'Never' and
            MucoCu == 'No' and Cardio == 'No' and Gastr == 'No' and
            Ocul == 'No' and Gender == 'Male' and Arthralgia == 'Never' and
            Abdominal_pain == 'Never' and Drug == 'No' and Infect == 'No' and
            Chest_pain == 'Never' and Genito == 'No' and Const == 'No' and
            Neuro == 'No' and Musc == 'No'):
            st.warning("You cannot make a prediction based on ethnicity alone.")
        else:
            input_df = user_input_features()
            model = pickle.load(open('model.pkl', 'rb'))
            scaler = pickle.load(open('scaler.pkl', 'rb'))
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
        st.info('It is **unlikely** that the patient has FMF. Because, my calculations show **{}%** probability.'.format(str(probabilityOfFMF)))
    else:
        st.success('It is **likely** that the patient may have FMF. Because, my calculations show **{}%** probability.'.format(str(probabilityOfFMF)))


    st.error('By the way, do not forget that I am just a prototype! Don\'t take my word for it.')

if cleared =='True':
    st.experimental_rerun()
