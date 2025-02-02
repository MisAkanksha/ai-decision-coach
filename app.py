import streamlit as st
import openai
import os
from dotenv import load_dotenv  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from textwrap import wrap

# ✅ Load API Key Securely From .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Check if API Key is Loaded
if not api_key:
    st.error("❌ API Key not found. Make sure it's set in the .env file!")
    st.stop()

# ✅ Initialize OpenAI Client
client = openai.OpenAI(api_key=api_key)

# 🌟 Set Page Config
st.set_page_config(page_title="Break the Loop", page_icon="🔄", layout="wide")

st.title("🔄 Break the Loop")
st.markdown("**Overthinking? Stuck in a decision spiral? Let’s break the loop and get clarity—without the mental exhaustion.**")

# 🔹 Step 1: Define the Decision
st.markdown("### 🔍 What’s Keeping You Stuck?")
decision = st.text_input("What decision are you struggling with?", placeholder="Example: Should I quit my job and start a business?")
decision_type = st.selectbox("What kind of decision is this?", ["Career", "Business", "Personal", "Investment", "Other"])

step1_complete = st.button("Let’s Map This Out →")

if step1_complete and decision:
    st.session_state["step1_complete"] = True

if st.session_state.get("step1_complete", False):
    # 🔹 Step 2: List Pros & Cons
    st.markdown("### ⚖️ What’s Pulling You Forward? What’s Holding You Back?")
    col1, col2 = st.columns(2)
    with col1:
        pros = st.text_area("✔️ Reasons This Feels Right:", placeholder="List all the positives...")
    with col2:
        cons = st.text_area("❌ Reasons This Feels Risky:", placeholder="List all the concerns...")

    step2_complete = st.button("Next: Add Key Considerations →")

    if step2_complete and pros and cons:
        st.session_state["step2_complete"] = True

if st.session_state.get("step2_complete", False):
    # 🔹 Step 3: Additional Context
    st.markdown("### 🧠 What Else Matters?")
    context = st.text_area("What other factors should be considered? (E.g., finances, emotions, timing)")

    step3_complete = st.button("Let’s Get Unstuck →")

    if step3_complete:
        st.session_state["step3_complete"] = True

if st.session_state.get("step3_complete", False):
    # 🔹 Step 4: AI Thought-Provoking Questions + Reframed Problem
    with st.spinner("Thinking..."):
        ai_prompt = f"""
        Decision: {decision}
        Type: {decision_type}
        Pros: {pros}
        Cons: {cons}
        Context: {context}

        You are a world-renowned life coach who has helped people navigate their toughest decisions.
        Your approach is warm, reflective, and empowering.
        Instead of listing pros and cons, reframe the problem in a way that helps users see their decisions more clearly.
        Ask 2 deep, thought-provoking questions that challenge biases and bring fresh perspectives.
        You NEVER make the decision for the user but instead guide them toward their own clarity.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.6,
                messages=[
                    {"role": "system", "content": "You are a world-renowned life coach. Avoid harmful topics, encourage reflection, and guide users towards clarity. Reframe their problem in a natural way and ask two thought-provoking questions."},
                    {"role": "user", "content": ai_prompt}
                ]
            )
            ai_questions = response.choices[0].message.content

            st.markdown("### 🗣 Let’s Break It Down Together")
            st.info(ai_questions)

            user_reflections = st.text_area("🧠 What Stands Out to You After Reflecting on These Questions?", placeholder="Write your insights here...")

        except Exception as e:
            st.error(f"❌ OpenAI API Error: {str(e)}")

    step4_complete = st.button("Next: Lock in Your Decision →")

    if step4_complete and user_reflections:
        st.session_state["step4_complete"] = True

if st.session_state.get("step4_complete", False):
    # 🔹 Step 5: User’s Final Decision
    final_decision = st.text_area("📌 What’s Your Move?", placeholder="After reflecting, what will you do?")

    step5_complete = st.button("Next: Confidence Check →")

    if step5_complete and final_decision:
        st.session_state["step5_complete"] = True

if st.session_state.get("step5_complete", False):
    confidence_score = st.slider("📊 How sure are you about this decision? (1-10)", min_value=1, max_value=10, value=7)

    ai_suggestions = "No additional recommendations. You seem confident!"  

    if confidence_score < 5:
        st.warning("You seem uncertain. Consider stepping away and revisiting later.")
        ai_suggestions = """
        🌿 Take a walk to clear your mind.  
        🧘 Try meditating for a few minutes.  
        ⏳ Sleep on it and revisit the decision tomorrow.  
        📖 Write down what’s still unclear and reflect.  
        """
        st.info(ai_suggestions)

    step6_complete = st.button("Finalize My Plan →")

    if step6_complete:
        st.session_state["step6_complete"] = True

if st.session_state.get("step6_complete", False):
    # 🔹 Show Report Preview Before Download
    st.markdown("### 📄 Your Decision Plan")
    st.write(f"**Decision:** {decision}")
    st.write(f"**Confidence Level:** {confidence_score}/10")
    st.write("**Pros:**", pros)
    st.write("**Cons:**", cons)
    st.write("**AI Reflections:**", ai_questions)
    st.write("**Your Thoughts:**", user_reflections)
    st.write("**Final Decision:**", final_decision)

    # ✅ Fix PDF Text Wrapping
    def wrap_text(canvas, text, x, y, max_width=80):
        """Wrap text properly so it does not run off the page"""
        wrapped_lines = wrap(text, max_width)
        for line in wrapped_lines:
            canvas.drawString(x, y, line)
            y -= 15  # Move down for next line
        return y

    if st.button("📥 Download as PDF"):
        with st.spinner("Generating your PDF..."):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pdf_filename = "decision_report.pdf"
            pdf = canvas.Canvas(pdf_filename, pagesize=letter)

            y = 750
            y = wrap_text(pdf, f"Break the Loop: Decision Report - {timestamp}", 100, y)
            y = wrap_text(pdf, f"Decision: {decision}", 100, y - 20)
            y = wrap_text(pdf, f"Confidence Score: {confidence_score}/10", 100, y - 20)
            y = wrap_text(pdf, f"Pros: {pros}", 100, y - 20)
            y = wrap_text(pdf, f"Cons: {cons}", 100, y - 20)
            y = wrap_text(pdf, f"AI Insights: {ai_questions}", 100, y - 20)
            y = wrap_text(pdf, f"Your Thoughts: {user_reflections}", 100, y - 20)
            y = wrap_text(pdf, f"Final Decision: {final_decision}", 100, y - 20)

            pdf.save()

            with open(pdf_filename, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button("📥 Download as PDF", data=pdf_bytes, file_name="decision_report.pdf", mime="application/pdf")

# 🔹 Footer Disclaimer at the Bottom
st.markdown(
    "<div style='text-align: center; font-size: 12px; margin-top: 50px;'>"
    "⚠️ This tool is designed for structured decision-making. It is NOT a substitute for professional mental health support. "
    "<a href='https://findahelpline.com/' target='_blank'>Find Help Near You</a>"
    "</div>",
    unsafe_allow_html=True
)
