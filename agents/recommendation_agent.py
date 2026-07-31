class RecommendationAgent:

    def get_recommendation(self, disease):

        recommendations = {

            "Common Cold": [
                "Drink plenty of water.",
                "Take adequate rest.",
                "Eat healthy food.",
                "Consult a doctor if fever lasts more than 3 days."
            ],

            "Flu": [
                "Take sufficient rest.",
                "Drink warm fluids.",
                "Monitor body temperature.",
                "Visit a doctor if breathing becomes difficult."
            ],

            "COVID-19": [
                "Isolate yourself.",
                "Wear a mask.",
                "Monitor oxygen levels.",
                "Seek immediate medical care if breathing becomes difficult."
            ],

            "Diabetes Risk": [
                "Reduce sugar intake.",
                "Exercise regularly.",
                "Monitor blood glucose.",
                "Consult a diabetologist."
            ],

            "Hypertension": [
                "Reduce salt intake.",
                "Exercise regularly.",
                "Check blood pressure frequently.",
                "Consult a cardiologist."
            ]

        }

        return recommendations.get(
            disease,
            ["Please consult a medical professional."]
        )