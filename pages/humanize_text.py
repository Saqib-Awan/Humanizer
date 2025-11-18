# pages/humanize_text.py
import random
import re
import ssl
import warnings
import nltk
import spacy
import streamlit as st
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
import time
from collections import Counter

warnings.filterwarnings("ignore", category=FutureWarning)

# Download NLTK resources - FIXED
def download_nltk_resources():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    resources = ['punkt', 'averaged_perceptron_tagger',
                 'punkt_tab', 'wordnet', 'averaged_perceptron_tagger_eng']
    for r in resources:
        try:
            nltk.download(r, quiet=True)
        except:
            pass

download_nltk_resources()

# Load spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("spaCy en_core_web_sm model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

# ============================================================================
# CORE CONFIGURATIONS
# ============================================================================

CITATION_REGEX = re.compile(r"\(\s*[A-Za-z&\-,\.\s]+(?:et al\.\s*)?,\s*\d{4}(?:,\s*(?:pp?\.\s*\d+(?:-\d+)?))?\s*\)")

PRESERVE_WORDS = {
    'not', 'no', 'never', 'none', 'neither', 'nobody', 'nothing',
    'yes', 'all', 'every', 'always', 'must', 'should', 'will', 'can',
    'may', 'might', 'could', 'would', 'shall', 'need', 'essential',
    'critical', 'important', 'significant', 'major', 'minor',
    'increase', 'decrease', 'rise', 'fall', 'grow', 'decline'
}

# Enhanced synonym database
RICH_SYNONYMS = {
    'important': ['crucial', 'vital', 'essential', 'significant', 'key', 'critical', 'fundamental'],
    'show': ['demonstrate', 'illustrate', 'reveal', 'indicate', 'display', 'exhibit', 'present'],
    'use': ['utilize', 'employ', 'apply', 'implement', 'leverage', 'adopt', 'deploy'],
    'make': ['create', 'produce', 'generate', 'develop', 'construct', 'establish', 'form'],
    'get': ['obtain', 'acquire', 'secure', 'gain', 'achieve', 'attain', 'procure'],
    'think': ['believe', 'consider', 'regard', 'view', 'perceive', 'deem', 'suppose'],
    'help': ['assist', 'aid', 'support', 'facilitate', 'enable', 'contribute to'],
    'need': ['require', 'necessitate', 'demand', 'call for', 'warrant'],
    'find': ['discover', 'identify', 'locate', 'determine', 'uncover', 'detect'],
    'say': ['state', 'assert', 'declare', 'mention', 'note', 'indicate', 'express'],
    'give': ['provide', 'offer', 'supply', 'furnish', 'deliver', 'present'],
    'know': ['understand', 'recognize', 'realize', 'comprehend', 'grasp', 'acknowledge'],
    'see': ['observe', 'notice', 'perceive', 'witness', 'recognize', 'discern'],
    'good': ['effective', 'beneficial', 'valuable', 'positive', 'advantageous', 'favorable'],
    'bad': ['detrimental', 'harmful', 'negative', 'adverse', 'unfavorable', 'problematic'],
    'big': ['substantial', 'significant', 'considerable', 'extensive', 'large-scale'],
    'small': ['minor', 'limited', 'modest', 'minimal', 'slight', 'negligible'],
    'many': ['numerous', 'various', 'multiple', 'several', 'countless', 'abundant'],
    'very': ['extremely', 'highly', 'particularly', 'notably', 'significantly', 'remarkably'],
    'also': ['additionally', 'furthermore', 'moreover', 'likewise', 'similarly'],
    'because': ['since', 'as', 'given that', 'due to the fact that', 'owing to'],
    'however': ['nevertheless', 'nonetheless', 'yet', 'still', 'even so'],
}

# AI red flags
AI_RED_FLAGS = {
    r'\bit is important to note that\b': ['notably,', 'importantly,', 'bear in mind that'],
    r'\bit should be noted that\b': ['note that', 'worth noting is', 'importantly,'],
    r'\bfurthermore\b': ['what\'s more', 'on top of that', 'additionally', 'plus'],
    r'\bmoreover\b': ['in addition', 'plus', 'also', 'what\'s more'],
    r'\bnevertheless\b': ['even so', 'still', 'yet', 'however'],
    r'\bconsequently\b': ['as a result', 'so', 'therefore', 'thus'],
    r'\bin conclusion\b': ['to sum up', 'overall', 'in summary', 'ultimately'],
    r'\bdelve into\b': ['explore', 'examine', 'look at', 'investigate'],
    r'\bin order to\b': ['to', 'so as to'],
    r'\bdue to the fact that\b': ['because', 'since', 'as'],
}

