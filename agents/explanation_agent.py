
class ExplanationAgent:

    def explain(self, patient):

        reasons = []

        if patient["Fever"]:
            reasons.append("Fever detected")

        if patient["Cough"]:
            reasons.append("Cough detected")

        if patient["Headache"]:
            reasons.append("Headache detected")

        if patient["Fatigue"]:
            reasons.append("Fatigue detected")

        if patient["Chest_Pain"]:
            reasons.append("Chest Pain detected")

        if patient["Shortness_of_Breath"]:
            reasons.append("Shortness of Breath detected")

        if patient["Sore_Throat"]:
            reasons.append("Sore Throat detected")

        if patient["Vomiting"]:
            reasons.append("Vomiting detected")

        if patient["Diarrhea"]:
            reasons.append("Diarrhea detected")

        if patient["Joint_Pain"]:
            reasons.append("Joint Pain detected")

        if patient["Itching"]:
            reasons.append("Itching detected")

        if patient["Redness"]:
            reasons.append("Redness detected")

        if patient["Swelling"]:
            reasons.append("Swelling detected")

        if patient["Dry_Skin"]:
            reasons.append("Dry Skin detected")

        if patient["Burning"]:
            reasons.append("Burning sensation detected")

        if patient["Rash"]:
            reasons.append("Rash detected")

        if patient["Pain"]:
            reasons.append("Pain detected")

        if patient["Family_History"]:
            reasons.append("Family History present")

        return reasons