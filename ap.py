import streamlit as st
from main import ask_question

st.set_page_config(page_title="Interview Prep RAG", page_icon="💼")

st.title("💼 Interview Prep Assistant")
st.write("Ask me anything about Shri's experience, projects, and skills!")

# Example questions
st.sidebar.header("Example Questions")
example_questions = [
    "Tell me about the MicroStrategy internship",
    "What distributed systems projects have you worked on?",
    "Explain your deep learning experience",
    "What's your experience with AWS?",
    "Tell me about your RAG system projects",
    "What machine learning frameworks do you know?",
]

for eq in example_questions:
    if st.sidebar.button(eq):
        st.session_state.question = eq

# Main query input
question = st.text_input(
    "Ask a question:", 
    value=st.session_state.get('question', ''),
    placeholder="e.g., Tell me about your distributed systems experience"
)

if st.button("Get Answer") or question:
    if question:
        with st.spinner("Searching and generating answer..."):
            answer, contexts = ask_question(question)
            
            st.success("Answer:")
            st.write(answer)
            
            with st.expander("📚 View Source Documents"):
                for i, ctx in enumerate(contexts):
                    st.write(f"**Source {i+1}:** {ctx['source']} (Relevance: {ctx['score']:.3f})")
                    st.text(ctx['text'][:300] + "...")
                    st.divider()
    else:
        st.warning("Please enter a question!")