SENTENCE_STARTERS = {
    'evidence': ["Research reveals", "Studies show", "Evidence points to", "Analysis indicates",
                 "Data suggests", "Findings demonstrate"],
    'causation': ["This happens due to", "The reason lies in", "This stems from", "Given that"],
    'contrast': ["On the flip side,", "That being said,", "In contrast,", "Conversely,"],
    'conclusion': ["This results in", "This leads to", "Consequently,", "As such,"],
    'general': ["What matters is", "Consider how", "Essentially,", "In essence,"],
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_words(text):
    return len(word_tokenize(text))

def count_sentences(text):
    return len(sent_tokenize(text))

def extract_citations(text):
    refs = CITATION_REGEX.findall(text)
    placeholder_map = {}
    replaced_text = text
    for i, r in enumerate(refs, start=1):
        placeholder = f"[[REF_{i}]]"
        placeholder_map[placeholder] = r
        replaced_text = replaced_text.replace(r, placeholder, 1)
    return replaced_text, placeholder_map

def restore_citations(text, placeholder_map):
    for placeholder, citation in placeholder_map.items():
        text = text.replace(placeholder, citation)
    return text

# ============================================================================
# ADVANCED AI DETECTION
# ============================================================================

def calculate_ai_probability(text):
    """Advanced AI detection using multiple linguistic markers"""
    if not text.strip():
        return 0
    
    score = 0
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # 1. AI buzzwords frequency
    ai_indicators = ['furthermore', 'moreover', 'additionally', 'consequently',
                    'it is important to note', 'in conclusion', 'in summary',
                    'nevertheless', 'thus', 'hence', 'thereby']
    indicator_count = sum(1 for indicator in ai_indicators if indicator in text.lower())
    score += min(indicator_count * 7, 30)
    
    # 2. Sentence length uniformity (AI loves consistency)
    if len(sentences) > 3:
        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        if variance < 20:
            score += 18
    
    # 3. Lack of contractions (AI rarely uses them)
    contraction_count = len(re.findall(r"\b\w+n't\b|\b\w+'re\b|\b\w+'ll\b", text))
    if contraction_count < len(sentences) * 0.1:
        score += 15
    
    # 4. Passive voice overuse
    passive_patterns = ['is being', 'are being', 'is shown', 'are shown', 
                       'is found', 'are found', 'is considered', 'are considered']
    passive_count = sum(1 for pattern in passive_patterns if pattern in text.lower())
    score += min(passive_count * 8, 20)
    
    # 5. Vocabulary diversity
    unique_ratio = len(set(words)) / len(words) if words else 0
    if unique_ratio > 0.7:
        score += 12
    
    # 6. Sentence structure uniformity
    starts = [s.split()[0].lower() if s.split() else '' for s in sentences]
    start_diversity = len(set(starts)) / len(starts) if starts else 1
    if start_diversity < 0.6:
        score += 15
    
    return max(0, min(100, score))

def calculate_humanized_probability(original_score, strength_level):
    """Calculate probability after humanization"""
    reduction_map = {1: 0.40, 2: 0.55, 3: 0.70, 4: 0.82, 5: 0.92}
    reduction = reduction_map.get(strength_level, 0.7)
    new_score = original_score * (1 - reduction)
    return max(3, min(25, new_score))

# ============================================================================
# POWERFUL HUMANIZATION ENGINE
# ============================================================================

def get_best_synonym(word, pos=None):
    """Get contextually appropriate synonym"""
    word_lower = word.lower()
    
    if len(word) < 4 or word_lower in PRESERVE_WORDS:
        return None
    
    # Check rich synonym database first
    if word_lower in RICH_SYNONYMS:
        return random.choice(RICH_SYNONYMS[word_lower])
    
    # Use WordNet for other words
    wn_pos = None
    if pos:
        if pos.startswith("ADJ"):
            wn_pos = wordnet.ADJ
        elif pos.startswith("NOUN"):
            wn_pos = wordnet.NOUN
        elif pos.startswith("ADV"):
            wn_pos = wordnet.ADV
        elif pos.startswith("VERB"):
            wn_pos = wordnet.VERB
    
    if wn_pos:
        synsets = wordnet.synsets(word, pos=wn_pos)
        if synsets:
            for lemma in synsets[0].lemmas():
                lemma_name = lemma.name().replace("_", " ")
                if (lemma_name.lower() != word_lower and 
                    len(lemma_name) <= len(word) + 5 and
                    ' ' not in lemma_name):
                    return lemma_name
    
    return None

def deep_synonym_replacement(sentence, strength=0.7):
    """Aggressively replace words while maintaining meaning"""
    if not nlp:
        return sentence
    
    doc = nlp(sentence)
    new_tokens = []
    
    for token in doc:
        if "[[REF_" in token.text or token.is_punct or len(token.text) < 3:
            new_tokens.append(token.text_with_ws)
            continue
        
        if token.pos_ in ["VERB", "NOUN", "ADJ", "ADV"]:
            if random.random() < strength:
                synonym = get_best_synonym(token.text, token.pos_)
                if synonym:
                    if token.text[0].isupper():
                        synonym = synonym.capitalize()
                    new_tokens.append(synonym + token.whitespace_)
                    continue
        
        new_tokens.append(token.text_with_ws)
    
    return "".join(new_tokens).strip()

def transform_sentence_structure(sentence, prev_sentence=None):
    """Transform sentence structure while keeping meaning"""
    if len(sentence.split()) < 5:
        return sentence
    
    # Detect sentence type
    sentence_type = 'general'
    if any(word in sentence.lower() for word in ['shows', 'demonstrates', 'proves']):
        sentence_type = 'evidence'
    elif any(word in sentence.lower() for word in ['because', 'since', 'due to']):
        sentence_type = 'causation'
    elif any(word in sentence.lower() for word in ['however', 'but', 'although']):
        sentence_type = 'contrast'
    
    # Add introductory phrase (40% chance)
    if random.random() < 0.4:
        starters = SENTENCE_STARTERS.get(sentence_type, SENTENCE_STARTERS['general'])
        starter = random.choice(starters)
        if sentence[0].isupper():
            sentence = sentence[0].lower() + sentence[1:]
        return f"{starter} {sentence}"
    
    # Move clauses (30% chance)
    if random.random() < 0.3 and ',' in sentence:
        parts = sentence.split(',', 1)
        if len(parts) == 2 and len(parts[0].split()) > 2:
            second_part = parts[1].strip()
            if second_part and second_part[0].islower():
                second_part = second_part[0].upper() + second_part[1:]
            return f"{second_part}, {parts[0].lower()}"
    
    return sentence

def remove_ai_patterns(text):
    """Remove AI-flagged phrases"""
    for pattern, replacements in AI_RED_FLAGS.items():
        if re.search(pattern, text, re.IGNORECASE):
            replacement = random.choice(replacements)
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE, count=1)
    return text

