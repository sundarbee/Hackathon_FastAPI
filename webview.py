import streamlit as st
import pandas as pd
import joblib

# Load the pre-trained model
model = joblib.load('promotion_model.pkl')

st.title('Employee Promotion Prediction')
st.write('Enter employee details to predict promotion status.')

# Input fields for the model features
# Categorical features
department_options = ['Sales & Marketing', 'Operations', 'Technology', 'Analytics', 'R&D', 'Procurement', 'Finance', 'HR', 'Legal']
region_options = ['region_7', 'region_22', 'region_19', 'region_23', 'region_26', 'region_2', 'region_20', 'region_13', 'region_16', 'region_4', 'region_28', 'region_11', 'region_27', 'region_31', 'region_15', 'region_25', 'region_14', 'region_17', 'region_5', 'region_3', 'region_29', 'region_8', 'region_32', 'region_30', 'region_10', 'region_9', 'region_6', 'region_21', 'region_24', 'region_12', 'region_1', 'region_18']
education_options = ["Master's & above", "Bachelor's", 'Below Secondary']
gender_options = ['f', 'm']
recruitment_channel_options = ['sourcing', 'other', 'referred']

department = st.selectbox('Department', department_options)
region = st.selectbox('Region', region_options)
education = st.selectbox('Education', education_options)
gender = st.selectbox('Gender', gender_options)
recruitment_channel = st.selectbox('Recruitment Channel', recruitment_channel_options)

# Numerical features
no_of_trainings = st.number_input('Number of Trainings', min_value=1, max_value=10, value=1)
age = st.number_input('Age', min_value=18, max_value=60, value=30)
previous_year_rating = st.slider('Previous Year Rating', min_value=1.0, max_value=5.0, value=3.0, step=1.0)
length_of_service = st.number_input('Length of Service (years)', min_value=1, max_value=37, value=5)
kpis_met = st.radio('KPIs Met >80%', options=[0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
awards_won = st.radio('Awards Won?', options=[0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
avg_training_score = st.number_input('Average Training Score', min_value=30, max_value=100, value=60)

# Create a DataFrame from user input
input_data = pd.DataFrame({
    'department': [department],
    'region': [region],
    'education': [education],
    'gender': [gender],
    'recruitment_channel': [recruitment_channel],
    'no_of_trainings': [no_of_trainings],
    'age': [age],
    'previous_year_rating': [previous_year_rating],
    'length_of_service': [length_of_service],
    'KPIs_met >80%': [kpis_met],
    'awards_won?': [awards_won],
    'avg_training_score': [avg_training_score]
})

if st.button('Predict Promotion'):
    prediction = model.predict(input_data)
    if prediction[0] == 1:
        st.success('The employee is predicted to be PROMOTED!')
    else:
        st.info('The employee is predicted NOT to be promoted.')

