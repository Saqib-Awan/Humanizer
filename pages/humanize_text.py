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

# Download NLTK resources
def download_nltk_resources():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    for r in ['punkt', 'wordnet', 'averaged_perceptron_tagger_eng']:
        nltk.download(r, quiet=True)

download_nltk_resources()

# Load spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

# ============================================================================
# CORE CONFIGURATIONS - STREAMLINED
# ============================================================================

CITATION_REGEX = re.compile(r"\(\s*[A-Za-z&\-,\.\s]+(?:et al\.\s*)?,\s*\d{4}(?:,\s*(?:pp?\.\s*\d+(?:-\d+)?))?\s*\)")

PRESERVE_WORDS = {
    'not', 'no', 'never', 'none', 'must', 'should', 'will', 'can', 'may',
    'data', 'research', 'study', 'analysis', 'evidence', 'results'
}

# Enhanced synonym database with contextual awareness
SYNONYMS = {
    'important': ['crucial', 'vital', 'key', 'critical', 'significant', 'essential'],
    'show': ['reveal', 'demonstrate', 'indicate', 'display', 'illustrate'],
    'use': ['utilize', 'employ', 'apply', 'leverage', 'implement'],
    'make': ['create', 'produce', 'generate', 'develop', 'establish'],
    'get': ['obtain', 'acquire', 'secure', 'gain', 'achieve'],
    'think': ['believe', 'consider', 'regard', 'view', 'perceive'],
    'help': ['assist', 'aid', 'support', 'facilitate', 'enable'],
    'find': ['discover', 'identify', 'locate', 'determine', 'uncover'],
    'give': ['provide', 'offer', 'supply', 'deliver', 'present'],
    'good': ['effective', 'beneficial', 'valuable', 'positive', 'favorable'],
    'bad': ['detrimental', 'harmful', 'negative', 'adverse', 'problematic'],
    'big': ['substantial', 'significant', 'considerable', 'extensive'],
    'small': ['minor', 'limited', 'modest', 'minimal', 'slight'],
    'many': ['numerous', 'various', 'multiple', 'several', 'countless'],
    'very': ['extremely', 'highly', 'particularly', 'notably', 'remarkably'],
}

# AI red flags - most obvious patterns
AI_PHRASES = {
    r'\bfurthermore\b': ['plus', 'also', "what's more", 'beyond that'],
    r'\bmoreover\b': ['also', 'plus', 'additionally', 'on top of that'],
    r'\bnevertheless\b': ['still', 'yet', 'however', 'even so'],
    r'\bconsequently\b': ['so', 'therefore', 'as a result', 'thus'],
    r'\bit is important to note that\b': ['notably', 'note that', 'importantly'],
    r'\bin conclusion\b': ['overall', 'in sum', 'ultimately', 'finally'],
    r'\bdelve into\b': ['explore', 'examine', 'look at', 'investigate'],
    r'\bin order to\b': ['to', 'so as to'],
    r'\bdue to the fact that\b': ['because', 'since', 'as'],
}

SENTENCE_STARTERS = [
    "Research shows", "Evidence suggests", "Studies reveal", "Analysis indicates",
    "This occurs because", "Given that", "Considering that",
    "However,", "Yet,", "Still,", "On the contrary,",
    "As a result,", "Therefore,", "Thus,", "Consequently,",
    "Interestingly,", "Notably,", "Clearly,", "Essentially,"
]

# ============================================================================
# AI DETECTION - ADVANCED SCORING
# ============================================================================

