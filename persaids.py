import time
import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="FMF Predictor", page_icon=":hospital:", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>Familial Mediterranean Fever (FMF) Predictor.</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Please fill the form below and click the predict button to see how likely your patient has FMF.</h3>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

input_df = []


# Create a three-column form layout
_, c1, c2, c3, _ = st.columns([0.25, 1.5, 1.5, 1.5, 0.25])

with c1:
    Number_episodes = st.number_input("Number of Episodes", min_value=0, max_value=30, help="Write the number of episodes in a year.")
    Chest_pain = st.radio("Chest Pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the symptom best.")
    MucoCu = st.radio("Mucocutaneous Manifestations? ", ('Yes', 'No'), horizontal =True)
    Neuro = st.radio("Neurologic  Manifestations? ", ('Yes', 'No'), horizontal =True)


with c2:
    Duration_episodes = st.number_input("Duration of Episodes", min_value=0.0, max_value=25.0, help="in days")
    Abdominal_pain = st.radio("Abdominal Pain", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the symptom best.")
    Cardio = st.radio("Cardiologic Manifestations? ", ('Yes', 'No'), horizontal =True)
    Gastr = st.radio("Gastrointestinal Manifestations? ", ('Yes', 'No'), horizontal =True)

with c3:
    Ethnicity = st.selectbox("Ethnicity:", ('Choose the ethnicty', 'Arab', 'Jewish', 'Caucasian', 'Hispanic', 'Asian', 'Other'), key='ethnicity', help="Select what group decribes the best.")
    Headache = st.radio("Headache(anytime)", ('Never', 'Sometimes or often', 'Always'), horizontal =True, help="Select what describes the symptom best.")
    Const = st.radio("Constitutional Manifestations? ", ('Yes', 'No'), horizontal =True)



def user_input_features():
    MucoCu_var = (1 if MucoCu == 'Yes' else 0)
    Cardio_var = (1 if Cardio == 'Yes' else 0)
    Gastr_var = (1 if Gastr == 'Yes' else 0)
    Const_var = (1 if Const == 'Yes' else 0)
    Neuro_var = (1 if Neuro == 'Yes' else 0)
    Caucasian = (1 if Ethnicity == 'Caucasian' else 0)
    Head_var = (1 if Headache == 'Sometimes or often' else 0)
    Abd_var = (1 if Abdominal_pain == 'Always' else 0)
    Chest_var = (1 if Chest_pain == 'Sometimes or often' else 0)


    data = {
            'Number of episodes/year': Number_episodes,
            'duration of episodes (days)': Duration_episodes,
            'Ethnicity_Caucasian': Caucasian,
            'Chest pain_1.0': Chest_var,
            'Abdominal pain_2.0': Abd_var,
            'Headache (anytime)_1.0':Head_var,
            'A_MucoCu': MucoCu_var,
            'F_Cardio': Cardio_var,
            'I_Const': Const_var,
            'D_Gastr': Gastr_var,
            'G_Neuro': Neuro_var
            }
    features = pd.DataFrame(data, index=[0])
    return features


st.markdown("<hr>", unsafe_allow_html=True)

_, left_button, right_button, _ = st.columns([5, 1, 1,  5])
predicted = False
cleared = False

with left_button:
    if st.button("Predict"):
        if  (Duration_episodes == 0 and Duration_episodes == 0.0 and Chest_pain != 'Sometimes or often' and
             MucoCu == 'No' and Abdominal_pain != 'Always' and Cardio == 'No' and Gastr == 'No' and
             Neuro == 'No' and Headache != 'Sometimes or often' and Const == 'No') or Ethnicity == 'Choose the ethnicty':
            st.error("Please provide more information for an accurate prediction.")
        else:
            st.spinner()
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
        st.markdown("<div style='padding: 10px; background-color: yellow;'>"
                    "It is <strong>unlikely</strong> that the patient has FMF. "
                    "Because, my calculations show <strong>{:.2f}%</strong> probability."
                    "</div>".format(probabilityOfFMF), unsafe_allow_html=True)
    elif 50 <= probabilityOfFMF <= 75:
        st.markdown("<div style='padding: 10px; background-color: orange;'>"
                    "It is <strong>possible</strong> that the patient has FMF. "
                    "Because, my calculations show <strong>{:.2f}%</strong> probability."
                    "</div>".format(probabilityOfFMF), unsafe_allow_html=True)
    else:
        st.markdown("<div style='padding: 10px; background-color: green; color: white;'>"
                    "It is <strong>likely</strong> that the patient may have FMF. "
                    "Because, my calculations show <strong>{:.2f}%</strong> probability."
                    "</div>".format(probabilityOfFMF), unsafe_allow_html=True)

if cleared =='True':
    st.experimental_rerun()
