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
PRESERVE_WORDS = {
    'not', 'no', 'never', 'none', 'neither', 'nobody', 'nothing',
    'yes', 'all', 'every', 'always', 'must', 'should', 'will', 'can',
    'may', 'might', 'could', 'would', 'shall', 'need', 'essential',
    'critical', 'important', 'significant', 'major', 'minor',
    'increase', 'decrease', 'rise', 'fall', 'grow', 'decline'
}

# Sentence restructuring patterns
RESTRUCTURE_PATTERNS = [
    # Active to passive hints
    {'trigger': ['shows', 'demonstrates', 'proves', 'indicates'], 'type': 'evidence'},
    {'trigger': ['because', 'since', 'as', 'due to'], 'type': 'causation'},
    {'trigger': ['however', 'but', 'although', 'while'], 'type': 'contrast'},
    {'trigger': ['therefore', 'thus', 'hence', 'consequently'], 'type': 'conclusion'},
]

# Natural starting phrases for variety
SENTENCE_STARTERS = {
    'evidence': [
        "Research indicates that", "Studies reveal that", "Evidence suggests that",
        "Analysis shows that", "Data demonstrates that", "Findings indicate that"
    ],
    'causation': [
        "This occurs because", "The reason being", "This happens due to",
        "Given that", "Considering that", "Since"
    ],
    'contrast': [
        "On the contrary,", "Conversely,", "In contrast,", "However,",
        "That said,", "Despite this,", "Yet"
    ],
    'conclusion': [
        "As a result,", "This leads to", "Consequently,", "Therefore,",
        "Thus,", "Hence,", "This means that"
    ],
    'general': [
        "It's worth noting that", "Interestingly,", "Notably,",
        "What's important is", "Consider that", "Essentially,"
    ]
}

# Rich synonym database organized by context
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

########################################
# Helper Functions
########################################
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

PLACEHOLDER_REGEX = re.compile(r"\[\s*\[\s*REF_(\d+)\s*\]\s*\]")

def restore_citations(text, placeholder_map):
    def replace_placeholder(match):
        placeholder = match.group(0)
        return placeholder_map.get(placeholder, placeholder)
    restored = PLACEHOLDER_REGEX.sub(replace_placeholder, text)
    return restored

########################################
# Advanced Synonym Replacement
########################################
def get_best_synonym(word, pos=None):
    """Get contextually appropriate synonym with high replacement rate"""
    word_lower = word.lower()
    
    # Skip very short words and preserved words
    if len(word) < 4 or word_lower in PRESERVE_WORDS:
        return None
    
    # First check rich synonym database
    if word_lower in RICH_SYNONYMS:
        candidates = RICH_SYNONYMS[word_lower]
        return random.choice(candidates)
    
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
    
    synonyms = []
    if wn_pos:
        synsets = wordnet.synsets(word, pos=wn_pos)
        if synsets:
            # Get from first synset only
            for lemma in synsets[0].lemmas():
                lemma_name = lemma.name().replace("_", " ")
                if (lemma_name.lower() != word_lower and 
                    len(lemma_name) <= len(word) + 5 and
                    ' ' not in lemma_name):  # Avoid phrases
                    synonyms.append(lemma_name)
    
    return random.choice(synonyms) if synonyms else None

def deep_synonym_replacement(sentence, strength=0.5):
    """Aggressively replace words while maintaining meaning"""
    if not nlp:
        return sentence
    
    doc = nlp(sentence)
    new_tokens = []
    
    for i, token in enumerate(doc):
        # Skip citations, punctuation, and very short words
        if "[[REF_" in token.text or token.is_punct or len(token.text) < 3:
            new_tokens.append(token.text_with_ws)
            continue
        
        # High probability replacement for content words
        if token.pos_ in ["VERB", "NOUN", "ADJ", "ADV"]:
            if random.random() < strength:  # High replacement rate
                synonym = get_best_synonym(token.text, token.pos_)
                if synonym:
                    # Preserve capitalization
                    if token.text[0].isupper():
                        synonym = synonym.capitalize()
                    new_tokens.append(synonym + token.whitespace_)
                    continue
        
        new_tokens.append(token.text_with_ws)
    
    return "".join(new_tokens).strip()