def calculate_ai_score(text):
    """Advanced AI detection using multiple linguistic markers"""
    if not text.strip():
        return 0
    
    score = 0
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # 1. Repetitive patterns (AI loves consistency)
    sentence_lengths = [len(s.split()) for s in sentences]
    if len(sentence_lengths) > 3:
        avg = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((x - avg) ** 2 for x in sentence_lengths) / len(sentence_lengths)
        if variance < 25:  # Too consistent = AI
            score += 20
    
    # 2. AI buzzwords frequency
    ai_words = ['furthermore', 'moreover', 'consequently', 'nevertheless', 
                'thus', 'hence', 'thereby', 'wherein', 'wherein']
    ai_count = sum(1 for word in words if word in ai_words)
    score += min(ai_count * 8, 25)
    
    # 3. Passive voice (AI overuses it)
    passive_patterns = ['is being', 'are being', 'was being', 'were being',
                       'is shown', 'are shown', 'is found', 'are found']
    passive_count = sum(1 for pattern in passive_patterns if pattern in text.lower())
    score += min(passive_count * 6, 20)
    
    # 4. Perfect grammar (no contractions = AI)
    contractions = len(re.findall(r"\b\w+n't\b|\b\w+'re\b|\b\w+'ll\b", text))
    if contractions < len(sentences) * 0.05:  # Less than 5% contractions
        score += 15
    
    # 5. Sentence structure uniformity
    starts = [s.split()[0].lower() if s.split() else '' for s in sentences]
    start_diversity = len(set(starts)) / len(starts) if starts else 1
    if start_diversity < 0.6:  # Too similar starts
        score += 15
    
    # 6. Vocabulary diversity (AI repeats words more)
    unique_ratio = len(set(words)) / len(words) if words else 1
    if unique_ratio < 0.65:  # Low diversity
        score += 10
    
    # 7. Formal transitions overdose
    formal_transitions = ['furthermore', 'moreover', 'additionally', 'consequently',
                         'therefore', 'thus', 'hence', 'subsequently']
    transition_density = sum(1 for w in words if w in formal_transitions) / len(words) * 100
    if transition_density > 2:  # More than 2% formal transitions
        score += 15
    
    return min(100, max(0, score))

def calculate_human_score(original_score, strength):
    """Calculate expected score after humanization"""
    reductions = {1: 0.25, 2: 0.45, 3: 0.65, 4: 0.80, 5: 0.90}
    reduction = reductions.get(strength, 0.70)
    new_score = original_score * (1 - reduction)
    return max(2, min(20, new_score))

# ============================================================================
# CORE HUMANIZATION ENGINE - OPTIMIZED
# ============================================================================

def extract_citations(text):
    """Preserve academic citations"""
    refs = CITATION_REGEX.findall(text)
    for i, ref in enumerate(refs, 1):
        text = text.replace(ref, f"[[REF_{i}]]", 1)
    return text, {f"[[REF_{i}]]": ref for i, ref in enumerate(refs, 1)}

def restore_citations(text, refs):
    """Restore citations after processing"""
    for placeholder, citation in refs.items():
        text = text.replace(placeholder, citation)
    return text

def smart_synonym_replace(sentence, strength=0.7):
    """Context-aware synonym replacement"""
    if not nlp:
        return sentence
    
    doc = nlp(sentence)
    new_tokens = []
    
    for token in doc:
        # Skip citations, punctuation, short words
        if "[[REF_" in token.text or token.is_punct or len(token.text) < 4:
            new_tokens.append(token.text_with_ws)
            continue
        
        # Preserve critical words
        if token.text.lower() in PRESERVE_WORDS:
            new_tokens.append(token.text_with_ws)
            continue
        
        # Replace content words based on strength
        if token.pos_ in ["VERB", "NOUN", "ADJ", "ADV"] and random.random() < strength:
            word_lower = token.text.lower()
            
            # Check custom synonyms first
            if word_lower in SYNONYMS:
                synonym = random.choice(SYNONYMS[word_lower])
                if token.text[0].isupper():
                    synonym = synonym.capitalize()
                new_tokens.append(synonym + token.whitespace_)
                continue
            
            # Try WordNet for other words
            synsets = wordnet.synsets(token.text, pos=getattr(wordnet, token.pos_, None))
            if synsets:
                lemmas = [l.name() for l in synsets[0].lemmas() 
                         if l.name().lower() != word_lower and '_' not in l.name()]
                if lemmas:
                    synonym = random.choice(lemmas[:3])  # Top 3 only
                    if token.text[0].isupper():
                        synonym = synonym.capitalize()
                    new_tokens.append(synonym + token.whitespace_)
                    continue
        
        new_tokens.append(token.text_with_ws)
    
    return "".join(new_tokens).strip()

def restructure_sentence(sentence, prev_sentence=None):
    """Transform sentence structure for variety"""
    if len(sentence.split()) < 6:
        return sentence
    
    # Strategy 1: Add varied starters (40% chance)
    if random.random() < 0.4:
        starter = random.choice(SENTENCE_STARTERS)
        if sentence[0].isupper():
            sentence = sentence[0].lower() + sentence[1:]
        return f"{starter} {sentence}"
    
    # Strategy 2: Move clauses if comma present (30% chance)
    if random.random() < 0.3 and ',' in sentence:
        parts = sentence.split(',', 1)
        if len(parts) == 2 and len(parts[0].split()) > 2:
            second = parts[1].strip()
            if second and second[0].islower():
                second = second[0].upper() + second[1:]
            return f"{second}, {parts[0].lower()}"
    
    return sentence

