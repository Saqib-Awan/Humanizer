import streamlit as st
import random  # Remove this when you add real detector
# import your_real_ai_detector_function_here  # ← later

st.set_page_config(page_title="AI Text Humanizer", layout="centered")

# ====================== WHITE THEME + HIDE SIDEBAR ======================
st.markdown("""
<style>
    /* Hide sidebar & top menu completely */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header {display: none !important;}
    
    /* Pure white background */
    .stApp {background-color: #ffffff !important; color: #333333 !important;}
    
    /* Nice input box */
    textarea {
        border-radius: 16px !important;
        border: 2px solid #e0e0e0 !important;
        background-color: #fafafa !important;
        color: #333 !important;
        font-size: 16px !important;
    }
    
    /* Gradient button (now blue-purple for white bg) */
    div.stButton > button {
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
        color: white !important;
        border: none;
        border-radius: 50px;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(99, 102, 241, 0.5);
    }
    
    /* Title gradient */
    .gradient-title {
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown("<h1 style='text-align: center;'><span style='font-size:70px;'>✍️</span><br><span class='gradient-title'>AI Text Humanizer & Detector</span></h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color:#666; margin-top:20px; margin-bottom:50px;'>Make AI Text Undetectable • Instantly Check AI Content</h2>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; color:#777; max-width:800px; margin:0 auto 60px auto; line-height:1.8;">
The most advanced tool to humanize AI-generated text and bypass all detectors (GPTZero, Originality.ai, Turnitin, etc.)
</div>
""", unsafe_allow_html=True)

# Feature boxes (updated colors for white bg)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h3 style='color:#F59E0B; text-align:center;'>🛡️ Smart Protection</h3><ul style='color:#555;'><li>Preserves citations & formatting</li><li>100% safe for academic use</li></ul>", unsafe_allow_html=True)
with col2:
    st.markdown("<h3 style='color:#10B981; text-align:center;'>🔍 Real-Time AI Detection</h3><ul style='color:#555;'><li>Shows exact AI % before & after</li><li>Beats all detectors</li></ul>", unsafe_allow_html=True)
with col3:
    st.markdown("<h3 style='color:#8B5CF6; text-align:center;'>⚡ Instant Processing</h3><ul style='color:#555;'><li>One-click humanize</li><li>Multiple modes</li></ul>", unsafe_allow_html=True)

# ====================== MAIN INPUT ======================
text = st.text_area("", placeholder="Paste your text here...", height=280, label_visibility="collapsed")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🔍 Check for AI", use_container_width=True):
        if text.strip():
            with st.spinner("Analyzing text..."):
                # Replace with your real detector later
                ai_score = random.randint(68, 99)
            st.session_state.before_ai = ai_score
            st.success(f"⚠️ Detected: **{ai_score}% AI Content**")
        else:
            st.warning("Please enter some text first")

with col2:
    if st.button("🚀 Humanize My Text", use_container_width=True):
        if text.strip():
            with st.spinner("Humanizing your text..."):
                # ←←←←← PUT YOUR ACTUAL HUMANIZER CODE HERE ↓↓↓↓↓
                humanized = text  # ← replace this line with your real function
                # Example: humanized = humanize_function(text)
                time.sleep(1.5)  # remove this when real
                # ←←←←← END OF YOUR HUMANIZER CODE
                
                # Fake low AI score after humanizing
                after_ai = random.randint(0, 12)
                st.session_state.humanized = humanized
                st.session_state.after_ai = after_ai
            st.success("✨ Text successfully humanized!")
        else:
            st.warning("Please enter some text first")

with col3:
    if st.button("📋 Copy Result", use_container_width=True):
        if 'humanized' in st.session_state:
            st.code(st.session_state.humanized)  # triggers copy
            st.toast("Copied to clipboard!")

# ====================== RESULTS ======================
if 'humanized' in st.session_state:
    st.markdown("---")
    st.markdown("### 📄 Humanized Output")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if 'before_ai' in st.session_state:
            st.error(f"Before: **{st.session_state.before_ai}% AI Detected**")
    with col_b:
        st.success(f"After: **{st.session_state.after_ai}% AI Detected** ⚡")
    
    st.text_area("Your undetectable human text:", st.session_state.humanized, height=300, label_visibility="collapsed")
    
    # Word count comparison
    before_words = len(text.split())
    after_words = len(st.session_state.humanized.split())
    st.caption(f"Word count: {before_words} → {after_words} words")

# Footer
st.markdown("<br><div style='text-align:center; color:#aaa; font-size:14px;'>Made for undetectable, natural writing ❤️</div><br>", unsafe_allow_html=True)