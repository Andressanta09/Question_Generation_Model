# Question_Generation_Model
Backend and frontend of an application to generate interview questions for the IT department preference.

# 🗣️ Job Interview Question Generator App

This is a Streamlit web application powered by Google Gemini that generates customized interview questions based on job roles, required skills, or full job descriptions.

## 🚀 Features

- 🎯 Generate technical, behavioral, logical, or mixed interview questions.
- 🤖 AI-powered by Google Gemini 1.5 Flash.
- 📄 Export questions as PDF or TXT.
- 🧠 Two modes:
  - Based on required skills and role.
  - Based on full job description text.

## 🧱 Technologies

- [Streamlit](https://streamlit.io/)
- [Google Generative AI SDK](https://ai.google.dev/)
- [FPDF](https://pyfpdf.github.io/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)
- [Pillow](https://python-pillow.org/)
- [Pygments](https://pygments.org/)

## 📁 Project Structure

job-interview-question-app/
-├── main_app.py # Main Streamlit app
-├── question_gen.py # Generator using structured inputs
-├── question_gen2.py # Generator using job description
-├── requirements.txt
-├── DejaVuSans.ttf # (Optional font for PDF generation)
-└── README.md

## ▶️ Run Locally

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/job-interview-question-app.git
    cd job-interview-question-app
    ```

2. Create `.env` file and set your Google API Key:
    ```
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:
    ```bash
    streamlit run main_app.py
    ```

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud).
3. Connect your GitHub account and select this repository.
4. Set `main_app.py` as the entry point.
5. Add a secret `GEMINI_API_KEY` in the **Secrets Manager**.

## 📃 License

This project is under the MIT License. Feel free to modify and use it as you wish.

---

## 💬 Feedback

Pull requests and feedback are welcome!