def remove_ai_patterns(text):
    """Aggressively remove AI-flagged phrases"""
    for pattern, replacements in AI_PHRASES.items():
        if re.search(pattern, text, re.IGNORECASE):
            replacement = random.choice(replacements)
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE, count=1)
    return text

def add_contractions(sentence):
    """Add natural contractions"""
    contractions = {
        r'\bdo not\b': "don't", r'\bdoes not\b': "doesn't", r'\bdid not\b': "didn't",
        r'\bwill not\b': "won't", r'\bwould not\b': "wouldn't", r'\bcannot\b': "can't",
        r'\bis not\b': "isn't", r'\bare not\b': "aren't", r'\bwas not\b': "wasn't",
        r'\bwere not\b': "weren't", r'\bhave not\b': "haven't", r'\bhas not\b': "hasn't",
        r'\bit is\b': "it's", r'\bthat is\b': "that's", r'\bwhat is\b': "what's",
    }
    
    # Apply contractions randomly (50% chance each)
    for pattern, contraction in contractions.items():
        if random.random() < 0.5:
            sentence = re.sub(pattern, contraction, sentence, flags=re.IGNORECASE, count=1)
    
    return sentence

def ultra_humanize(text, strength=4):
    """Main humanization pipeline - streamlined and powerful"""
    # Extract citations
    text, citations = extract_citations(text)
    
    # Get sentences
    sentences = sent_tokenize(text)
    if not sentences:
        return text
    
    # Calculate strength factors
    synonym_power = 0.3 + (strength * 0.15)  # 0.45 to 1.05
    structure_power = 0.2 + (strength * 0.16)  # 0.36 to 1.0
    
    transformed = []
    
    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue
        
        # Step 1: Remove AI patterns
        sentence = remove_ai_patterns(sentence)
        
        # Step 2: Add contractions
        if strength >= 3:
            sentence = add_contractions(sentence)
        
        # Step 3: Smart synonym replacement
        sentence = smart_synonym_replace(sentence, min(synonym_power, 0.85))
        
        # Step 4: Restructure sentence
        if random.random() < structure_power:
            prev = transformed[-1] if transformed else None
            sentence = restructure_sentence(sentence, prev)
        
        # Step 5: Vary connectors randomly
        if i > 0 and random.random() < 0.25 and strength >= 3:
            connectors = ['However,', 'Yet,', 'Still,', 'Also,', 'Plus,', 'But,']
            if not any(sentence.startswith(c) for c in connectors):
                connector = random.choice(connectors)
                sentence = f"{connector} {sentence[0].lower()}{sentence[1:]}"
        
        transformed.append(sentence)
    
    # Join and clean
    result = " ".join(transformed)
    result = restore_citations(result, citations)
    
    # Final cleanup
    result = re.sub(r'\s+([.,;:!?])', r'\1', result)
    result = re.sub(r'\s{2,}', ' ', result)
    result = re.sub(r'(\w+)\s+\1\b', r'\1', result)  # Remove duplicates
    
    return result.strip()

# ============================================================================
# STREAMLIT UI - KEEP ORIGINAL DESIGN
# ============================================================================