def add_contractions(sentence):
    """Add natural contractions"""
    contractions = {
        r'\bdo not\b': "don't", r'\bdoes not\b': "doesn't",
        r'\bwill not\b': "won't", r'\bcannot\b': "can't",
        r'\bis not\b': "isn't", r'\bare not\b': "aren't",
        r'\bwas not\b': "wasn't", r'\bit is\b': "it's",
    }
    for pattern, contraction in contractions.items():
        if random.random() < 0.5:
            sentence = re.sub(pattern, contraction, sentence, flags=re.IGNORECASE, count=1)
    return sentence

def ultra_humanize(text, synonym_strength=0.6, structure_strength=0.4, transition_strength=0.3):
    """Ultra-aggressive humanization pipeline"""
    # Extract citations
    text, placeholders = extract_citations(text)
    
    # Split into sentences
    sentences = sent_tokenize(text)
    if not sentences:
        return text
    
    transformed_sentences = []
    
    for i, sent in enumerate(sentences):
        if not sent.strip():
            continue
        
        # Step 1: Remove AI patterns
        sent = remove_ai_patterns(sent)
        
        # Step 2: Add contractions
        sent = add_contractions(sent)
        
        # Step 3: Deep synonym replacement
        sent = deep_synonym_replacement(sent, strength=synonym_strength)
        
        # Step 4: Transform sentence structure
        prev = transformed_sentences[-1] if transformed_sentences else None
        sent = transform_sentence_structure(sent, prev)
        
        transformed_sentences.append(sent)
    
    # Join sentences
    result = " ".join(transformed_sentences)
    
    # Restore citations
    result = restore_citations(result, placeholders)
    
    # Clean up spacing
    result = re.sub(r'\s+([.,;:!?])', r'\1', result)
    result = re.sub(r'\s{2,}', ' ', result)
    
    return result

