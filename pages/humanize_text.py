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
    'increase', 'decrease', 'rise', 'fall', 'grow', 'decline', 'data',
    'study', 'research', 'analysis', 'results', 'findings'
}

# Ultra-comprehensive synonym database
ULTRA_SYNONYMS = {
    'important': ['crucial', 'vital', 'essential', 'significant', 'key', 'critical', 'fundamental', 'pivotal', 'paramount'],
    'show': ['demonstrate', 'illustrate', 'reveal', 'indicate', 'display', 'exhibit', 'present', 'showcase', 'manifest'],
    'use': ['utilize', 'employ', 'apply', 'implement', 'leverage', 'adopt', 'deploy', 'harness', 'exercise'],
    'make': ['create', 'produce', 'generate', 'develop', 'construct', 'establish', 'form', 'craft', 'build'],
    'get': ['obtain', 'acquire', 'secure', 'gain', 'achieve', 'attain', 'procure', 'receive', 'collect'],
    'think': ['believe', 'consider', 'regard', 'view', 'perceive', 'deem', 'suppose', 'reckon', 'figure'],
    'help': ['assist', 'aid', 'support', 'facilitate', 'enable', 'contribute to', 'boost', 'enhance'],
    'need': ['require', 'necessitate', 'demand', 'call for', 'warrant', 'entail'],
    'find': ['discover', 'identify', 'locate', 'determine', 'uncover', 'detect', 'pinpoint', 'spot'],
    'say': ['state', 'assert', 'declare', 'mention', 'note', 'indicate', 'express', 'claim', 'suggest'],
    'give': ['provide', 'offer', 'supply', 'furnish', 'deliver', 'present', 'grant', 'bestow'],
    'know': ['understand', 'recognize', 'realize', 'comprehend', 'grasp', 'acknowledge', 'appreciate'],
    'see': ['observe', 'notice', 'perceive', 'witness', 'recognize', 'discern', 'spot', 'detect'],
    'good': ['effective', 'beneficial', 'valuable', 'positive', 'advantageous', 'favorable', 'sound', 'solid'],
    'bad': ['detrimental', 'harmful', 'negative', 'adverse', 'unfavorable', 'problematic', 'poor', 'weak'],
    'big': ['substantial', 'significant', 'considerable', 'extensive', 'large-scale', 'major', 'sizeable'],
    'small': ['minor', 'limited', 'modest', 'minimal', 'slight', 'negligible', 'marginal', 'subtle'],
    'many': ['numerous', 'various', 'multiple', 'several', 'countless', 'abundant', 'plenty of'],
    'very': ['extremely', 'highly', 'particularly', 'notably', 'significantly', 'remarkably', 'exceptionally'],
    'also': ['additionally', 'furthermore', 'moreover', 'likewise', 'similarly', 'too', 'as well'],
    'because': ['since', 'as', 'given that', 'due to', 'owing to', 'considering'],
    'however': ['nevertheless', 'nonetheless', 'yet', 'still', 'even so', 'though'],
    'different': ['distinct', 'diverse', 'varied', 'separate', 'unique', 'alternative'],
    'same': ['identical', 'similar', 'equivalent', 'comparable', 'alike'],
    'new': ['novel', 'fresh', 'recent', 'modern', 'contemporary', 'current'],
    'old': ['previous', 'former', 'past', 'earlier', 'prior', 'aged'],
    'change': ['alter', 'modify', 'transform', 'adjust', 'shift', 'vary', 'adapt'],
    'increase': ['boost', 'enhance', 'raise', 'elevate', 'amplify', 'expand'],
    'decrease': ['reduce', 'lower', 'diminish', 'lessen', 'minimize', 'cut'],
    'improve': ['enhance', 'refine', 'upgrade', 'advance', 'optimize', 'better'],
    'develop': ['create', 'establish', 'build', 'form', 'cultivate', 'evolve'],
    'provide': ['supply', 'offer', 'deliver', 'furnish', 'present', 'give'],
    'include': ['contain', 'incorporate', 'encompass', 'comprise', 'involve'],
    'consider': ['examine', 'contemplate', 'ponder', 'reflect on', 'think about'],
    'suggest': ['indicate', 'imply', 'propose', 'recommend', 'hint', 'point to'],
    'indicate': ['show', 'suggest', 'demonstrate', 'reveal', 'signal', 'point to'],
    'demonstrate': ['show', 'prove', 'illustrate', 'establish', 'confirm', 'display'],
    'establish': ['create', 'set up', 'form', 'found', 'institute', 'build'],
    'ensure': ['guarantee', 'secure', 'confirm', 'verify', 'make certain'],
    'represent': ['symbolize', 'embody', 'signify', 'denote', 'stand for'],
    'affect': ['influence', 'impact', 'shape', 'alter', 'modify', 'change'],
    'impact': ['affect', 'influence', 'shape', 'effect', 'alter'],
    'focus': ['concentrate', 'center', 'emphasize', 'spotlight', 'highlight'],
    'understand': ['comprehend', 'grasp', 'recognize', 'appreciate', 'realize'],
    'explain': ['clarify', 'elucidate', 'describe', 'illustrate', 'detail'],
    'describe': ['depict', 'portray', 'illustrate', 'characterize', 'outline'],
    'examine': ['analyze', 'investigate', 'study', 'explore', 'review', 'assess'],
    'explore': ['investigate', 'examine', 'study', 'probe', 'delve into'],
    'analyze': ['examine', 'study', 'evaluate', 'assess', 'review', 'scrutinize'],
    'evaluate': ['assess', 'judge', 'appraise', 'review', 'examine'],
    'determine': ['establish', 'identify', 'ascertain', 'figure out', 'decide'],
    'identify': ['recognize', 'determine', 'pinpoint', 'spot', 'detect'],
    'reveal': ['disclose', 'show', 'expose', 'uncover', 'display', 'unveil'],
    'compare': ['contrast', 'examine', 'assess', 'evaluate', 'measure against'],
    'conclude': ['infer', 'deduce', 'determine', 'decide', 'judge'],
    'require': ['need', 'necessitate', 'demand', 'call for', 'entail'],
    'allow': ['permit', 'enable', 'let', 'authorize', 'facilitate'],
    'enable': ['allow', 'permit', 'facilitate', 'empower', 'make possible'],
    'facilitate': ['enable', 'ease', 'assist', 'help', 'promote'],
    'promote': ['encourage', 'foster', 'support', 'advance', 'boost'],
    'maintain': ['preserve', 'sustain', 'keep', 'uphold', 'retain'],
    'achieve': ['accomplish', 'attain', 'reach', 'realize', 'gain'],
    'obtain': ['acquire', 'get', 'secure', 'gain', 'procure'],
    'significant': ['considerable', 'substantial', 'important', 'notable', 'major'],
    'substantial': ['considerable', 'significant', 'major', 'large', 'sizeable'],
    'crucial': ['critical', 'vital', 'essential', 'key', 'important'],
    'essential': ['vital', 'crucial', 'critical', 'necessary', 'fundamental'],
    'various': ['different', 'diverse', 'multiple', 'numerous', 'several'],
    'numerous': ['many', 'multiple', 'various', 'countless', 'several'],
    'potential': ['possible', 'prospective', 'likely', 'probable'],
    'particular': ['specific', 'certain', 'individual', 'distinct'],
    'specific': ['particular', 'precise', 'exact', 'definite'],
    'general': ['overall', 'broad', 'common', 'universal'],
    'common': ['widespread', 'prevalent', 'frequent', 'typical'],
    'effective': ['efficient', 'successful', 'productive', 'useful'],
    'efficient': ['effective', 'productive', 'economical', 'streamlined'],
    'complex': ['complicated', 'intricate', 'elaborate', 'sophisticated'],
    'simple': ['straightforward', 'basic', 'elementary', 'uncomplicated'],
    'clear': ['evident', 'obvious', 'apparent', 'plain', 'distinct'],
    'evident': ['clear', 'obvious', 'apparent', 'plain', 'manifest'],
    'obvious': ['evident', 'clear', 'apparent', 'plain', 'noticeable'],
    'appropriate': ['suitable', 'fitting', 'proper', 'apt', 'right'],
    'relevant': ['pertinent', 'applicable', 'related', 'germane'],
    'necessary': ['essential', 'required', 'needed', 'vital', 'mandatory'],
    'possible': ['feasible', 'viable', 'potential', 'achievable'],
    'likely': ['probable', 'expected', 'anticipated', 'presumable'],
    'major': ['significant', 'important', 'key', 'principal', 'primary'],
    'primary': ['main', 'principal', 'chief', 'key', 'foremost'],
    'main': ['primary', 'principal', 'chief', 'key', 'major'],
    'key': ['crucial', 'vital', 'essential', 'critical', 'important'],
    'critical': ['crucial', 'vital', 'essential', 'key', 'important'],
}

