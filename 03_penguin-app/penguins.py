import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

st.title("Palmer's Penguins")
st.markdown("Use this Streamlit app to make your own scatterplot about penguins!")

penguin_file = st.file_uploader('Select the csv file that contains penguins data')


@st.cache()
def load_file(penguin_file):
    time.sleep(3)

    if penguin_file is not None:
        df = pd.read_csv(penguin_file)
    else:
        st.stop()  # stop flow if no file is uploaded
    return df


penguins_df = load_file(penguin_file)
# selected_species = st.selectbox("What species would you like to visualize ?", ["Adelie", "Gentoo", "Chinstrap"])
selected_x_var = st.selectbox("What do want the x variable to be ?",
                              ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
selected_y_var = st.selectbox("What do want the y variable to be ?",
                              ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
selected_gender = st.selectbox("What genred do you want to filter for ?", ["all", "female", "male"])
# penguins_df = penguins_df[penguins_df["species"] == selected_species]

if selected_gender == "male":
    penguins_df = penguins_df.query("sex == 'male'")
elif selected_gender == "female":
    penguins_df = penguins_df.query("sex == 'female'")
else:
    pass
sns.set_style('darkgrid')
markers = {"Adelie": "X", "Gentoo": "s", "Chinstrap": "o"}
fig, ax = plt.subplots()
ax = sns.scatterplot(data=penguins_df, x=selected_x_var, y=selected_y_var, hue="species", markers=markers,
                     style="species")
plt.xlabel(selected_x_var)
plt.ylabel(selected_y_var)
plt.title(f"Scatterplot of Palmer's Penguins: {selected_gender}")
st.pyplot(fig)
