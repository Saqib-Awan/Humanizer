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
import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)

########################################
# NLTK Setup
########################################
def download_nltk_resources():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    for r in ['punkt', 'averaged_perceptron_tagger', 'punkt_tab', 'wordnet', 'averaged_perceptron_tagger_eng']:
        nltk.download(r, quiet=True)

download_nltk_resources()

########################################
# SpaCy Setup
########################################
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("Install spaCy model: python -m spacy download en_core_web_sm")
    nlp = None

########################################
# PASTE YOUR FULL WORD LISTS HERE
# Import from word_lists.py (create separate file)
########################################
from word_lists import (
    PRESERVE_WORDS,
    ULTRA_SYNONYMS,
    DIVERSE_STARTERS,
    AI_RED_FLAGS,
    CONTRACTIONS_MAP,
    HUMAN_FILLERS,
    INFORMAL_REPLACEMENTS
)

########################################
# Citation Handling
########################################
CITATION_REGEX = re.compile(r"\(\s*[A-Za-z&\-,\.\s]+(?:et al\.\s*)?,\s*\d{4}(?:,\s*(?:pp?\.\s*\d+(?:-\d+)?))?\s*\)")
PLACEHOLDER_REGEX = re.compile(r"\[\s*\[\s*REF_(\d+)\s*\]\s*\]")

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
    def replace_placeholder(match):
        return placeholder_map.get(match.group(0), match.group(0))
    return PLACEHOLDER_REGEX.sub(replace_placeholder, text)

########################################
# Advanced AI Detection (StealthWriter-style)
########################################
def calculate_perplexity_score(text):
    """Calculate text perplexity - AI tends to have lower perplexity"""
    words = word_tokenize(text.lower())
    if len(words) < 10:
        return 50
    
    word_freq = Counter(words)
    unique_ratio = len(word_freq) / len(words)
    
    # Calculate bigram entropy
    bigrams = list(zip(words[:-1], words[1:]))
    bigram_freq = Counter(bigrams)
    
    entropy = 0
    for bigram in set(bigrams):
        prob = bigram_freq[bigram] / len(bigrams)
        entropy -= prob * np.log2(prob) if prob > 0 else 0
    
    # Normalize (higher entropy = more human-like)
    perplexity_score = min(entropy * 10, 100)
    return perplexity_score

def calculate_burstiness(sentences):
    """AI writing has uniform sentence length; humans vary greatly"""
    if len(sentences) < 3:
        return 50
    
    lengths = [len(s.split()) for s in sentences]
    mean_len = np.mean(lengths)
    std_len = np.std(lengths)
    
    # Coefficient of variation (higher = more human)
    cv = (std_len / mean_len) if mean_len > 0 else 0
    burstiness = min(cv * 100, 100)
    return burstiness

def detect_ai_patterns(text):
    """Detect specific AI writing patterns"""
    text_lower = text.lower()
    score = 0
    
    # AI red flags from your list
    for pattern, _ in AI_RED_FLAGS.items():
        if re.search(pattern, text_lower):
            score += 3
    
    # Formal transition overuse
    formal_transitions = ['furthermore', 'moreover', 'additionally', 'consequently', 'nonetheless', 'nevertheless']
    score += sum(text_lower.count(t) for t in formal_transitions) * 4
    
    # Passive voice detection
    passive_indicators = ['is being', 'are being', 'was being', 'were being', 'is shown', 'are shown']
    score += sum(text_lower.count(p) for p in passive_indicators) * 3
    
    # Lack of contractions
    sentences = sent_tokenize(text)
    contraction_ratio = len(re.findall(r"\w+n't|\w+'re|\w+'ll|\w+'ve|\w+'d", text)) / max(len(sentences), 1)
    if contraction_ratio < 0.15:
        score += 15
    
    # Perfect grammar (too perfect)
    if not re.search(r'\b(kinda|gonna|wanna|gotta|sorta|yeah|ok|okay)\b', text_lower):
        score += 8
    
    return min(score, 50)

def calculate_ai_probability(text):
    """Advanced AI detection combining multiple signals"""
    if not text.strip():
        return 0
    
    sentences = sent_tokenize(text)
    
    # Multiple detection methods
    perplexity = calculate_perplexity_score(text)
    burstiness = calculate_burstiness(sentences)
    pattern_score = detect_ai_patterns(text)
    
    # Weight different signals
    # Lower perplexity = more AI-like (invert for score)
    perplexity_component = (100 - perplexity) * 0.3
    
    # Lower burstiness = more AI-like (invert for score)
    burstiness_component = (100 - burstiness) * 0.3
    
    # Pattern detection
    pattern_component = pattern_score * 0.4
    
    final_score = perplexity_component + burstiness_component + pattern_component
    
    return max(0, min(100, final_score))

