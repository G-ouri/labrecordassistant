import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
from google import genai


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Lab Record Assistant",
    page_icon="🧪",
    layout="wide"
)


# =========================================================
# AI SETUP
# =========================================================

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(api_key=API_KEY)

    MODEL = "gemini-2.5-flash"

except Exception:
    client = None


def ask_ai(prompt):

    if client is None:
        return "AI connection not configured. Please add GEMINI_API_KEY in Streamlit Secrets."

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧪 AI Lab Assistant")

page = st.sidebar.radio(
    "Choose Feature",
    [
        "🏠 Dashboard",
        "🤖 Experiment Generator",
        "📷 Lab Record OCR",
        "📊 Observation Analyzer",
        "🎤 AI Viva"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("🧪 AI Lab Record Assistant")

    st.subheader("Smart Laboratory Management using AI")

    st.write(
        """
        An AI-powered laboratory assistant that helps students
        generate experiments, digitize handwritten records,
        analyze observations, generate graphs and prepare for viva.
        """
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("AI Features", "5")

    with col2:
        st.metric("Record Processing", "OCR + AI")

    with col3:
        st.metric("Graph Analysis", "Automatic")

    with col4:
        st.metric("Viva", "AI Powered")

    st.divider()

    st.subheader("Available Features")

    st.markdown(
        """
        ### 🤖 Experiment Generator
        Generate complete laboratory experiments using AI.

        ### 📷 Lab Record OCR
        Upload a scanned/photographed lab record and convert it
        into structured digital content.

        ### 📊 Observation Analyzer
        Enter experimental observations, generate graphs and
        automatically analyze the results.

        ### 🎤 AI Viva
        Generate viva questions based on your experiment.

        ### 📝 Result Generator
        Automatically generate result and conclusion sections.
        """
    )


# =========================================================
# EXPERIMENT GENERATOR
# =========================================================

elif page == "🤖 Experiment Generator":

    st.title("🤖 AI Experiment Generator")

    topic = st.text_input(
        "Enter experiment topic",
        placeholder="Example: Breadth First Search"
    )

    if st.button("Generate Experiment", type="primary"):

        if topic.strip() == "":
            st.warning("Please enter an experiment topic.")

        else:

            with st.spinner("Generating experiment..."):

                prompt = f"""
You are an AI college laboratory assistant.

Create a laboratory experiment for:

{topic}

Generate:

1. Title
2. Objective
3. Requirements
4. Theory
5. Procedure
6. Algorithm
7. Expected Result
8. Five Viva Questions

Keep the content concise and suitable for a college
engineering laboratory record.
"""

                result = ask_ai(prompt)

            st.subheader("Generated Laboratory Experiment")

            st.markdown(result)


# =========================================================
# OCR LAB RECORD
# =========================================================

elif page == "📷 Lab Record OCR":

    st.title("📷 AI Lab Record Digitizer")

    st.write(
        "Upload a photo or scanned image of your laboratory record."
    )

    uploaded_file = st.file_uploader(
        "Upload Lab Record",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Lab Record",
            width=500
        )

        if st.button("Extract & Structure Record", type="primary"):

            with st.spinner("Reading laboratory record..."):

                # OCR
                extracted_text = pytesseract.image_to_string(image)

            st.subheader("OCR Text")

            st.text_area(
                "Extracted Text",
                extracted_text,
                height=200
            )

            with st.spinner("Structuring record using AI..."):

                prompt = f"""
You are an AI laboratory record assistant.

Convert the following OCR text into a structured
laboratory record.

OCR TEXT:
{extracted_text}

Return:

Title:
Objective:
Requirements:
Theory:
Procedure:
Algorithm:
Observations:
Result:
Conclusion:

IMPORTANT:
Do not invent information.
If information is missing, write "Not available".
"""

                structured = ask_ai(prompt)

            st.subheader("Structured Laboratory Record")

            st.markdown(structured)


# =========================================================
# OBSERVATION ANALYZER
# =========================================================

elif page == "📊 Observation Analyzer":

    st.title("📊 AI Observation Analyzer")

    st.write(
        "Enter your experimental observations below."
    )

    default_data = pd.DataFrame({
        "Input Size": [10, 20, 30, 40, 50],
        "Execution Time": [0.02, 0.05, 0.09, 0.15, 0.22]
    })

    edited_data = st.data_editor(
        default_data,
        num_rows="dynamic",
        use_container_width=True
    )

    if st.button("Analyze Observations", type="primary"):

        if len(edited_data.columns) < 2:

            st.error("Please provide at least two columns.")

        else:

            x_column = edited_data.columns[0]
            y_column = edited_data.columns[1]

            st.subheader("Experimental Graph")

            try:

                fig, ax = plt.subplots()

                ax.plot(
                    edited_data[x_column],
                    edited_data[y_column],
                    marker="o"
                )

                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)

                ax.set_title(
                    f"{x_column} vs {y_column}"
                )

                ax.grid(True)

                st.pyplot(fig)

            except Exception as e:

                st.error(
                    "Could not create graph. "
                    "Please make sure the columns contain numbers."
                )

            data_text = edited_data.to_string(index=False)

            with st.spinner("AI is analyzing observations..."):

                analysis_prompt = f"""
You are an AI laboratory data analysis assistant.

Analyze the following experimental observations:

{data_text}

Provide:

1. Observed trend
2. Relationship between variables
3. Important observations
4. Possible explanation
5. Conclusion

Use ONLY the given data.
Do not invent values.
"""

                analysis = ask_ai(analysis_prompt)

            st.subheader("🤖 AI Analysis")

            st.markdown(analysis)

            with st.spinner("Generating result..."):

                result_prompt = f"""
Write a short laboratory RESULT and CONCLUSION.

Experimental data:

{data_text}

AI Analysis:

{analysis}

Do not invent experimental values.
"""

                result = ask_ai(result_prompt)

            st.subheader("📝 Result & Conclusion")

            st.markdown(result)


# =========================================================
# AI VIVA
# =========================================================

elif page == "🎤 AI Viva":

    st.title("🎤 AI Viva Examiner")

    experiment = st.text_area(
        "Enter your experiment",
        placeholder="Example: Implement Breadth First Search using Python.",
        height=150
    )

    if st.button("Generate Viva Questions", type="primary"):

        if experiment.strip() == "":

            st.warning("Please enter an experiment.")

        else:

            with st.spinner("Preparing viva questions..."):

                prompt = f"""
You are an AI viva examiner for a college laboratory.

Experiment:

{experiment}

Generate 5 viva questions.

For each question provide:

Question:
Expected Answer:
Difficulty:

Keep answers short and educational.
"""

                viva = ask_ai(prompt)

            st.subheader("🎓 Viva Questions")

            st.markdown(viva)


# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.caption(
    "AI Lab Record Assistant | Hackathon Prototype"
)
