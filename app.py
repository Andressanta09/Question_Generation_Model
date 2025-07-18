import os
import json
import streamlit as st
from question_gen import question_generator_gemini
from fpdf import FPDF
import tempfile
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from PIL import Image
import io



st.set_page_config(page_title="Interview Question Generator", layout="centered")

st.title("🗣️ Job Interview Question Generator 📊")

def code_to_image(code_text: str) -> str:
    """
    Renders a code snippet as an image with syntax highlighting using Courier New.
    """
    formatter = ImageFormatter(
        font_name='Courier New',  # compatible with Windows
        line_numbers=True,
        style='default',
        image_format='PNG'
    )
    img_data = io.BytesIO()
    highlight(code_text, PythonLexer(), formatter, outfile=img_data)
    img_data.seek(0)
    image = Image.open(img_data)
    tmp_image_path = tempfile.NamedTemporaryFile(delete=False, suffix='.png').name
    image.save(tmp_image_path)
    return tmp_image_path


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
        
        blocks = resultado.split('\n')
        in_code_block = False
        code_lines = []

        for line in blocks:
            # Detectar inicio o fin de bloque de código
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                if not in_code_block:
                    # Mostrar bloque de código acumulado
                    st.code("\n".join(code_lines), language="python")
                    code_lines = []
                continue

            if in_code_block:
                code_lines.append(line)
            else:
                if line.strip():  # línea no vacía
                    st.markdown(line.strip())
      
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

        code_block = []
        in_code = False

        for line in blocks:
            if line.strip().startswith("```"):
                in_code = not in_code
                if not in_code:
                    code_image_path = code_to_image("\n".join(code_block))
                    pdf.image(code_image_path, w=180)
                    code_block = []
                continue

            if in_code:
                code_block.append(line)
            else:
                if line.strip():
                    pdf.multi_cell(0, 10, line.strip())
                    pdf.ln(1)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            st.download_button(
                label="📄 Download questions in PDF",
                data=open(tmp_file.name, "rb").read(),
                file_name="interview_questions.pdf",
                mime="application/pdf"
            )
