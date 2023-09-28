import time
import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="FMF Predictor", page_icon=":hospital:", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>Familial Mediterranean Fever (FMF) diagnosis using machine learning.</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Please fill the form below and click the predict button to see how likely your patient has FMF.</h3>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

input_df = []


# Create a three-column form layout
_, c1, c2, c3, _ = st.columns([0.25, 1.5, 1.5, 1.5, 0.25])

with c1:
    Number_episodes = st.number_input("Number of Episodes", min_value=0, max_value=30, help="Write the number of episodes in a year.")
    Chest_pain = st.radio("Chest Pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")
    MucoCu = st.radio("Mucocutaneous Manifestations? ", ('Yes', 'No'), horizontal =True)


with c2:
    Duration_episodes = st.number_input("Duration of Episodes", min_value=0.0, max_value=25.0, help="in days")
    Abdominal_pain = st.radio("Abdominal Pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")
    Cardio = st.radio("Cardiologic Manifestations? ", ('Yes', 'No'), horizontal =True)
    Gastr = st.radio("Gastrointestinal Manifestations? ", ('Yes', 'No'), horizontal =True)

with c3:
    Ethnicity = st.selectbox("Ethnicity:", ('Arab', 'Jewish', 'Caucasian', 'Hispanic', 'Asian', 'Other'), key='ethnicity', help="Select what group decribes the best.")
    Joint = st.radio("Joint Pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the sympotom best.")
    Const = st.radio("Costitutional Manifestations? ", ('Yes', 'No'), horizontal =True)



def user_input_features():
    MucoCu_var = (1 if MucoCu == 'Yes' else 0)
    Cardio_var = (1 if Cardio == 'Yes' else 0)
    Gastr_var = (1 if Gastr == 'Yes' else 0)
    Const_var = (1 if Const == 'Yes' else 0)

    # Ethincity
    if Ethnicity == 'Arab':
        Arab = 1
        Jewish = 0
        Caucasian = 0
        Hispanic = 0
        Asian = 0
        Other = 0
    elif Ethnicity == 'Jewish':
        Arab = 0
        Jewish = 1
        Caucasian = 0
        Hispanic = 0
        Asian = 0
        Other = 0
    elif Ethnicity == 'Caucasian':
        Arab = 0
        Jewish = 0
        Caucasian = 1
        Hispanic = 0
        Asian = 0
        Other = 0
    elif Ethnicity == 'Hispanic':
        Arab = 0
        Jewish = 0
        Caucasian = 0
        Hispanic = 1
        Asian = 0
        Other = 0
    elif Ethnicity == 'Asian':
        Arab = 0
        Jewish = 0
        Caucasian = 0
        Hispanic = 0
        Asian = 1
        Other = 0
    else:
        Arab = 0
        Jewish = 0
        Caucasian = 0
        Hispanic = 0
        Asian = 0
        Other = 1

    # Headache
    if Joint == 'Sometimes or often':
        Joint_1 = 1
        Joint_2 = 0
    elif Joint == 'Always':
        Joint_1 = 0
        Joint_2 = 1
    else:
        Joint_1 = 0
        Joint_2 = 0

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


    if (Number_episodes == 0 and Duration_episodes < 0.5 and
        MucoCu_var == 0 and Cardio_var == 0 and Gastr_var == 0 and Const_var == 0 and
        Joint_1 == 0 and Joint_2 == 0 and Abd_1 == 0 and Abd_2 == 0 and
        Chest_1 == 0 and Chest_2 == 0):
        st.warning("You cannot make a prediction based on ethnicity alone.")
        return None
    data = {
            'Number of episodes/year': Number_episodes,
            'duration of episodes (days)': Duration_episodes,
            'A_MucoCu': MucoCu_var,
            'D_Gastr': Gastr_var,
            'F_Cardio': Cardio_var,
            'I_Const': Const_var,
            'Ethnicity_Caucasian': Caucasian,
            'Ethnicity_Arab': Arab,
            'Ethnicity_Hispanic': Hispanic,
            'Ethnicity_Jewish': Jewish,
            'Ethnicity_Other': Other,
            'Ethnicity_Asian': Asian,
            'Abdominal pain_1.0': Abd_1,
            'Abdominal pain_2.0': Abd_2,
            'Chest pain_1.0': Chest_1,
            'Chest pain_2.0': Chest_2,
            'Arthralgia_1.0': Joint_1,
            'Arthralgia_2.0': Joint_2
            }
    features = pd.DataFrame(data, index=[0])

    # Set Number_episodes to 1 if it was originally 0
    if Number_episodes == 0:
        features['Number of episodes/year'] = 1

    # Set Duration_episodes to 0.5 if it was less than 0.5
    if Duration_episodes < 0.5:
        features['duration of episodes (days)'] = 0.5

    return features






st.markdown("<hr>", unsafe_allow_html=True)

_, left_button, right_button, _ = st.columns([3,1,1,3])
predicted = False
cleared = False

with left_button:
    if st.button("Predict"):
        st.spinner()

        # Check if any data is entered
        input_df = user_input_features()
        if input_df is None:
            st.warning("No prediction available.")

        else:
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