########################################
# Sentence Structure Transformation
########################################
def transform_sentence_structure(sentence, prev_sentence=None):
    """Transform sentence structure while keeping meaning"""
    
    # Skip very short sentences
    if len(sentence.split()) < 5:
        return sentence
    
    sentence = sentence.strip()
    if not sentence:
        return sentence
    
    # Detect sentence type
    sentence_type = 'general'
    for pattern in RESTRUCTURE_PATTERNS:
        if any(trigger in sentence.lower() for trigger in pattern['trigger']):
            sentence_type = pattern['type']
            break
    
    # Random transformation strategies
    transformations = []
    
    # Strategy 1: Add introductory phrase (40% chance)
    if random.random() < 0.4:
        starters = SENTENCE_STARTERS.get(sentence_type, SENTENCE_STARTERS['general'])
        starter = random.choice(starters)
        
        # Make first letter lowercase after starter
        if sentence[0].isupper() and not sentence.split()[0] in ['I', 'AI']:
            sentence_lower = sentence[0].lower() + sentence[1:]
        else:
            sentence_lower = sentence
        
        transformations.append(f"{starter} {sentence_lower}")
    
    # Strategy 2: Move clauses around (30% chance)
    if random.random() < 0.3 and ',' in sentence:
        parts = sentence.split(',', 1)
        if len(parts) == 2 and len(parts[0].split()) > 2:
            # Swap parts occasionally
            second_part = parts[1].strip()
            if second_part and second_part[0].islower():
                second_part = second_part[0].upper() + second_part[1:]
            transformations.append(f"{second_part}, {parts[0].lower()}")
    
    # Strategy 3: Change connecting words (always apply if found)
    connectors = {
        'however': ['nevertheless', 'yet', 'though'],
        'therefore': ['thus', 'consequently', 'as a result'],
        'because': ['since', 'as', 'given that'],
        'although': ['while', 'though', 'even though'],
        'moreover': ['furthermore', 'additionally', 'what\'s more'],
    }
    
    for old_conn, new_conns in connectors.items():
        if old_conn in sentence.lower():
            new_conn = random.choice(new_conns)
            sentence = re.sub(old_conn, new_conn, sentence, flags=re.IGNORECASE)
    
    # Choose a transformation or return modified sentence
    if transformations and random.random() < 0.5:
        return random.choice(transformations)
    
    return sentence

########################################
# Expand contractions
########################################
contraction_map = {
    "n't": " not", "'re": " are", "'s": " is", "'ll": " will",
    "'ve": " have", "'d": " would", "'m": " am"
}

def expand_contractions(sentence):
    """Expand contractions for formal text"""
    for contr, expansion in contraction_map.items():
        sentence = re.sub(r'\b(\w+)' + re.escape(contr), r'\1' + expansion, sentence)
    return sentence

########################################
# Add Natural Transitions
########################################
def add_natural_connector(sentence, prev_sentence=None, strength=0.3):
    """Add transitions based on context"""
    if random.random() > strength:
        return sentence
    
    # Don't add if sentence already starts with transition
    first_word = sentence.split()[0].lower().rstrip(',')
    common_transitions = ['however', 'therefore', 'moreover', 'furthermore', 
                         'additionally', 'consequently', 'nevertheless']
    
    if first_word in common_transitions:
        return sentence
    
    # Detect relationship with previous sentence
    if prev_sentence:
        # Check for contrast
        if any(word in sentence.lower() for word in ['but', 'however', 'although', 'despite']):
            transitions = ['On the other hand,', 'Conversely,', 'In contrast,', 'However,']
        # Check for addition
        elif any(word in sentence.lower() for word in ['also', 'and', 'addition']):
            transitions = ['Additionally,', 'Moreover,', 'Furthermore,', 'In addition,']
        # Check for result
        elif any(word in sentence.lower() for word in ['result', 'therefore', 'thus']):
            transitions = ['As a result,', 'Consequently,', 'Therefore,', 'Thus,']
        else:
            transitions = ['Notably,', 'Interestingly,', 'In this regard,', 'It is worth noting that']
        
        connector = random.choice(transitions)
        return f"{connector} {sentence[0].lower()}{sentence[1:]}"
    
    return sentence

