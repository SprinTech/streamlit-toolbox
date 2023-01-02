import streamlit as st
import pickle
import pandas as pd

st.title("Penguin Classifier")
st.write("Modify penguins characteristics to get prediction.")

penguin_file = st.file_uploader("Upload your penguin data")
if penguin_file is None:
    with open("random_forest_penguin.pickle", "rb") as f:
        rfc = pickle.load(f)

    with open("output_penguin.pickle", "rb") as f:
        unique_penguin_mapping = pickle.load(f)

else:
    penguin_df = pd.read_csv(penguin_file)

island = st.selectbox("Penguin Island", options=("Biscoe", "Dream", "Torgerson"))
sex = st.selectbox("Sex", options=("Female", "Male"))
bill_length = st.number_input("Bill Length (mm)", min_value=0)
bill_depth = st.number_input("Bill Depth (mm)", min_value=0)
flipper_length = st.number_input("Flipper Depth (mm)", min_value=0)
body_mass = st.number_input("Body Mass (g)", min_value=0)

island_biscoe, island_dream, island_torgerson = 0, 0, 0

if island == "Biscoe":
    island_biscoe = 1
elif island == "Dream":
    island_dream = 1
elif island == "Torgerson":
    island_torgerson = 1

sex_female, sex_male = 0, 0
if sex == "Female":
    sex_female = 1
elif sex == "Male":
    sex_male = 1

new_prediction = rfc.predict(
    [[bill_length, bill_depth, flipper_length, body_mass, island_biscoe, island_dream, island_torgerson, sex_female,
     sex_male]])
prediction_species = unique_penguin_mapping[new_prediction][0]
st.write(f"The penguin has chance to be {prediction_species} species")