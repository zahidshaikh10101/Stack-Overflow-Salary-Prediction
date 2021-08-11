import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x:
        return 'Post grad'
    return 'Other degrees'

def clean_gender(x):
    if 'Man' in x:
        return 'Male'
    if 'Woman' in x:
        return 'Female'
    return 'Other'


@st.cache
def load_data():
    data = pd.read_csv("survey_results_public.csv")
    data = data[['Age', 'Country', 'EdLevel', 'Employment', 'Gender', 'YearsCodePro', 'ConvertedComp']]
    data = data[data['ConvertedComp'].notnull()]
    data = data.dropna()
    data = data[data['Employment'] == "Employed full-time"]
    data = data.drop('Employment', axis=1)

    country_map = shorten_categories(data.Country.value_counts(), 300)
    data["Country"] = data["Country"].map(country_map)
    data = data[data["ConvertedComp"] <= 250000]
    data = data[data["ConvertedComp"] >= 10000]
    data = data[data["Country"] != "Other"]

    data["YearsCodePro"] = data["YearsCodePro"].apply(clean_experience)
    data["EdLevel"] = data["EdLevel"].apply(clean_education)
    data['Gender'] = data['Gender'].apply(clean_gender)
    data = data.rename({"ConvertedComp": "Salary", "EdLevel": "Education"}, axis=1)
    return data

df = load_data()

def show_explore_page():

    st.markdown("<h1 style='text-align: center; color: white;'>Explore Software Engineer Salaries</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color:grey;'>Stack Overflow Developer Survey 2020</h4>", unsafe_allow_html=True)
    st.write('')


    st.markdown('___')

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    st.markdown('___')

    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.markdown('___')
    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.markdown("<h4 style='text-align: center; color:grey;'>Made with ❤️ by Zahid Shaikh</h4>", unsafe_allow_html=True)