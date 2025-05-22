import os
import streamlit as st
from question_gen import question_generator_gemini  # Asegúrate que el archivo y función se llamen así
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="Interview Question Generator", layout="centered")

st.title("🗣️ Job Interview Question Generator 📊")

# Entradas del usuario
rol = st.text_input("Job position 🔍", placeholder="Example: Data Analyst")
level = st.selectbox("Candidate level", ["Entry", "Junior", "Mid", "Senior"])
type = st.selectbox("Type of questions", ["Technique", "Behavioral", "Logical", "Mixed"])
n_questions = st.slider("#️⃣ Number of questions", 1, 10, 5)
level_description = st.text_input("More detailed description of the candidate's level", placeholder="Example: 'recent graduate with little experience', 'professional with 5 years of experience in the sector'.")
responsibilities = st.text_input("The 3-5 main responsibilities of the position are: ", placeholder="Example: 'Cleaning data sets', 'Developing predictive models using statistical techniques.'") 
technical_skills = st.text_input("The 3-5 key technical skills or knowledge required are: ", placeholder="Example: SQL, Python, etc.")
soft_skills = st.text_input("The 3-5 soft skills or competencies important for success in the position are: ", placeholder="Example: Communication, Collaboration, Critical Thinking,..")

# Botón para generar preguntas
if st.button("Generate questions"):
    if not rol:
        st.warning("Please enter a role.")
    else:
        with st.spinner("Generating questions...⏳"):
            resultado = question_generator_gemini(
                rol=rol,
                level=level,
                level_description=level_description,
                type=type,
                responsibilities=responsibilities,
                technical_skills=technical_skills,
                soft_skills=soft_skills,
                n=n_questions
            )

        st.markdown("### ✅ Questions generated:")
        
        preguntas = [line.strip() for line in resultado.strip().split('\n') if line.strip()]
        for pregunta in preguntas:
            st.markdown(f"- {pregunta}")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        try:
            font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
            pdf.add_font("DejaVu", "", font_path, uni=True)
            pdf.set_font("DejaVu", size=12)
        except Exception:
            pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, "Job Interview Questions", ln=True, align='C')
        pdf.ln(5)

        for linea in preguntas:
            pdf.multi_cell(0, 10, linea)
            pdf.ln(1)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            st.download_button(
                label="📄 Download questions in PDF",
                data=open(tmp_file.name, "rb").read(),
                file_name="interview_questions.pdf",
                mime="application/pdf"
            )