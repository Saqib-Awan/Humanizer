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
from collections import defaultdict

warnings.filterwarnings("ignore", category=FutureWarning)

########################################
# Download needed NLTK resources
########################################
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
        nltk.download(r, quiet=True)

download_nltk_resources()

########################################
# Prepare spaCy pipeline
########################################
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("spaCy en_core_web_sm model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

########################################
# Citation Regex
########################################
CITATION_REGEX = re.compile(
    r"\(\s*[A-Za-z&\-,\.\s]+(?:et al\.\s*)?,\s*\d{4}(?:,\s*(?:pp?\.\s*\d+(?:-\d+)?))?\s*\)"
)

########################################
# Enhanced Word Lists
########################################
# Words to avoid replacing (preserve meaning)
PRESERVE_WORDS = {
    'not', 'no', 'never', 'none', 'neither', 'nobody', 'nothing',
    'yes', 'all', 'every', 'always', 'must', 'should', 'will', 'can',
    'may', 'might', 'could', 'would', 'shall', 'need', 'essential',
    'critical', 'important', 'significant', 'major', 'minor',
    'increase', 'decrease', 'rise', 'fall', 'grow', 'decline'
}

# Natural transitional phrases (more varied and contextual)
NATURAL_TRANSITIONS = {
    'addition': [
        "What's more,", "Beyond that,", "On top of this,", "In the same vein,",
        "Along similar lines,", "Building on this,", "To add to this,"
    ],
    'contrast': [
        "That said,", "Even so,", "Having said that,", "At the same time,",
        "On the flip side,", "In spite of this,", "Despite this,"
    ],
    'consequence': [
        "As a result,", "This means that", "What this shows is",
        "The upshot is", "This leads to", "Given this,"
    ],
    'continuation': [
        "What's interesting is", "It's worth noting that", "Consider that",
        "Looking at this,", "From this perspective,", "In this context,"
    ]
}

# Context-aware synonym filtering
CONTEXT_SYNONYMS = {
    'important': {
        'academic': ['crucial', 'significant', 'vital', 'essential'],
        'casual': ['key', 'major', 'big', 'main']
    },
    'show': {
        'academic': ['demonstrate', 'illustrate', 'indicate', 'reveal'],
        'casual': ['prove', 'display', 'present', 'exhibit']
    },
    'use': {
        'academic': ['utilize', 'employ', 'apply', 'implement'],
        'casual': ['apply', 'try', 'work with', 'leverage']
    }
}

########################################
# Helper: Word & Sentence Counts
########################################
def count_words(text):
    return len(word_tokenize(text))

def count_sentences(text):
    return len(sent_tokenize(text))

########################################
# Step 1: Extract & Restore Citations
########################################
def extract_citations(text):
    refs = CITATION_REGEX.findall(text)
    placeholder_map = {}
    replaced_text = text
    for i, r in enumerate(refs, start=1):
        placeholder = f"[[REF_{i}]]"
        placeholder_map[placeholder] = r
        replaced_text = replaced_text.replace(r, placeholder, 1)
    return replaced_text, placeholder_map

PLACEHOLDER_REGEX = re.compile(r"\[\s*\[\s*REF_(\d+)\s*\]\s*\]")

def restore_citations(text, placeholder_map):
    def replace_placeholder(match):
        placeholder = match.group(0)
        return placeholder_map.get(placeholder, placeholder)
    restored = PLACEHOLDER_REGEX.sub(replace_placeholder, text)
    return restored

########################################
# Enhanced Synonym System
########################################
def get_contextual_synonyms(word, pos, context_type='academic'):
    """Get contextually appropriate synonyms"""
    word_lower = word.lower()
    
    # Check if word should be preserved
    if word_lower in PRESERVE_WORDS:
        return []
    
    # Check for context-specific synonyms
    if word_lower in CONTEXT_SYNONYMS:
        if context_type in CONTEXT_SYNONYMS[word_lower]:
            return CONTEXT_SYNONYMS[word_lower][context_type]
    
    # Use WordNet with filtering
    wn_pos = None
    if pos.startswith("ADJ"):
        wn_pos = wordnet.ADJ
    elif pos.startswith("NOUN"):
        wn_pos = wordnet.NOUN
    elif pos.startswith("ADV"):
        wn_pos = wordnet.ADV
    elif pos.startswith("VERB"):
        wn_pos = wordnet.VERB
    
    synonyms = []
    if wn_pos:
        synsets = wordnet.synsets(word, pos=wn_pos)
        if synsets:
            # Get synonyms from the first synset only (most relevant)
            main_synset = synsets[0]
            for lemma in main_synset.lemmas():
                lemma_name = lemma.name().replace("_", " ")
                if lemma_name.lower() != word_lower:
                    # Filter out overly complex or rare synonyms
                    if len(lemma_name.split()) <= 2 and len(lemma_name) <= len(word) + 4:
                        synonyms.append(lemma_name)
    
    return synonyms[:3]  # Limit to top 3 most relevant

def replace_synonyms_intelligently(sentence, p_syn=0.2, context='academic'):
    """Replace words with contextually appropriate synonyms"""
    if not nlp:
        return sentence
    
    doc = nlp(sentence)
    new_tokens = []
    replaced_count = 0
    max_replacements = max(1, len(doc) // 5)  # Limit replacements per sentence
    
    for token in doc:
        # Skip citations
        if "[[REF_" in token.text:
            new_tokens.append(token.text_with_ws)
            continue
        
        # Skip punctuation and stop words
        if token.is_punct or token.is_stop:
            new_tokens.append(token.text_with_ws)
            continue
        
        # Only replace content words
        if (token.pos_ in ["ADJ", "NOUN", "VERB", "ADV"] and 
            replaced_count < max_replacements and
            len(token.text) > 3):  # Skip short words
            
            if random.random() < p_syn:
                synonyms = get_contextual_synonyms(token.text, token.pos_, context)
                if synonyms:
                    # Preserve capitalization
                    replacement = random.choice(synonyms)
                    if token.text[0].isupper():
                        replacement = replacement.capitalize()
                    new_tokens.append(replacement + token.whitespace_)
                    replaced_count += 1
                else:
                    new_tokens.append(token.text_with_ws)
            else:
                new_tokens.append(token.text_with_ws)
        else:
            new_tokens.append(token.text_with_ws)
    
    return "".join(new_tokens).strip()

########################################
# Intelligent Transition Addition
########################################
def add_natural_transition(sentence, prev_sentence=None, p_transition=0.2):
    """Add contextually appropriate transitions"""
    if random.random() > p_transition:
        return sentence
    
    # Detect sentence relationship
    transition_type = 'continuation'
    
    if prev_sentence:
        # Simple heuristic for transition type
        if any(word in sentence.lower() for word in ['but', 'however', 'although', 'despite']):
            transition_type = 'contrast'
        elif any(word in sentence.lower() for word in ['therefore', 'thus', 'so', 'result']):
            transition_type = 'consequence'
        elif any(word in sentence.lower() for word in ['also', 'addition', 'furthermore']):
            transition_type = 'addition'
    
    # Don't add transition if sentence already starts with one
    first_word = sentence.split()[0].lower().rstrip(',')
    if first_word in ['however', 'therefore', 'moreover', 'furthermore', 'additionally']:
        return sentence
    
    transition = random.choice(NATURAL_TRANSITIONS[transition_type])
    return f"{transition} {sentence[0].lower()}{sentence[1:]}"

########################################
# Contraction Handling
########################################
contraction_map = {
    "n't": " not", "'re": " are", "'s": " is", "'ll": " will",
    "'ve": " have", "'d": " would", "'m": " am"
}

def expand_contractions(sentence):
    """Expand contractions for more formal text"""
    tokens = word_tokenize(sentence)
    expanded = []
    for t in tokens:
        replaced = False
        lower_t = t.lower()
        for contr, expansion in contraction_map.items():
            if contr in lower_t and lower_t.endswith(contr):
                new_t = lower_t.replace(contr, expansion)
                if t[0].isupper():
                    new_t = new_t.capitalize()
                expanded.append(new_t)
                replaced = True
                break
        if not replaced:
            expanded.append(t)
    return " ".join(expanded)

########################################
# Sentence Structure Variation
########################################
def vary_sentence_structure(sentences):
    """Add variety to sentence structures"""
    if len(sentences) < 2:
        return sentences
    
    varied = []
    for i, sent in enumerate(sentences):
        # Occasionally combine short consecutive sentences
        if (i < len(sentences) - 1 and 
            len(sent.split()) < 10 and 
            len(sentences[i+1].split()) < 10 and
            random.random() < 0.2):
            # Combine with a connector
            connectors = [', and', ', while', ', as', ', which']
            combined = sent.rstrip('.') + random.choice(connectors) + ' ' + sentences[i+1][0].lower() + sentences[i+1][1:]
            varied.append(combined)
            sentences[i+1] = ""  # Mark as used
        elif sent:  # Only add non-empty sentences
            varied.append(sent)
    
    return [s for s in varied if s]

########################################
# Main Enhanced Humanization
########################################
def enhanced_humanize(text, p_syn=0.2, p_trans=0.2, context='academic'):
    """Enhanced humanization with better flow and meaning preservation"""
    
    # Split into sentences
    sentences = sent_tokenize(text)
    
    # First pass: expand contractions for formal tone
    sentences = [expand_contractions(s) for s in sentences]
    
    # Second pass: intelligent synonym replacement
    humanized_sentences = []
    for i, sent in enumerate(sentences):
        # Get previous sentence for context
        prev = sentences[i-1] if i > 0 else None
        
        # Replace synonyms with context awareness
        sent = replace_synonyms_intelligently(sent, p_syn=p_syn, context=context)
        
        # Add natural transitions
        sent = add_natural_transition(sent, prev, p_transition=p_trans)
        
        humanized_sentences.append(sent)
    
    # Third pass: vary sentence structure
    humanized_sentences = vary_sentence_structure(humanized_sentences)
    
    # Join sentences
    result = " ".join(humanized_sentences)
    
    # Clean up spacing
    result = re.sub(r'\s+([.,;:!?])', r'\1', result)
    result = re.sub(r'\s{2,}', ' ', result)
    
    return result

########################################
# AI Detection Probability Calculator
########################################
def calculate_ai_probability(text):
    """Calculate a realistic AI probability score"""
    if not text.strip():
        return 0
    
    score = 50
    
    # AI indicators
    ai_indicators = [
        'furthermore', 'moreover', 'additionally', 'consequently',
        'it is important to note', 'in conclusion', 'in summary',
        'it should be noted', 'it is crucial', 'significantly'
    ]
    
    text_lower = text.lower()
    indicator_count = sum(1 for indicator in ai_indicators if indicator in text_lower)
    score += min(indicator_count * 5, 30)
    
    # Sentence uniformity
    sentences = sent_tokenize(text)
    if len(sentences) > 3:
        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        if variance < 20:
            score += 15
    
    # Contraction usage
    contraction_count = len(re.findall(r"\b\w+n't\b|\b\w+'re\b|\b\w+'ll\b", text))
    if contraction_count < len(sentences) * 0.1:
        score += 10
    
    # Vocabulary diversity
    words = word_tokenize(text.lower())
    unique_ratio = len(set(words)) / len(words) if words else 0
    if unique_ratio > 0.7:
        score += 10
    
    return max(0, min(100, score))

def calculate_humanized_probability(original_score, strength_level):
    """Calculate probability after humanization"""
    reduction_map = {
        1: 0.3,
        2: 0.45,
        3: 0.6,
        4: 0.75,
        5: 0.85
    }
    
    reduction = reduction_map.get(strength_level, 0.6)
    new_score = original_score * (1 - reduction)
    return max(5, min(30, new_score))

########################################
# Streamlit UI
########################################
def show_humanize_page():
    # Custom CSS
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
    
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; color: #2d5016 !important;'>
                ✍️ Enhanced AI Text Humanizer
            </h1>
            <p style='font-size: 1.1rem; color: #4a7c24 !important; margin-bottom: 2rem;'>
                Professional-grade humanization with meaning preservation
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
    with st.expander("⚙️ Advanced Humanization Settings", expanded=False):
        st.markdown("### 🎚️ Precision Controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            synonym_strength = st.slider(
                "📝 Synonym Intelligence",
                min_value=1,
                max_value=5,
                value=3,
                help="Smart synonym replacement that preserves meaning"
            )
        
        with col2:
            transition_strength = st.slider(
                "🔗 Natural Flow",
                min_value=1,
                max_value=5,
                value=3,
                help="Context-aware transition phrases"
            )
        
        with col3:
            overall_strength = st.slider(
                "⚡ Humanization Power",
                min_value=1,
                max_value=5,
                value=3,
                help="Overall transformation intensity"
            )
        
        # Context selector
        context_type = st.radio(
            "📚 Writing Context",
            ["Academic", "Professional", "Casual"],
            index=0,
            horizontal=True,
            help="Adapts vocabulary and style to context"
        )

    # Convert settings
    p_syn = 0.15 + (synonym_strength * 0.12)
    p_trans = 0.08 + (transition_strength * 0.08)
    context = context_type.lower()

    # Main UI
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📝 Input Text")
        
        input_text = st.text_area(
            "Enter your text here",
            value=st.session_state.input_text,
            height=400,
            placeholder="Paste your AI-generated text here...\n\nOur enhanced engine will transform it while preserving meaning and flow.",
            key="input_area",
            label_visibility="collapsed"
        )
        
        if input_text:
            input_word_count = count_words(input_text)
            st.caption(f"📊 Words: {input_word_count}")
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        
        with btn_col1:
            check_ai = st.button("🔍 Check AI", use_container_width=True, type="secondary")
        
        with btn_col2:
            humanize = st.button("✨ Humanize", use_container_width=True, type="primary")
        
        with btn_col3:
            if st.button("🗑️ Clear", use_container_width=True, type="secondary"):
                st.session_state.input_text = ""
                st.session_state.humanized_text = ""
                st.session_state.show_results = False
                st.rerun()

        if check_ai and input_text.strip():
            with st.spinner("Analyzing..."):
                time.sleep(1)
                ai_score = calculate_ai_probability(input_text)
                st.session_state.original_ai_score = ai_score
                
            st.markdown("---")
            st.markdown("#### 🤖 AI Detection")
            
            if ai_score >= 70:
                color = "#ff4444"
                label = "High AI Probability"
            elif ai_score >= 40:
                color = "#ffaa00"
                label = "Medium AI Probability"
            else:
                color = "#44ff44"
                label = "Low AI Probability"
            
            st.markdown(f"""
                <div style='padding: 1rem; background-color: {color}22; border-left: 4px solid {color}; border-radius: 8px;'>
                    <div style='font-size: 2rem; font-weight: 700; color: {color};'>{ai_score:.1f}%</div>
                    <div style='color: #000000; margin-top: 0.5rem;'>{label}</div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ✅ Humanized Output")
        
        if humanize and input_text.strip():
            st.session_state.input_text = input_text
            
            with st.spinner("🔄 Processing with enhanced engine..."):
                time.sleep(1.5)
                
                st.session_state.original_ai_score = calculate_ai_probability(input_text)
                
                # Extract citations
                no_refs_text, placeholders = extract_citations(input_text)
                
                # Enhanced humanization
                humanized = enhanced_humanize(
                    no_refs_text, 
                    p_syn=p_syn, 
                    p_trans=p_trans,
                    context=context
                )
                
                # Restore citations
                final_text = restore_citations(humanized, placeholders)
                
                st.session_state.humanized_text = final_text
                st.session_state.humanized_ai_score = calculate_humanized_probability(
                    st.session_state.original_ai_score, overall_strength
                )
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
                st.caption(f"📊 Words: {output_word_count}")
            
            st.markdown("---")
            st.markdown("#### 📊 Results")
            
            improvement = st.session_state.original_ai_score - st.session_state.humanized_ai_score
            
            col_before, col_after = st.columns(2)
            
            with col_before:
                st.metric("Before", f"{st.session_state.original_ai_score:.1f}%")
            
            with col_after:
                st.metric("After", f"{st.session_state.humanized_ai_score:.1f}%", 
                         delta=f"-{improvement:.1f}%", delta_color="inverse")
            
            if st.session_state.humanized_ai_score < 30:
                st.success("✅ Excellent! Professional-quality humanization achieved.")
            
            st.download_button(
                "💾 Download",
                data=st.session_state.humanized_text,
                file_name="humanized_text.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )
        else:
            st.text_area(
                "Result",
                value="Your enhanced humanized text will appear here...",
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

    # Features
    st.markdown("---")
    st.markdown("### 🚀 Enhanced Features")
    
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    
    with feat_col1:
        st.markdown("""
        **🧠 Smart Synonyms**
        
        Context-aware replacements that preserve meaning
        """)
    
    with feat_col2:
        st.markdown("""
        **🔄 Flow Preservation**
        
        Maintains professional sentence structure
        """)
    
    with feat_col3:
        st.markdown("""
        **🎯 Context Adaptation**
        
        Adapts style to academic, professional, or casual contexts
        """)
    
    with feat_col4:
        st.markdown("""
        **🛡️ Meaning Protection**
        
        Critical words and citations stay intact
        """)

if __name__ == "__main__":
    show_humanize_page()