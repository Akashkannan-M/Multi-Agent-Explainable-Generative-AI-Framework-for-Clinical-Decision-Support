from agents.genai_agent import GenAIAgent

agent = GenAIAgent()

recommendations = [
    "Drink plenty of water.",
    "Take adequate rest.",
    "Eat healthy food."
]

response = agent.generate_response(
    "Common Cold",
    29,
    recommendations
)

print(response)