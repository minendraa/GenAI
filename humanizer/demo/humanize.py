# humanizer.py
import random
import re
import nltk

# --- NEW Self-Healing Code Block ---
# This block checks if the 'punkt' tokenizer data is available.
# If not, it downloads it automatically.
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("NLTK 'punkt' model not found. Downloading now...")
    nltk.download('punkt')
    print("Download complete.")
# ------------------------------------


# --- CONFIGURATION ---

# 1. Dictionary of common "AI-sounding" words and their simpler, more human alternatives.
COMPLEX_TO_SIMPLE_WORDS = {
    "utilize": "use",
    "leverage": "use",
    "facilitate": "help",
    "subsequently": "later",
    "commence": "start",
    "ascertain": "find out",
    "endeavor": "try",
    "myriad": "many",
    "delve into": "look at",
    "a testament to": "proof of",
    "it is crucial": "it's important",
    "it is imperative": "we must",
    "navigate the complexities of": "handle",
    "meticulously": "carefully",
    "furthermore": "also",
    "in addition": "plus",
    "therefore": "so",
}

# 2. Map for creating contractions to make text sound more conversational.
CONTRACTION_MAP = {
    "is not": "isn't",
    "are not": "aren't",
    "cannot": "can't",
    "do not": "don't",
    "does not": "doesn't",
    "have not": "haven't",
    "will not": "won't",
    "it is": "it's",
    "he is": "he's",
    "she is": "she's",
    "that is": "that's",
    "what is": "what's",
    "who is": "who's",
    "you are": "you're",
    "they are": "they're",
    "we are": "we're",
}

def simplify_vocabulary(text: str) -> str:
    """Replaces complex or overly formal words with simpler alternatives."""
    for complex_word, simple_word in COMPLEX_TO_SIMPLE_WORDS.items():
        # Use regex with word boundaries (\b) to avoid replacing parts of words
        # e.g., don't replace "commence" in "commencement"
        text = re.sub(r'\b' + re.escape(complex_word) + r'\b', simple_word, text, flags=re.IGNORECASE)
    return text

def add_contractions(text: str) -> str:
    """Adds contractions to make the text sound more natural."""
    for long_form, contraction in CONTRACTION_MAP.items():
        text = re.sub(r'\b' + re.escape(long_form) + r'\b', contraction, text, flags=re.IGNORECASE)
    return text

def vary_sentence_structure(text: str) -> str:
    """
    Introduces variation into sentence length to increase "burstiness".
    - Merges some consecutive short sentences.
    - This is a simplified approach. A more advanced version would also split long sentences.
    """
    sentences = nltk.sent_tokenize(text)
    if len(sentences) < 2:
        return text

    new_sentences = []
    i = 0
    while i < len(sentences):
        current_sentence = sentences[i]
        
        # Check if we can merge this sentence with the next one
        # Condition: both are short and we decide to merge based on a random chance
        if i + 1 < len(sentences):
            next_sentence = sentences[i+1]
            # Merge if both sentences are short (e.g., < 12 words) and a 50% chance occurs
            if len(current_sentence.split()) < 12 and len(next_sentence.split()) < 12 and random.choice([True, False]):
                # Combine sentences. Remove the period from the first and lowercase the second.
                merged_sentence = current_sentence.rstrip(' .?!') + ", and " + next_sentence[0].lower() + next_sentence[1:]
                new_sentences.append(merged_sentence)
                i += 2  # Skip the next sentence as it has been merged
                continue

        new_sentences.append(current_sentence)
        i += 1
        
    return " ".join(new_sentences)

def humanize_text(text: str) -> str:
    """
    Applies a series of transformations to make text sound less like AI.
    The order of operations can matter.
    """
    # 1. Start with major structural changes
    humanized_text = vary_sentence_structure(text)
    
    # 2. Then, simplify the language
    humanized_text = simplify_vocabulary(humanized_text)
    
    # 3. Finally, add conversational touches
    humanized_text = add_contractions(humanized_text)
    
    return humanized_text