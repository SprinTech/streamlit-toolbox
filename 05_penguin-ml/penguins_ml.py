import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

penguin_df = pd.read_csv("penguins.csv")
penguin_df.dropna(inplace=True)
output = penguin_df["species"]
features = penguin_df.drop(columns=["species", "year"])
features = pd.get_dummies(features)

output, uniques = pd.factorize(output)

X_train, X_test, y_train, y_test = train_test_split(features, output, test_size=.8)
rfc = RandomForestClassifier(random_state=15)
rfc.fit(X_train, y_train)
y_pred = rfc.predict(X_test)
score = round(accuracy_score(y_pred, y_test), 2)

print(f"Your accuracy score for this model is {score}")

with open("random_forest_penguin.pickle", "wb") as f:
    pickle.dump(rfc, f)

with open("output_penguin.pickle", "wb") as f:
    pickle.dump(uniques, f)

fig, ax = plt.subplots()
ax = sns.barplot(x=rfc.feature_importances_, y=features.columns)
plt.title("Which features are the most import for species predictions ?")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig("feature_importance.png")