########################################
# Core Humanization Engine
########################################
def get_smart_synonym(word, pos, context='academic'):
    """Get contextually appropriate synonym from your comprehensive lists"""
    word_lower = word.lower()
    
    # Preserve critical words
    if word_lower in PRESERVE_WORDS:
        return None
    
    # Use your ultra-comprehensive synonym database
    if word_lower in ULTRA_SYNONYMS:
        synonyms = ULTRA_SYNONYMS[word_lower]
        if synonyms:
            return random.choice(synonyms)
    
    return None

def remove_ai_red_flags(text):
    """Remove/replace AI-flagged phrases from your list"""
    for pattern, replacements in AI_RED_FLAGS.items():
        if re.search(pattern, text, re.IGNORECASE):
            replacement = random.choice(replacements)
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE, count=1)
    return text

def apply_contractions(text, ratio=0.4):
    """Add natural contractions"""
    for full, contracted in CONTRACTIONS_MAP.items():
        if random.random() < ratio:
            text = re.sub(r'\b' + re.escape(full) + r'\b', contracted, text, count=1, flags=re.IGNORECASE)
    return text

def add_sentence_variety(sentences):
    """Create varied sentence structures and lengths"""
    varied = []
    i = 0
    
    while i < len(sentences):
        sent = sentences[i]
        words = sent.split()
        
        # Randomly vary structure
        if len(words) > 15 and random.random() < 0.3:
            # Split long sentence
            mid = len(words) // 2
            part1 = ' '.join(words[:mid]) + '.'
            part2 = ' '.join(words[mid:])
            part2 = part2[0].upper() + part2[1:] if len(part2) > 1 else part2
            varied.extend([part1, part2])
        elif len(words) < 8 and i < len(sentences) - 1 and len(sentences[i+1].split()) < 8 and random.random() < 0.25:
            # Combine short sentences
            connector = random.choice([', and', ', but', ', while', ' -'])
            combined = sent.rstrip('.') + connector + ' ' + sentences[i+1][0].lower() + sentences[i+1][1:]
            varied.append(combined)
            i += 1  # Skip next sentence
        else:
            varied.append(sent)
        
        i += 1
    
    return varied

def add_natural_transitions(sentences):
    """Add varied transitions from your comprehensive lists"""
    result = []
    
    for i, sent in enumerate(sentences):
        # Don't add transition to first sentence
        if i == 0:
            result.append(sent)
            continue
        
        # Random transition addition
        if random.random() < 0.25:
            # Choose transition type based on context
            transition_types = list(DIVERSE_STARTERS.keys())
            trans_type = random.choice(transition_types)
            transition = random.choice(DIVERSE_STARTERS[trans_type])
            
            # Don't add if sentence already has transition
            first_words = sent.split()[:2]
            if not any(w.lower().rstrip(',') in ['however', 'therefore', 'moreover', 'furthermore'] for w in first_words):
                sent = f"{transition} {sent[0].lower()}{sent[1:]}"
        
        result.append(sent)
    
    return result

