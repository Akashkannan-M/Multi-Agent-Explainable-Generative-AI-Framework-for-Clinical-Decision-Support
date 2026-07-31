class ImageAgent:

    def analyze_image(self, filename):

        filename = filename.lower()

        if "skin" in filename:
            return "Possible Skin Disease detected."

        elif "xray" in filename:
            return "Possible Lung Infection detected."

        elif "brain" in filename:
            return "Possible Brain Abnormality detected."

        elif "eye" in filename:
            return "Possible Eye Disease detected."

        else:
            return "No abnormality detected."