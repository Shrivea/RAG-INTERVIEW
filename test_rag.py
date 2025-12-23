from main import ask_question

# Test questions
questions = [
    "Tell me about the MicroStrategy internship",
    "What distributed systems experience do you have?",
    "Explain your deep learning projects"
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print('='*60)
    answer, contexts = ask_question(q)
    print(f"\nA: {answer}\n")