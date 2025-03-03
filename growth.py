import streamlit as st
import random
import pandas as pd
from fpdf import FPDF

# Configure Page
st.set_page_config(page_title="Grammar Growth Challenge", page_icon="📚", layout="wide")

# Custom Styles
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            font-size: 18px;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTitle, .stHeader, .stSubheader {
            color: #1E90FF;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Introduction
st.title("📖 Grammar Growth Challenge")
st.header("Develop Your English Grammar Skills with a Growth Mindset!")
st.write("Challenge yourself with multiple-choice questions and track your progress.")

# Daily Grammar Tip
st.subheader("🌟 Daily Grammar Tip")
grammar_tips = [
    "Use 'their' for possession, 'there' for location, and 'they're' for 'they are'.",
    "Always capitalize the first letter of a sentence and proper nouns.",
    "Use 'its' for possession and 'it's' for 'it is'.",
    "A sentence must have a subject, a verb, and a complete thought.",
    "Use commas to separate items in a list: 'I bought apples, oranges, and bananas.'",
]
st.success(random.choice(grammar_tips))

# MCQs Data
questions = {
    "Which sentence is grammatically correct?": ["I am going too the store.", "She don’t like ice cream.", "They're going to the park.", "They're going to the park."],
    "Choose the correct word: 'I am taller ___ my brother.'": ["then", "than", "them", "than"],
    "Which word correctly completes the sentence: 'She ___ a beautiful song yesterday.'": ["singed", "sang", "sung", "sang"],
    "What is the correct plural of 'child'?": ["childs", "children", "childes", "children"],
    "Identify the verb: 'She quickly ran to the store.'": ["She", "quickly", "ran", "ran"],
    "Which is a correct sentence?": ["He go to school.", "She went to the park.", "They is playing.", "She went to the park."],
    "Which is the correct spelling?": ["recieve", "receive", "receve", "receive"],
}

# Generate 10 Random Questions
quiz_questions = random.sample(list(questions.keys()), 10)

# Store User Answers
user_answers = {}

st.subheader("✍️ Take the Grammar Quiz")
for i, question in enumerate(quiz_questions):
    options = questions[question][:3]
    correct_answer = questions[question][3]  # Last option is correct
    user_answers[question] = st.radio(f"**{i+1}. {question}**", options, index=None, key=f"q{i}")

# Submit Button
if st.button("📊 Submit Answers & Get Score"):
    score = sum(1 for q in quiz_questions if user_answers[q] == questions[q][3])
    percentage = (score / len(quiz_questions)) * 100

    st.subheader("🎯 Your Quiz Result")
    st.success(f"✅ You scored **{score} out of {len(quiz_questions)}**!")
    st.info(f"📊 Percentage: **{percentage:.2f}%**")

    # Score Feedback
    if percentage >= 80:
        st.balloons()
        st.success("🌟 Excellent! Keep it up!")
    elif percentage >= 50:
        st.warning("😊 Good job! Keep practicing.")
    else:
        st.error("😢 Don't worry! Try again and improve.")

    # Save Results in a DataFrame
    data = {
        "Question": quiz_questions,
        "Your Answer": [user_answers[q] for q in quiz_questions],
        "Correct Answer": [questions[q][3] for q in quiz_questions],
    }
    df = pd.DataFrame(data)

    # Buttons for Exporting Data
    st.subheader("📁 Export Your Score")

    # CSV Download
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv_data, "grammar_quiz_results.csv", "text/csv")

    # Excel Download
    excel_data = df.to_excel("grammar_quiz_results.xlsx", index=False)
    with open("grammar_quiz_results.xlsx", "rb") as f:
        st.download_button("📥 Download Excel", f, "grammar_quiz_results.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # PDF Download
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(200, 10, "Grammar Quiz Results", ln=True, align="C")

        def chapter_title(self, title):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, title, ln=True, align="L")
            self.ln(5)

        def chapter_body(self, body):
            self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, body)
            self.ln()

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Grammar Quiz Results", ln=True, align="C")
    pdf.ln(10)

    for i, q in enumerate(quiz_questions):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{i+1}. {q}", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Your Answer: {user_answers[q]}", ln=True)
        pdf.cell(0, 10, f"Correct Answer: {questions[q][3]}", ln=True)
        pdf.ln()

    pdf.cell(0, 10, f"Total Score: {score} out of {len(quiz_questions)}", ln=True)
    pdf.cell(0, 10, f"Percentage: {percentage:.2f}%", ln=True)

    pdf_output = "grammar_quiz_results.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as f:
        st.download_button("📥 Download PDF", f, pdf_output, "application/pdf")

st.write("---")
st.write("💡 Keep challenging yourself, learning from mistakes, and growing with every step! 🚀")
st.write("**Created by Sadia, GIAIC Student.**")