def show_humanize_page():
    st.markdown("""
        <style>
        .stApp { background-color: #D8EBC3; }
        .stTextArea textarea { background-color: white !important; color: #000000 !important; }
        .stMarkdown, h1, h2, h3, h4, p, div, span, label { color: #000000 !important; }
        .stButton > button { border-radius: 8px; font-weight: 500; }
        #MainMenu, footer, header { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; color: #2d5016 !important;'>
                ✍️ Ultra AI Text Humanizer
            </h1>
            <p style='font-size: 1.1rem; color: #4a7c24 !important;'>
                StealthWriter-level transformation engine
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    if 'humanized_text' not in st.session_state:
        st.session_state.humanized_text = ""
    if 'original_score' not in st.session_state:
        st.session_state.original_score = 0
    if 'human_score' not in st.session_state:
        st.session_state.human_score = 0
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

    # Settings
    with st.expander("⚙️ Transformation Settings", expanded=False):
        st.markdown("### 🎚️ Humanization Power")
        
        strength = st.slider(
            "Transformation Intensity",
            min_value=1,
            max_value=5,
            value=4,
            help="Higher = More aggressive transformation (Recommended: 4-5)"
        )
        
        st.info(f"**Level {strength}**: {'Light' if strength <= 2 else 'Medium' if strength == 3 else 'Strong' if strength == 4 else 'Maximum'} transformation")

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
            words = len(word_tokenize(input_text))
            sents = len(sent_tokenize(input_text))
            st.caption(f"📊 {words} words · {sents} sentences")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            check = st.button("🔍 Check AI", use_container_width=True, type="secondary")
        
        with col_b:
            humanize = st.button("✨ Transform", use_container_width=True, type="primary")
        
        with col_c:
            if st.button("🗑️ Clear", use_container_width=True, type="secondary"):
                st.session_state.input_text = ""
                st.session_state.humanized_text = ""
                st.session_state.show_results = False
                st.rerun()

        if check and input_text.strip():
            with st.spinner("🔍 Analyzing AI patterns..."):
                time.sleep(0.8)
                score = calculate_ai_score(input_text)
                st.session_state.original_score = score
            
            st.markdown("---")
            st.markdown("#### 🤖 AI Detection Score")
            
            color = "#ff4444" if score >= 70 else "#ffaa00" if score >= 40 else "#44ff44"
            label = "High AI" if score >= 70 else "Medium AI" if score >= 40 else "Low AI"
            
            st.markdown(f"""
                <div style='padding: 1rem; background-color: {color}22; border-left: 4px solid {color}; border-radius: 8px;'>
                    <div style='font-size: 2rem; font-weight: 700; color: {color};'>{score:.0f}%</div>
                    <div style='color: #000000; margin-top: 0.5rem;'>{label} Probability</div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ✅ Transformed Text")
        
        if humanize and input_text.strip():
            st.session_state.input_text = input_text
            
            with st.spinner("🔄 Transforming..."):
                progress = st.progress(0)
                
                progress.progress(30)
                st.session_state.original_score = calculate_ai_score(input_text)
                time.sleep(0.3)
                
                progress.progress(60)
                result = ultra_humanize(input_text, strength)
                time.sleep(0.3)
                
                st.session_state.humanized_text = result
                st.session_state.human_score = calculate_human_score(
                    st.session_state.original_score, strength
                )
                
                progress.progress(100)
                time.sleep(0.2)
                progress.empty()
                
                st.session_state.show_results = True
        
        if st.session_state.show_results and st.session_state.humanized_text:
            st.text_area(
                "Result",
                value=st.session_state.humanized_text,
                height=400,
                key="output_area",
                label_visibility="collapsed"
            )
            
            words = len(word_tokenize(st.session_state.humanized_text))
            sents = len(sent_tokenize(st.session_state.humanized_text))
            st.caption(f"📊 {words} words · {sents} sentences")
            
            st.markdown("---")
            st.markdown("#### 📊 Transformation Results")
            
            improvement = st.session_state.original_score - st.session_state.human_score
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Before", f"{st.session_state.original_score:.0f}%")
            with m2:
                st.metric("After", f"{st.session_state.human_score:.0f}%")
            with m3:
                st.metric("Reduced", f"{improvement:.0f}%", delta=f"-{improvement:.0f}%")
            
            if st.session_state.human_score < 15:
                st.success("✅ Excellent! Highly humanized text.")
            elif st.session_state.human_score < 30:
                st.info("👍 Good! Try level 5 for better results.")
            else:
                st.warning("⚠️ Increase to level 4-5 for better humanization.")
            
            st.download_button(
                "💾 Download Text",
                data=st.session_state.humanized_text,
                file_name="humanized_text.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )
        else:
            st.text_area(
                "Result",
                value="Your transformed text will appear here...",
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

    # Features
    st.markdown("---")
    st.markdown("### 🚀 Key Features")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**🔄 Structure Shift**\n\nReorders sentence patterns")
    with c2:
        st.markdown("**📝 Smart Synonyms**\n\nContext-aware replacements")
    with c3:
        st.markdown("**🎯 Meaning Lock**\n\nPreserves original intent")
    with c4:
        st.markdown("**🛡️ Citation Safe**\n\nProtects references")

if __name__ == "__main__":
    show_humanize_page()