import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

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
    penguin_df.dropna(inplace=True)
    output = penguin_df["species"]
    features = penguin_df.drop(columns=["species", "year"])
    features = pd.get_dummies(features)

    output, unique_penguin_mapping = pd.factorize(output)

    X_train, X_test, y_train, y_test = train_test_split(features, output, test_size=.8)
    rfc = RandomForestClassifier(random_state=15)
    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)
    score = round(accuracy_score(y_pred, y_test), 2)

with st.form("user_inputs"):
    island = st.selectbox("Penguin Island", options=("Biscoe", "Dream", "Torgerson"))
    sex = st.selectbox("Sex", options=("Female", "Male"))
    bill_length = st.number_input("Bill Length (mm)", min_value=0)
    bill_depth = st.number_input("Bill Depth (mm)", min_value=0)
    flipper_length = st.number_input("Flipper Depth (mm)", min_value=0)
    body_mass = st.number_input("Body Mass (g)", min_value=0)
    st.form_submit_button()
    
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
st.image("feature_importance.png")

fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df["bill_length_mm"], hue=penguin_df["species"])
plt.axvline(bill_length)
plt.title("Bill Length by Species")
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df["bill_depth_mm"], hue=penguin_df["species"])
plt.axvline(bill_depth)
plt.title("Bill Depth by Species")
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df["flipper_length_mm"], hue=penguin_df["species"])
plt.axvline(flipper_length)
plt.title("Flipper Length by Species")
st.pyplot(ax)