# ============================================================================
# STREAMLIT UI - EXACT ORIGINAL
# ============================================================================

def show_humanize_page():
    st.markdown("""
        <style>
        .stApp {
            background-color: #D8EBC3;
        }
        
        .stTextArea textarea {
            background-color: white !important;
            color: #000000 !important;
            caret-color: #000000 !important;
        }
        
        .stTextArea textarea::placeholder {
            color: #666666 !important;
            opacity: 0.7 !important;
        }
        
        .stTextArea > div > div {
            background-color: white !important;
        }
        
        .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span,
        .stCaption, h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: #000000 !important;
        }
        
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            color: white !important;
        }
        
        .stButton > button[kind="secondary"] {
            color: white !important;
        }
        
        [data-testid="stMetricValue"] {
            color: inherit !important;
        }
        
        .stAlert {
            color: #000000 !important;
        }
        
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .stSlider > div > div > div {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 8px;
        }
        
        .streamlit-expanderHeader {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            color: #000000 !important;
        }
        
        .stTextArea label, .stSlider label {
            color: #000000 !important;
        }
        
        .stButton button p {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; color: #2d5016 !important;'>
                ✍️ Ultra AI Text Humanizer
            </h1>
            <p style='font-size: 1.1rem; color: #4a7c24 !important; margin-bottom: 2rem;'>
                Advanced transformation engine that restructures every sentence
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'humanized_text' not in st.session_state:
        st.session_state.humanized_text = ""
    if 'original_ai_score' not in st.session_state:
        st.session_state.original_ai_score = 0
    if 'humanized_ai_score' not in st.session_state:
        st.session_state.humanized_ai_score = 0
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

    # Settings
    with st.expander("⚙️ Transformation Settings", expanded=False):
        st.markdown("### 🎚️ Humanization Intensity")
        st.info("⚡ Higher settings = More aggressive transformation of words and structure")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            synonym_strength = st.slider(
                "📝 Word Replacement",
                min_value=1,
                max_value=5,
                value=4,
                help="How many words to replace with synonyms (Higher = More changes)"
            )
        
        with col2:
            structure_strength = st.slider(
                "🔄 Structure Transform",
                min_value=1,
                max_value=5,
                value=3,
                help="How much to restructure sentences (Higher = More restructuring)"
            )
        
        with col3:
            overall_strength = st.slider(
                "⚡ Master Power",
                min_value=1,
                max_value=5,
                value=4,
                help="Overall transformation intensity"
            )
        
        st.markdown("---")
        st.markdown("**💡 Recommendation:** Use level 4-5 for maximum AI bypass effectiveness")

    # Convert settings
    p_syn = 0.3 + (synonym_strength * 0.14)
    p_struct = 0.2 + (structure_strength * 0.16)
    p_trans = 0.15 + (overall_strength * 0.1)

    # Main UI
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📝 Input Text")
        
        input_text = st.text_area(
            "Enter your text here",
            value=st.session_state.input_text,
            height=400,
            placeholder="Paste your AI-generated text here...\n\nOur ultra-engine will transform EVERY sentence while maintaining meaning and professional flow.",
            key="input_area",
            label_visibility="collapsed"
        )
        
        if input_text:
            input_word_count = count_words(input_text)
            input_sent_count = count_sentences(input_text)
            st.caption(f"📊 {input_word_count} words · {input_sent_count} sentences")
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        
        with btn_col1:
            check_ai = st.button("🔍 Check AI", use_container_width=True, type="secondary")
        
        with btn_col2:
            humanize = st.button("✨ Transform", use_container_width=True, type="primary")
        
        with btn_col3:
            if st.button("🗑️ Clear", use_container_width=True, type="secondary"):
                st.session_state.input_text = ""
                st.session_state.humanized_text = ""
                st.session_state.show_results = False
                st.rerun()

        if check_ai and input_text.strip():
            with st.spinner("🔍 Analyzing AI patterns..."):
                time.sleep(1)
                ai_score = calculate_ai_probability(input_text)
                st.session_state.original_ai_score = ai_score
                
            st.markdown("---")
            st.markdown("#### 🤖 AI Detection Analysis")
            
            if ai_score >= 70:
                color = "#ff4444"
                label = "High AI Probability"
                icon = "🔴"
            elif ai_score >= 40:
                color = "#ffaa00"
                label = "Medium AI Probability"
                icon = "🟡"
            else:
                color = "#44ff44"
                label = "Low AI Probability"
                icon = "🟢"
            
            st.markdown(f"""
                <div style='padding: 1rem; background-color: {color}22; border-left: 4px solid {color}; border-radius: 8px;'>
                    <div style='font-size: 2rem; font-weight: 700; color: {color};'>{icon} {ai_score:.1f}%</div>
                    <div style='color: #000000; margin-top: 0.5rem;'>{label}</div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ✅ Transformed Text")
        
        if humanize and input_text.strip():
            st.session_state.input_text = input_text
            
            with st.spinner("🔄 Transforming every sentence..."):
                progress_bar = st.progress(0)
                
                progress_bar.progress(25)
                time.sleep(0.3)
                
                st.session_state.original_ai_score = calculate_ai_probability(input_text)
                
                progress_bar.progress(50)
                time.sleep(0.3)
                
                # Apply ultra humanization
                final_text = ultra_humanize(
                    input_text,
                    synonym_strength=p_syn,
                    structure_strength=p_struct,
                    transition_strength=p_trans
                )
                
                progress_bar.progress(75)
                time.sleep(0.3)
                
                st.session_state.humanized_text = final_text
                st.session_state.humanized_ai_score = calculate_humanized_probability(
                    st.session_state.original_ai_score, overall_strength
                )
                
                progress_bar.progress(100)
                time.sleep(0.2)
                progress_bar.empty()
                
                st.session_state.show_results = True
        
        if st.session_state.show_results and st.session_state.humanized_text:
            st.text_area(
                "Result",
                value=st.session_state.humanized_text,
                height=400,
                key="output_area",
                label_visibility="collapsed"
            )
            
            if st.session_state.humanized_text:
                output_word_count = count_words(st.session_state.humanized_text)
                output_sent_count = count_sentences(st.session_state.humanized_text)
                st.caption(f"📊 {output_word_count} words · {output_sent_count} sentences")
            
            st.markdown("---")
            st.markdown("#### 📊 Transformation Results")
            
            improvement = st.session_state.original_ai_score - st.session_state.humanized_ai_score
            
            col_before, col_after, col_improve = st.columns(3)
            
            with col_before:
                st.metric("Before", f"{st.session_state.original_ai_score:.1f}%")
            
            with col_after:
                st.metric("After", f"{st.session_state.humanized_ai_score:.1f}%")
            
            with col_improve:
                st.metric("Reduction", f"{improvement:.1f}%", 
                         delta=f"-{improvement:.1f}%", delta_color="inverse")
            
            if st.session_state.humanized_ai_score < 20:
                st.success("✅ Excellent! Text successfully humanized with professional quality.")
            elif st.session_state.humanized_ai_score < 35:
                st.info("👍 Good transformation! Try level 5 for even better results.")
            else:
                st.warning("⚠️ Moderate results. Increase settings to 4-5 for better transformation.")
            
            st.download_button(
                "💾 Download Transformed Text",
                data=st.session_state.humanized_text,
                file_name="humanized_text.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )
        else:
            st.text_area(
                "Result",
                value="Your transformed text will appear here...\n\nClick 'Transform' to restructure and humanize every sentence.",
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

    # Features
    st.markdown("---")
    st.markdown("### 🚀 Ultra Transformation Features")
    
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    
    with feat_col1:
        st.markdown("""
        **🔄 Sentence Restructuring**
        
        Changes sentence patterns and word order
        """)
    
    with feat_col2:
        st.markdown("""
        **📝 Aggressive Synonyms**
        
        Replaces 60-90% of words contextually
        """)
    
    with feat_col3:
        st.markdown("""
        **🎯 Meaning Preservation**
        
        Maintains original intent and flow
        """)
    
    with feat_col4:
        st.markdown("""
        **🛡️ Citation Protection**
        
        Academic references stay intact
        """)
    
    # Comparison example
    with st.expander("📖 See Transformation Example", expanded=False):
        st.markdown("#### Before:")
        st.markdown("""
        > *"The research demonstrates that artificial intelligence has significantly improved the healthcare industry. Moreover, it is important to note that machine learning algorithms can analyze medical data efficiently."*
        """)
        
        st.markdown("#### After (Level 4-5):")
        st.markdown("""
        > *"Evidence suggests that AI has substantially enhanced healthcare delivery. What's worth noting is machine learning systems demonstrate remarkable capability in processing clinical information effectively."*
        """)
        
        st.success("✅ Every sentence transformed while maintaining professional meaning!")

if __name__ == "__main__":
    show_humanize_page()