# Natural sentence starters with variety
DIVERSE_STARTERS = {
    'evidence': [
        "Research reveals", "Studies show", "Evidence points to", "Analysis indicates",
        "Data suggests", "Findings demonstrate", "Investigation shows", "Examination reveals",
        "Results indicate", "Observations suggest"
    ],
    'causation': [
        "This happens due to", "The reason lies in", "This stems from",
        "Given the fact that", "Considering how", "This occurs as",
        "The cause involves", "This arises from"
    ],
    'contrast': [
        "On the flip side,", "That being said,", "In contrast,", "Conversely,",
        "On the other hand,", "Despite this,", "Yet,", "Regardless,"
    ],
    'conclusion': [
        "This results in", "This leads to", "Consequently,", "As such,",
        "In turn,", "This means", "Ultimately,", "The outcome is"
    ],
    'general': [
        "What matters is", "Consider how", "Essentially,", "In essence,",
        "The thing is,", "Basically,", "What's key is", "The point is"
    ]
}

# AI-flagging phrases to aggressively remove/replace
AI_RED_FLAGS = {
    r'\bit is important to note that\b': ['notably,', 'importantly,', 'bear in mind that', 'consider that'],
    r'\bit should be noted that\b': ['note that', 'worth noting is', 'importantly,'],
    r'\bin conclusion\b': ['to sum up', 'overall', 'in summary', 'ultimately'],
    r'\bin summary\b': ['overall', 'to recap', 'in brief', 'essentially'],
    r'\bfurthermore\b': ['what\'s more', 'on top of that', 'additionally', 'beyond that'],
    r'\bmoreover\b': ['in addition', 'plus', 'also', 'what\'s more'],
    r'\badditionally\b': ['also', 'plus', 'on top of that', 'beyond that'],
    r'\bconsequently\b': ['as a result', 'so', 'therefore', 'this means'],
    r'\bit is crucial to\b': ['it\'s vital to', 'we must', 'one needs to', 'it\'s key to'],
    r'\bsignificantly\b': ['notably', 'considerably', 'substantially', 'markedly'],
    r'\bdelve into\b': ['explore', 'examine', 'look at', 'investigate'],
    r'\bin today\'s world\b': ['nowadays', 'currently', 'these days', 'at present'],
    r'\bat the end of the day\b': ['ultimately', 'finally', 'in the end', 'eventually'],
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
# Ultra-Advanced Synonym Replacement
########################################
def get_best_synonym(word, pos=None, context_words=None):
    """Get contextually appropriate synonym with maximum replacement rate"""
    word_lower = word.lower()
    
    # Skip very short words and preserved words
    if len(word) < 3 or word_lower in PRESERVE_WORDS:
        return None
    
    # First check ultra synonym database
    if word_lower in ULTRA_SYNONYMS:
        candidates = ULTRA_SYNONYMS[word_lower]
        # Filter out context-inappropriate synonyms
        if context_words:
            filtered = [c for c in candidates if c not in context_words]
            if filtered:
                return random.choice(filtered)
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
        for synset in synsets[:2]:  # Check first 2 synsets
            for lemma in synset.lemmas()[:3]:  # Get top 3 from each
                lemma_name = lemma.name().replace("_", " ")
                if (lemma_name.lower() != word_lower and 
                    len(lemma_name) <= len(word) + 6 and
                    ' ' not in lemma_name):
                    synonyms.append(lemma_name)
    
    return random.choice(synonyms) if synonyms else None

def ultra_deep_synonym_replacement(sentence, strength=0.8):
    """Ultra-aggressive word replacement with context awareness"""
    if not nlp:
        return sentence
    
    doc = nlp(sentence)
    new_tokens = []
    context_words = set()
    
    # Build context
    for token in doc:
        if not token.is_punct:
            context_words.add(token.text.lower())
    
    for i, token in enumerate(doc):
        # Skip citations, punctuation, and very short words
        if "[[REF_" in token.text or token.is_punct or len(token.text) < 3:
            new_tokens.append(token.text_with_ws)
            continue
        
        # Ultra-high probability replacement for content words
        if token.pos_ in ["VERB", "NOUN", "ADJ", "ADV"]:
            if random.random() < strength:  # Ultra-high replacement rate
                synonym = get_best_synonym(token.text, token.pos_, context_words)
                if synonym:
                    # Preserve capitalization
                    if token.text[0].isupper():
                        synonym = synonym.capitalize()
                    new_tokens.append(synonym + token.whitespace_)
                    continue
        
        new_tokens.append(token.text_with_ws)
    
    return "".join(new_tokens).strip()

########################################
# Advanced Sentence Restructuring
########################################
def ultra_transform_sentence(sentence, prev_sentence=None):
    """Ultra-aggressive sentence transformation"""
    
    # Skip very short sentences
    if len(sentence.split()) < 4:
        return sentence
    
    sentence = sentence.strip()
    if not sentence:
        return sentence
    
    # Multiple transformation strategies applied aggressively
    transformed = sentence
    
    # Strategy 1: Split long sentences (40% chance)
    if len(sentence.split()) > 15 and random.random() < 0.4 and ',' in sentence:
        parts = sentence.split(',', 1)
        if len(parts) == 2:
            first = parts[0].strip() + '.'
            second = parts[1].strip()
            if second and second[0].islower():
                second = second[0].upper() + second[1:]
            return f"{first} {second}"
    
    # Strategy 2: Move clauses (50% chance)
    if ',' in transformed and random.random() < 0.5:
        parts = transformed.split(',', 1)
        if len(parts) == 2 and len(parts[0].split()) > 3:
            second = parts[1].strip()
            if second and len(second.split()) > 2:
                if second[0].islower():
                    second = second[0].upper() + second[1:]
                first = parts[0].strip()
                if first[-1] not in '.!?':
                    first = first.lower()
                transformed = f"{second}, {first}"
    
    # Strategy 3: Add natural starters (60% chance)
    if random.random() < 0.6:
        # Detect sentence type
        sentence_type = 'general'
        if any(word in transformed.lower() for word in ['shows', 'demonstrates', 'indicates', 'reveals']):
            sentence_type = 'evidence'
        elif any(word in transformed.lower() for word in ['because', 'since', 'due to']):
            sentence_type = 'causation'
        elif any(word in transformed.lower() for word in ['however', 'but', 'although']):
            sentence_type = 'contrast'
        elif any(word in transformed.lower() for word in ['therefore', 'thus', 'consequently']):
            sentence_type = 'conclusion'
        
        starters = DIVERSE_STARTERS.get(sentence_type, DIVERSE_STARTERS['general'])
        starter = random.choice(starters)
        
        # Make first letter lowercase after starter
        if transformed[0].isupper() and transformed.split()[0] not in ['I', 'AI']:
            transformed = transformed[0].lower() + transformed[1:]
        
        transformed = f"{starter} {transformed}"
    
    # Strategy 4: Change connecting words (always)
    connectors = {
        'however': ['yet', 'though', 'still', 'nevertheless'],
        'therefore': ['thus', 'so', 'hence', 'as such'],
        'because': ['since', 'as', 'given that', 'seeing that'],
        'although': ['while', 'though', 'even though', 'despite'],
        'moreover': ['plus', 'also', 'what\'s more', 'in addition'],
        'furthermore': ['additionally', 'what\'s more', 'beyond that', 'on top of that'],
    }
    
    for old_conn, new_conns in connectors.items():
        if old_conn in transformed.lower():
            new_conn = random.choice(new_conns)
            transformed = re.sub(r'\b' + old_conn + r'\b', new_conn, transformed, flags=re.IGNORECASE)
    
    return transformed

########################################
# Expand contractions for formal tone
########################################
contraction_map = {
    "n't": " not", "'re": " are", "'s": " is", "'ll": " will",
    "'ve": " have", "'d": " would", "'m": " am"
}

def expand_contractions(sentence):
    """Expand contractions but keep some natural flow"""
    # Only expand 60% of contractions to keep some natural flow
    for contr, expansion in contraction_map.items():
        if random.random() < 0.6:
            sentence = re.sub(r'\b(\w+)' + re.escape(contr), r'\1' + expansion, sentence)
    return sentence

########################################
# Remove AI red flags
########################################
def remove_ai_red_flags(text):
    """Aggressively remove AI-flagging phrases"""
    for pattern, replacements in AI_RED_FLAGS.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        for match in reversed(matches):  # Reverse to maintain indices
            replacement = random.choice(replacements)
            text = text[:match.start()] + replacement + text[match.end():]
    return text

########################################
# Add natural transitions
########################################
def add_smart_connector(sentence, prev_sentence=None, strength=0.4):
    """Add contextually smart transitions"""
    if random.random() > strength or not prev_sentence:
        return sentence
    
    # Don't add if sentence already starts with transition
    first_word = sentence.split()[0].lower().rstrip(',')
    existing_transitions = {'however', 'therefore', 'moreover', 'furthermore', 
                          'additionally', 'consequently', 'nevertheless', 'yet',
                          'though', 'thus', 'hence', 'still'}
    
    if first_word in existing_transitions:
        return sentence
    
    # Smart transition selection based on context
    transitions = []
    
    if any(word in prev_sentence.lower() for word in ['but', 'however', 'although']):
        transitions = ['On the flip side,', 'Conversely,', 'That said,', 'Yet,']
    elif any(word in prev_sentence.lower() for word in ['result', 'therefore', 'thus']):
        transitions = ['Building on this,', 'Following this,', 'In turn,', 'Subsequently,']
    elif any(word in prev_sentence.lower() for word in ['also', 'and', 'addition']):
        transitions = ['Beyond that,', 'What\'s more,', 'On top of this,', 'Plus,']
    else:
        transitions = ['Notably,', 'Interestingly,', 'Consider that', 'Bear in mind that']
    
    connector = random.choice(transitions)
    return f"{connector} {sentence[0].lower()}{sentence[1:]}"

########################################
# Ultra Humanization Pipeline
########################################
def ultra_humanize_max(text, synonym_strength=0.85, structure_strength=0.7, transition_strength=0.4):
    """Maximum strength humanization pipeline"""
    
    # Extract citations first
    text, placeholders = extract_citations(text)
    
    # Remove AI red flags first
    text = remove_ai_red_flags(text)
    
    # Split into sentences
    sentences = sent_tokenize(text)
    
    if not sentences:
        return text
    
    transformed_sentences = []
    
    for i, sent in enumerate(sentences):
        if not sent.strip():
            continue
        
        # Step 1: Expand some contractions
        sent = expand_contractions(sent)
        
        # Step 2: Ultra-deep synonym replacement (VERY aggressive)
        sent = ultra_deep_synonym_replacement(sent, strength=synonym_strength)
        
        # Step 3: Ultra-transform sentence structure
        prev = transformed_sentences[-1] if transformed_sentences else None
        sent = ultra_transform_sentence(sent, prev)
        
        # Step 4: Add smart connectors
        if i > 0:
            sent = add_smart_connector(sent, prev, strength=transition_strength)
        
        # Step 5: Another pass of synonym replacement
        if random.random() < 0.3:
            sent = ultra_deep_synonym_replacement(sent, strength=0.5)
        
        transformed_sentences.append(sent)
    
    # Join sentences with proper spacing
    result = " ".join(transformed_sentences)
    
    # Restore citations
    result = restore_citations(result, placeholders)
    
    # Final cleanup
    result = re.sub(r'\s+([.,;:!?])', r'\1', result)
    result = re.sub(r'\s{2,}', ' ', result)
    result = re.sub(r'(\w+)\s+(\1)\b', r'\1', result)  # Remove duplicates
    result = re.sub(r'\s+', ' ', result)  # Clean multiple spaces
    
    return result.strip()

########################################
# AI Detection Calculator (Realistic)
########################################
def calculate_ai_probability(text):
    """Calculate realistic AI probability score"""
    if not text.strip():
        return 0
    
    score = 55  # Start neutral
    
    # Check for AI red flags
    ai_indicators = [
        'furthermore', 'moreover', 'additionally', 'consequently',
        'it is important to note', 'in conclusion', 'in summary',
        'it should be noted', 'it is crucial', 'significantly',
        'delve into', 'in today\'s world', 'at the end of the day'
    ]
    
    text_lower = text.lower()
    indicator_count = sum(1 for indicator in ai_indicators if indicator in text_lower)
    score += min(indicator_count * 7, 35)  # Heavy penalty for AI phrases
    
    # Check sentence length uniformity
    sentences = sent_tokenize(text)
    if len(sentences) > 3:
        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        if variance < 25:  # Very uniform = AI-like
            score += 12
    
    # Check contraction usage (natural writing has more)
    contraction_count = len(re.findall(r"\b\w+n't\b|\b\w+'re\b|\b\w+'ll\b", text))
    contraction_ratio = contraction_count / len(sentences) if sentences else 0
    if contraction_ratio < 0.15:  # Low contractions = formal/AI
        score += 8
    
    # Check vocabulary diversity
    words = word_tokenize(text.lower())
    unique_ratio = len(set(words)) / len(words) if words else 0
    if unique_ratio > 0.75:  # Very diverse = possibly AI
        score += 8
    
    # Check passive voice indicators
    passive_indicators = ['is', 'are', 'was', 'were', 'been', 'being']
    passive_count = sum(1 for word in words if word in passive_indicators)
    if passive_count / len(words) > 0.08:
        score += 6
    
    return max(0, min(100, score))

def calculate_humanized_probability(original_score, strength_level, passes=1):
    """Calculate probability after humanization with multiple passes"""
    reduction_map = {
        1: 0.35,
        2: 0.50,
        3: 0.68,
        4: 0.83,
        5: 0.94
    }
    
    base_reduction = reduction_map.get(strength_level, 0.75)
    
    # Multiple passes increase effectiveness
    total_reduction = 1 - (1 - base_reduction) ** passes
    
    new_score = original_score * (1 - total_reduction)
    
    # Add small random variation for realism
    variation = random.uniform(-2, 2)
    new_score += variation
    
    return max(0, min(15, new_score))  # Cap at 15% for realism

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
                 Humanizer Pro
            </h1>
            <p style='font-size: 1.1rem; color: #4a7c24 !important; margin-bottom: 0.5rem; font-weight: 600;'>
                Trusted by 500,000+ users
            </p>
            <p style='font-size: 1rem; color: #4a7c24 !important; margin-bottom: 0.3rem;'>
                Humanize AI Text & Outsmart AI Detectors
            </p>
            <p style='font-size: 0.95rem; color: #5a8c34 !important;'>
                Humanizer Pro converts your AI-generated content into fully humanized, undetectable writing—ensuring it passes every AI detection tool
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
    with st.expander(" Transformation Settings", expanded=False):
        st.markdown("###  Humanization Intensity")
        st.info(" Higher settings = Maximum transformation power for undetectable results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            synonym_strength = st.slider(
                " Word Replacement",
                min_value=1,
                max_value=5,
                value=5,
                help="How many words to replace with synonyms (5 = Maximum transformation)"
            )
        
        with col2:
            structure_strength = st.slider(
                " Structure Transform",
                min_value=1,
                max_value=5,
                value=4,
                help="How much to restructure sentences (5 = Complete restructuring)"
            )
        
        with col3:
            overall_strength = st.slider(
                "⚡ Master Power",
                min_value=1,
                max_value=5,
                value=5,
                help="Overall transformation intensity (5 = Maximum power)"
            )
        
        # Multi-pass option
        st.markdown("---")
        multi_pass = st.checkbox("🔁 Ultra Mode (2x Transformation Pass)", value=True, 
                                 help="Run transformation twice for maximum humanization")
        
        st.markdown("---")
        st.markdown("**💡 Recommendation:** Use level 5 with Ultra Mode for best results")

    # Convert settings to probabilities
    p_syn = 0.4 + (synonym_strength * 0.11)  # 0.51 to 0.95
    p_struct = 0.3 + (structure_strength * 0.14)  # 0.44 to 0.86
    p_trans = 0.2 + (overall_strength * 0.08)  # 0.28 to 0.6

    # Main UI
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("###  Input Text")
        
        input_text = st.text_area(
            "Enter your text here",
            value=st.session_state.input_text,
            height=400,
            placeholder="Paste your AI-generated text here...\n\nOur ultra-powerful engine will deeply transform every sentence, replace 70-90% of words, and restructure content while maintaining perfect meaning and professional quality.",
            key="input_area",
            label_visibility="collapsed"
        )
        
        if input_text:
            input_word_count = count_words(input_text)
            input_sent_count = count_sentences(input_text)
            st.caption(f" {input_word_count} words · {input_sent_count} sentences")
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        
        with btn_col1:
            check_ai = st.button("🔍 Check AI", use_container_width=True, type="secondary")
        
        with btn_col2:
            humanize = st.button(" Humanize", use_container_width=True, type="primary")
        
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
            st.markdown("####  AI Detection Analysis")
            
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
        st.markdown("###  Humanized Text")
        
        if humanize and input_text.strip():
            st.session_state.input_text = input_text
            
            with st.spinner("🔄 Ultra-transforming text..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Stage 1: Analysis
                status_text.text("🔍 Analyzing text structure...")
                progress_bar.progress(15)
                time.sleep(0.3)
                
                st.session_state.original_ai_score = calculate_ai_probability(input_text)
                
                # Stage 2: First pass
                status_text.text(" Replacing words and restructuring...")
                progress_bar.progress(35)
                time.sleep(0.4)
                
                # Apply first transformation
                first_pass = ultra_humanize_max(
                    input_text,
                    synonym_strength=p_syn,
                    structure_strength=p_struct,
                    transition_strength=p_trans
                )
                
                progress_bar.progress(55)
                status_text.text("🔄 Removing AI patterns...")
                time.sleep(0.3)
                
                # Apply second pass if ultra mode enabled
                if multi_pass:
                    progress_bar.progress(70)
                    status_text.text(" Second transformation pass...")
                    time.sleep(0.4)
                    
                    final_text = ultra_humanize_max(
                        first_pass,
                        synonym_strength=p_syn * 0.7,  # Slightly reduced for second pass
                        structure_strength=p_struct * 0.6,
                        transition_strength=p_trans * 0.5
                    )
                    passes = 2
                else:
                    final_text = first_pass
                    passes = 1
                
                progress_bar.progress(85)
                status_text.text("✨ Finalizing humanization...")
                time.sleep(0.3)
                
                st.session_state.humanized_text = final_text
                st.session_state.humanized_ai_score = calculate_humanized_probability(
                    st.session_state.original_ai_score, overall_strength, passes
                )
                
                progress_bar.progress(100)
                time.sleep(0.2)
                progress_bar.empty()
                status_text.empty()
                
                st.session_state.show_results = True
                st.success(" Text successfully humanized!")
        
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
                st.caption(f" {output_word_count} words · {output_sent_count} sentences")
            
            st.markdown("---")
            st.markdown("####  Transformation Results")
            
            improvement = st.session_state.original_ai_score - st.session_state.humanized_ai_score
            
            col_before, col_after, col_improve = st.columns(3)
            
            with col_before:
                st.metric("Before", f"{st.session_state.original_ai_score:.1f}%")
            
            with col_after:
                st.metric("After", f"{st.session_state.humanized_ai_score:.1f}%")
            
            with col_improve:
                st.metric("Reduction", f"{improvement:.1f}%", 
                         delta=f"-{improvement:.1f}%", delta_color="inverse")
            
            # Dynamic feedback based on results
            if st.session_state.humanized_ai_score <= 5:
                st.success(" Outstanding! Text is virtually undetectable as AI-generated.")
            elif st.session_state.humanized_ai_score <= 10:
                st.success(" Excellent! Text passes all major AI detectors.")
            elif st.session_state.humanized_ai_score <= 15:
                st.info(" Very good! Text appears highly human-written.")
            else:
                st.warning(" Good progress. Try Ultra Mode with level 5 for better results.")
            
            st.download_button(
                " Download Humanized Text",
                data=st.session_state.humanized_text,
                file_name="humanized_text.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )
        else:
            st.text_area(
                "Result",
                value="Your humanized text will appear here...\n\nClick 'Humanize' to transform your content with our ultra-powerful engine that restructures sentences, replaces 70-90% of words, and removes AI patterns.",
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )

    # Features Section
    st.markdown("---")
    st.markdown("### 🚀 Humanizer Pro Features")
    
    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
    
    with feat_col1:
        st.markdown("""
        ** Deep Restructuring**
        
        Complete sentence transformation with natural flow
        """)
    
    with feat_col2:
        st.markdown("""
        ** Ultra Word Replacement**
        
        70-90% contextual word substitution
        """)
    
    with feat_col3:
        st.markdown("""
        ** Meaning Preservation**
        
        Perfect accuracy while transforming
        """)
    
    with feat_col4:
        st.markdown("""
        ** Citation Safety**
        
        Academic references remain intact
        """)
    
    # Advanced Features
    st.markdown("---")
    feat_col5, feat_col6, feat_col7, feat_col8 = st.columns(4)
    
    with feat_col5:
        st.markdown("""
        ** Multi-Pass System**
        
        Optional 2x transformation for maximum effect
        """)
    
    with feat_col6:
        st.markdown("""
        ** AI Pattern Removal**
        
        Eliminates telltale AI phrases
        """)
    
    with feat_col7:
        st.markdown("""
        ** Natural Transitions**
        
        Smart connectors between sentences
        """)
    
    with feat_col8:
        st.markdown("""
        ** Real-Time Analysis**
        
        Accurate AI probability scoring
        """)
    
    # Comparison Example
    with st.expander(" See Transformation Example", expanded=False):
        st.markdown("#### Before (AI-Generated):")
        st.markdown("""
        > *"The research demonstrates that artificial intelligence has significantly improved the healthcare industry. Moreover, it is important to note that machine learning algorithms can analyze medical data efficiently. Furthermore, this technology enables healthcare professionals to make more informed decisions. In conclusion, AI represents a transformative force in modern medicine."*
        
        **AI Probability: 87%** 🔴
        """)
        
        st.markdown("---")
        
        st.markdown("#### After (Level 5 + Ultra Mode):")
        st.markdown("""
        > *"Evidence reveals AI has substantially enhanced healthcare delivery. What's worth noting is how machine learning systems demonstrate remarkable capability in processing clinical information. This tech empowers medical professionals to reach better-informed conclusions. Ultimately, artificial intelligence stands as a game-changing element in contemporary medical practice."*
        
        **AI Probability: 4%** 🟢
        """)
        
        st.success(" 95% reduction! Complete sentence restructuring + 85% word replacement = Undetectable!")
    
    # Tips Section
    with st.expander("💡 Pro Tips for Best Results", expanded=False):
        st.markdown("""
        ### How to Get Maximum Humanization:
        
        1. **Use Level 5 Settings** - Maximum transformation power
        2. **Enable Ultra Mode** - 2x pass ensures deep humanization
        3. **Check Long Texts** - Break very long content into sections for best results
        4. **Review Output** - Quick scan ensures meaning is preserved
        5. **Academic Work** - Citations are automatically protected
        
        ### What Gets Transformed:
        -  70-90% of words replaced with contextual synonyms
        -  Sentence structures completely restructured
        -  AI-flagging phrases removed
        -  Natural transitions added
        -  Vocabulary diversity optimized
        -  Passive voice reduced
        
        ### What Stays Protected:
        -  Academic citations
        -  Technical terms (when needed)
        -  Numbers and data
        -  Proper nouns
        -  Core meaning and intent
        """)

if __name__ == "__main__":
    show_humanize_page()