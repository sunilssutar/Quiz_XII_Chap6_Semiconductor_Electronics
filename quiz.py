
import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# QUIZ QUESTIONS
# -------------------------------

questions = [
    {
        "question": "What is the SI unit of electric charge?",
        "options": ["Coulomb", "Ampere", "Volt", "Ohm"],
        "answer": "Coulomb",
        "marks": 1
    },
    {
        "question": "Which law describes the force between two point charges?",
        "options": [
            "Newton's law",
            "Coulomb's law",
            "Ohm's law",
            "Faraday's law"
        ],
        "answer": "Coulomb's law",
        "marks": 1
    },
    {
        "question": "What is the SI unit of electric field?",
        "options": ["N/C", "Joule", "Coulomb", "Watt"],
        "answer": "N/C",
        "marks": 1
    }
]

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Physics Quiz",
    page_icon="📝"
)

st.title("Class 12 Physics Quiz")
st.write("Chapter: Electrostatics")

st.divider()

# -------------------------------
# STUDENT DETAILS AND QUIZ
# -------------------------------

with st.form("quiz_form"):

    st.subheader("Student Details")

    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")

    st.divider()

    st.subheader("Answer the Questions")

    responses = []

    for i, q in enumerate(questions):

        st.write(f"**Q{i+1}. {q['question']}**")

        response = st.radio(
            "Select your answer:",
            q["options"],
            index=None,
            key=f"question_{i}"
        )

        responses.append(response)

        st.write("")

    submitted = st.form_submit_button("Submit Quiz")

# -------------------------------
# EVALUATION
# -------------------------------

if submitted:

    if not name.strip() or not roll.strip():
        st.error("Please enter your name and roll number.")

    elif any(answer is None for answer in responses):
        st.warning("Please answer all questions before submitting.")

    else:

        score = 0
        results = []

        for i, q in enumerate(questions):

            correct = responses[i] == q["answer"]

            if correct:
                score += q["marks"]

            results.append({
                "Question": q["question"],
                "Your Answer": responses[i],
                "Correct Answer": q["answer"],
                "Result": "Correct" if correct else "Incorrect"
            })

        total_marks = sum(q["marks"] for q in questions)

        st.success("Quiz submitted successfully!")

        st.subheader("Your Result")

        st.metric(
            "Score",
            f"{score} / {total_marks}"
        )

        st.write(f"Student: {name}")
        st.write(f"Roll Number: {roll}")

        st.subheader("Answer Review")

        st.dataframe(pd.DataFrame(results))

        # Save result
        student_result = pd.DataFrame([{
            "Date": datetime.now().isoformat(),
            "Name": name,
            "Roll Number": roll,
            "Score": score,
            "Total Marks": total_marks
        }])

        try:
            student_result.to_csv(
                "quiz_results.csv",
                mode="a",
                header=not __import__("os").path.exists(
                    "quiz_results.csv"
                ),
                index=False
            )
            st.info("Your result has been recorded.")

        except Exception as e:
            st.error(f"Could not save result: {e}")