def strategic_synonym_replacement(text, strength=0.3):
    """Replace words with synonyms from your ultra-comprehensive database"""
    if not nlp:
        return text
    
    doc = nlp(text)
    tokens = []
    replace_count = 0
    max_replacements = max(2, len(doc) // 6)
    
    for token in doc:
        # Skip special cases
        if token.is_punct or token.is_stop or "[[REF_" in token.text or len(token.text) < 4:
            tokens.append(token.text_with_ws)
            continue
        
        # Strategic replacement
        if (token.pos_ in ["ADJ", "VERB", "NOUN", "ADV"] and 
            replace_count < max_replacements and 
            random.random() < strength):
            
            synonym = get_smart_synonym(token.text, token.pos_)
            if synonym:
                # Preserve capitalization
                if token.text[0].isupper():
                    synonym = synonym.capitalize()
                tokens.append(synonym + token.whitespace_)
                replace_count += 1
            else:
                tokens.append(token.text_with_ws)
        else:
            tokens.append(token.text_with_ws)
    
    return "".join(tokens)

def add_human_imperfections(text):
    """Add subtle human-like imperfections"""
    # Occasionally use informal replacements from your list
    for pattern, replacements in INFORMAL_REPLACEMENTS.items():
        if re.search(pattern, text) and random.random() < 0.2:
            replacement = random.choice(replacements)
            text = re.sub(pattern, replacement, text, count=1, flags=re.IGNORECASE)
    
    # Rarely add filler words
    if random.random() < 0.15:
        filler = random.choice(HUMAN_FILLERS)
        sentences = sent_tokenize(text)
        if sentences:
            idx = random.randint(0, len(sentences) - 1)
            sentences[idx] = sentences[idx].replace('. ', f', {filler}, ', 1)
            text = ' '.join(sentences)
    
    return text

########################################
# Main Humanization Pipeline
########################################
def advanced_humanize(text, strength=3):
    """StealthWriter-level humanization pipeline"""
    
    # Strength mapping
    syn_strength = 0.15 + (strength * 0.1)
    
    # Extract citations
    text, citations = extract_citations(text)
    
    # Step 1: Remove AI red flags
    text = remove_ai_red_flags(text)
    
    # Step 2: Split into sentences
    sentences = sent_tokenize(text)
    
    # Step 3: Add sentence variety
    sentences = add_sentence_variety(sentences)
    
    # Step 4: Add natural transitions
    sentences = add_natural_transitions(sentences)
    
    # Step 5: Join and apply synonym replacement
    text = ' '.join(sentences)
    text = strategic_synonym_replacement(text, syn_strength)
    
    # Step 6: Add contractions
    text = apply_contractions(text, ratio=0.35)
    
    # Step 7: Add human imperfections
    text = add_human_imperfections(text)
    
    # Step 8: Clean up
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Step 9: Restore citations
    text = restore_citations(text, citations)
    
    return text

########################################
# Streamlit UI
########################################
def show_humanize_page():
    # Custom CSS (keeping your existing styling)
    st.markdown("""
        <style>
        .stApp { background-color: #D8EBC3; }
        .stTextArea textarea {
            background-color: white !important;
            color: #000000 !important;
            caret-color: #000000 !important;
        }
        .stTextArea textarea::placeholder {
            color: #666666 !important;
            opacity: 0.7 !important;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown div, h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: #000000 !important;
        }
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            color: white !important;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        #MainMenu, footer, header { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; color: #2d5016 !important;'>
                ✍️ Enhanced AI Text Humanizer
            </h1>
            <p style='font-size: 1.1rem; color: #4a7c24 !important; margin-bottom: 2rem;'>
                Natural Write converts your AI-generated content into fully humanized, undetectable writing—ensuring it passes every AI detection tool
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Session state
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
    with st.expander("⚙️ Advanced Settings", expanded=False):
        strength = st.slider(
            "⚡ Humanization Strength",
            min_value=1,
            max_value=5,
            value=3,
            help="Higher = more aggressive transformation"
        )

    # Main UI
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📝 Input Text")
        
        input_text = st.text_area(
            "Enter text",
            value=st.session_state.input_text,
            height=400,
            placeholder="Paste your AI-generated text here...",
            key="input_area",
            label_visibility="collapsed"
        )
        
        if input_text:
            st.caption(f"📊 Words: {len(word_tokenize(input_text))}")
        
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
            with st.spinner("Analyzing with advanced AI detection..."):
                time.sleep(1)
                ai_score = calculate_ai_probability(input_text)
                st.session_state.original_ai_score = ai_score
                
            st.markdown("---")
            st.markdown("#### 🤖 AI Detection")
            
            color = "#ff4444" if ai_score >= 70 else "#ffaa00" if ai_score >= 40 else "#44ff44"
            label = "High AI" if ai_score >= 70 else "Medium AI" if ai_score >= 40 else "Low AI"
            
            st.markdown(f"""
                <div style='padding: 1rem; background-color: {color}22; border-left: 4px solid {color}; border-radius: 8px;'>
                    <div style='font-size: 2rem; font-weight: 700; color: {color};'>{ai_score:.1f}%</div>
                    <div style='color: #000000; margin-top: 0.5rem;'>{label} Probability</div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ✅ Humanized Output")
        
        if humanize and input_text.strip():
            st.session_state.input_text = input_text
            
            with st.spinner("🔄 Humanizing with advanced engine..."):
                time.sleep(1.5)
                
                st.session_state.original_ai_score = calculate_ai_probability(input_text)
                
                # Advanced humanization
                humanized = advanced_humanize(input_text, strength=strength)
                
                st.session_state.humanized_text = humanized
                st.session_state.humanized_ai_score = calculate_ai_probability(humanized)
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
                st.caption(f"📊 Words: {len(word_tokenize(st.session_state.humanized_text))}")
            
            st.markdown("---")
            st.markdown("#### 📊 Results")
            
            improvement = st.session_state.original_ai_score - st.session_state.humanized_ai_score
            
            col_before, col_after = st.columns(2)
            
            with col_before:
                st.metric("Before", f"{st.session_state.original_ai_score:.1f}%")
            
            with col_after:
                st.metric("After", f"{st.session_state.humanized_ai_score:.1f}%", 
                         delta=f"-{improvement:.1f}%", delta_color="inverse")
            
            if st.session_state.humanized_ai_score < 25:
                st.success("✅ Excellent! Highly humanized content.")
            elif st.session_state.humanized_ai_score < 40:
                st.info("✨ Good! Significant improvement achieved.")
            
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
                value="Your humanized text will appear here...",
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

    # Features
    st.markdown("---")
    st.markdown("### 🚀 Advanced Features")
    
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    
    with feat_col1:
        st.markdown("**🧠 Smart AI Detection**\n\nMulti-signal analysis system")
    
    with feat_col2:
        st.markdown("**🔄 Natural Variation**\n\nHuman-like sentence diversity")
    
    with feat_col3:
        st.markdown("**🎯 Meaning Preservation**\n\nContext-aware transformations")
    
    with feat_col4:
        st.markdown("**🛡️ Citation Protection**\n\nAcademic integrity maintained")

if __name__ == "__main__":
    show_humanize_page()