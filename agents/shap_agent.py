import pandas as pd
import matplotlib.pyplot as plt


class SHAPAgent:

    def explain(self, patient):

        importance = {
            "Age": patient["Age"] * 0.3,
            "Fever": patient["Fever"] * 20,
            "Cough": patient["Cough"] * 18,
            "Headache": patient["Headache"] * 12,
            "Fatigue": patient["Fatigue"] * 15,
            "Chest Pain": patient["Chest_Pain"] * 18,
            "Family History": patient["Family_History"] * 22
        }

        df = pd.DataFrame(
            importance.items(),
            columns=["Feature", "Importance"]
        )

        df = df.sort_values(
            by="Importance",
            ascending=False
        )

        fig, ax = plt.subplots()

        ax.barh(
            df["Feature"],
            df["Importance"]
        )

        ax.set_title("Explainable AI (Feature Importance)")

        return fig