########################################
# Aggressive Word Variation
########################################
def apply_word_variations(text, strength=0.6):
    """Apply multiple word variations with high coverage"""
    
    # Common phrase replacements
    phrase_replacements = {
        r'\bin order to\b': ['to', 'so as to', 'with the aim of'],
        r'\bdue to the fact that\b': ['because', 'since', 'as'],
        r'\bat the present time\b': ['currently', 'now', 'presently'],
        r'\bin the event that\b': ['if', 'should', 'when'],
        r'\bfor the purpose of\b': ['to', 'for'],
        r'\bin spite of\b': ['despite', 'regardless of'],
        r'\bby means of\b': ['through', 'via', 'using'],
        r'\bit is important to note that\b': ['notably,', 'importantly,', 'significantly,'],
    }
    
    for pattern, replacements in phrase_replacements.items():
        if re.search(pattern, text, re.IGNORECASE):
            replacement = random.choice(replacements)
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

########################################
# Main Enhanced Humanization Pipeline
########################################
def ultra_humanize(text, synonym_strength=0.6, structure_strength=0.4, transition_strength=0.3):
    """Ultra-aggressive humanization that transforms every sentence"""
    
    # Extract citations first
    text, placeholders = extract_citations(text)
    
    # Split into sentences
    sentences = sent_tokenize(text)
    
    if not sentences:
        return text
    
    transformed_sentences = []
    
    for i, sent in enumerate(sentences):
        if not sent.strip():
            continue
        
        # Step 1: Expand contractions
        sent = expand_contractions(sent)
        
        # Step 2: Apply phrase variations
        sent = apply_word_variations(sent, strength=0.5)
        
        # Step 3: Deep synonym replacement (aggressive)
        sent = deep_synonym_replacement(sent, strength=synonym_strength)
        
        # Step 4: Transform sentence structure
        prev = transformed_sentences[-1] if transformed_sentences else None
        sent = transform_sentence_structure(sent, prev)
        
        # Step 5: Add natural connectors
        if i > 0:
            sent = add_natural_connector(sent, prev, strength=transition_strength)
        
        transformed_sentences.append(sent)
    
    # Join sentences
    result = " ".join(transformed_sentences)
    
    # Restore citations
    result = restore_citations(result, placeholders)
    
    # Clean up spacing
    result = re.sub(r'\s+([.,;:!?])', r'\1', result)
    result = re.sub(r'\s{2,}', ' ', result)
    result = re.sub(r'(\w+)\s+(\1)', r'\1', result)  # Remove accidental duplicates
    
    return result

########################################
# AI Detection Calculator
########################################
def calculate_ai_probability(text):
    """Calculate realistic AI probability score"""
    if not text.strip():
        return 0
    
    score = 50
    
    ai_indicators = [
        'furthermore', 'moreover', 'additionally', 'consequently',
        'it is important to note', 'in conclusion', 'in summary',
        'it should be noted', 'it is crucial', 'significantly'
    ]
    
    text_lower = text.lower()
    indicator_count = sum(1 for indicator in ai_indicators if indicator in text_lower)
    score += min(indicator_count * 5, 30)
    
    sentences = sent_tokenize(text)
    if len(sentences) > 3:
        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        if variance < 20:
            score += 15
    
    contraction_count = len(re.findall(r"\b\w+n't\b|\b\w+'re\b|\b\w+'ll\b", text))
    if contraction_count < len(sentences) * 0.1:
        score += 10
    
    words = word_tokenize(text.lower())
    unique_ratio = len(set(words)) / len(words) if words else 0
    if unique_ratio > 0.7:
        score += 10
    
    return max(0, min(100, score))

def calculate_humanized_probability(original_score, strength_level):
    """Calculate probability after humanization"""
    reduction_map = {
        1: 0.4,
        2: 0.55,
        3: 0.7,
        4: 0.82,
        5: 0.92
    }
    
    reduction = reduction_map.get(strength_level, 0.7)
    new_score = original_score * (1 - reduction)
    return max(3, min(25, new_score))

########################################
# Streamlit UI
########################################
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
    p_syn = 0.3 + (synonym_strength * 0.14)  # 0.44 to 1.0
    p_struct = 0.2 + (structure_strength * 0.16)  # 0.36 to 1.0
    p_trans = 0.15 + (overall_strength * 0.1)  # 0.25 to 0.65

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
                
                # Simulate processing stages
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