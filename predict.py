import pickle
import streamlit as st
import numpy as np
import time


def load_model():
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_edu = data["le_edu"]
le_gender = data["le_gender"]

def show_predict_page():

    st.markdown("<h1 style='text-align: center; color: white;'>Software Developer Salary Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color:grey;'>We need some information to predict the salary</h4>", unsafe_allow_html=True)
    st.write('')

    st.markdown('___')

    age = st.slider("Age", 20, 90, 20)

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        'Bachelor’s degree',
        'Master’s degree',
        'Post grad',
        'Other degrees',
    )

    gender = (
        "Male",
        "Female",
        "Others",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    gender = st.radio("Gender", gender)

    expericence = st.slider("Years of Experience", 0, 70, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[age, country, education, gender, expericence]])
        X[:, 1] = le_country.transform(X[:,1])
        X[:, 2] = le_edu.transform(X[:,2])
        X[:, 3] = le_gender.transform(X[:,3])
        X = X.astype(float)

        st.spinner()
        with st.spinner(text='Gathering Infomation '):
            time.sleep(3)
        

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
        st.success('Sucecessfully Completed')
        


    st.markdown("<h4 style='text-align: center; color:grey;'>Made with ❤️ by Zahid Shaikh</h4>", unsafe_allow_html=True)