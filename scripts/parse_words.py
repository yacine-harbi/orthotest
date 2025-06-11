#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to parse words_flac.json and create a categorized words_dictionary.json file.
Categorizes French words by difficulty level: facile, moyen, difficile.
"""

import json
import re
from typing import Dict, Tuple

def count_syllables(word: str) -> int:
    """
    Estimate syllable count for French words.
    This is a simplified approach based on vowel patterns.
    """
    # Remove accents and convert to lowercase for counting
    word_clean = word.lower()
    # Count vowel groups (approximate syllable count)
    vowels = 'aeiouyàáâäèéêëìíîïòóôöùúûü'
    syllable_count = 0
    prev_was_vowel = False
    
    for char in word_clean:
        if char in vowels:
            if not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = True
        else:
            prev_was_vowel = False
    
    # Adjust for silent 'e' at the end
    if word_clean.endswith('e') and syllable_count > 1:
        syllable_count -= 1
    
    return max(1, syllable_count)  # At least 1 syllable

def is_technical_term(word: str) -> bool:
    """
    Check if a word is likely a technical or scientific term.
    """
    technical_patterns = [
        r'.*tion$',      # -tion endings
        r'.*sion$',      # -sion endings
        r'.*ique$',      # -ique endings (scientific)
        r'.*logie$',     # -logie endings
        r'.*graphie$',   # -graphie endings
        r'.*métrie$',    # -métrie endings
        r'.*scope$',     # -scope endings
        r'.*phage$',     # -phage endings
        r'.*gène$',      # -gène endings
        r'.*pathie$',    # -pathie endings
        r'.*thérapie$',  # -thérapie endings
    ]
    
    word_lower = word.lower()
    return any(re.match(pattern, word_lower) for pattern in technical_patterns)

def has_complex_spelling(word: str) -> bool:
    """
    Check if a word has complex spelling patterns.
    """
    complex_patterns = [
        r'.*cc.*',       # double c
        r'.*mm.*',       # double m
        r'.*nn.*',       # double n
        r'.*ff.*',       # double f
        r'.*ll.*',       # double l
        r'.*rr.*',       # double r
        r'.*ss.*',       # double s
        r'.*tt.*',       # double t
        r'.*pp.*',       # double p
        r'.*ph.*',       # ph combination
        r'.*th.*',       # th combination
        r'.*ch.*',       # ch combination
        r'.*gn.*',       # gn combination
        r'.*qu.*',       # qu combination
        r'.*x.*',        # contains x
        r'.*y.*',        # contains y
        r'.*w.*',        # contains w
    ]
    
    word_lower = word.lower()
    complex_count = sum(1 for pattern in complex_patterns if re.search(pattern, word_lower))
    return complex_count >= 2  # Multiple complex patterns

def categorize_word(word: str) -> str:
    """
    Categorize a French word by difficulty level.
    
    Args:
        word: The French word or phrase to categorize
        
    Returns:
        Difficulty level: 'facile', 'moyen', or 'difficile'
    """
    # Handle phrases (multiple words)
    words = word.strip().split()
    
    if len(words) > 1:
        # For phrases, categorize based on complexity
        total_length = len(word.replace(' ', ''))
        avg_word_length = total_length / len(words)
        
        if len(words) <= 2 and avg_word_length <= 5:
            return 'facile'  # Simple short phrases
        elif len(words) <= 3 and avg_word_length <= 7:
            return 'moyen'   # Medium phrases
        else:
            return 'difficile'  # Complex phrases
    
    # Single word analysis
    single_word = words[0]
    word_length = len(single_word)
    syllable_count = count_syllables(single_word)
    
    # Check for technical terms first
    if is_technical_term(single_word):
        return 'difficile'
    
    # Check for very complex spelling
    if has_complex_spelling(single_word) and word_length > 8:
        return 'difficile'
    
    # Simple words (common criteria)
    if (word_length <= 5 and syllable_count <= 2) or single_word.lower() in [
        'un', 'une', 'le', 'la', 'les', 'de', 'du', 'des', 'et', 'ou', 'où', 
        'qui', 'que', 'quoi', 'avec', 'pour', 'dans', 'sur', 'sous', 'par',
        'chat', 'chien', 'eau', 'feu', 'air', 'terre', 'jour', 'nuit', 'ami',
        'père', 'mère', 'fils', 'fille', 'homme', 'femme', 'enfant', 'bébé',
        'rouge', 'bleu', 'vert', 'jaune', 'noir', 'blanc', 'grand', 'petit',
        'bon', 'mauvais', 'beau', 'laid', 'nouveau', 'vieux', 'jeune',
        'manger', 'boire', 'dormir', 'marcher', 'courir', 'voir', 'entendre',
        'parler', 'écouter', 'regarder', 'sentir', 'toucher', 'aimer',
        'maison', 'école', 'travail', 'voiture', 'train', 'avion', 'livre',
        'pain', 'lait', 'viande', 'fruit', 'légume', 'temps', 'argent'
    ]:
        return 'facile'
    
    # Difficult words (complex criteria)
    if (word_length > 12 or 
        syllable_count > 4 or 
        is_technical_term(single_word) or
        has_complex_spelling(single_word)):
        return 'difficile'
    
    # Medium words (everything else)
    return 'moyen'

def parse_words_file(input_file: str = 'words_flac.json', output_file: str = 'words_dictionary.json') -> None:
    """
    Parse the words_flac.json file and create a categorized words_dictionary.json file.
    
    Args:
        input_file: Path to the input JSON file
        output_file: Path to the output JSON file
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
        
        print(f"Loaded {len(words_data)} entries from {input_file}")
        
        # Initialize categorized dictionary
        categorized_words = {
            'facile': {},
            'moyen': {},
            'difficile': {}
        }
        
        # Process each word
        for filename, word in words_data.items():
            difficulty = categorize_word(word)
            categorized_words[difficulty][filename] = word
            
        # Print statistics
        print(f"\nCategorization complete:")
        print(f"  Facile: {len(categorized_words['facile'])} words")
        print(f"  Moyen: {len(categorized_words['moyen'])} words")
        print(f"  Difficile: {len(categorized_words['difficile'])} words")
        print(f"  Total: {sum(len(cat) for cat in categorized_words.values())} words")
        
        # Write the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(categorized_words, f, ensure_ascii=False, indent=2)
        
        print(f"\nCategorized dictionary saved to {output_file}")
        
        # Show some examples from each category
        print("\nExamples from each category:")
        for difficulty, words in categorized_words.items():
            if words:
                print(f"\n{difficulty.upper()}:")
                # Show first 5 examples
                for i, (filename, word) in enumerate(list(words.items())[:5]):
                    print(f"  {filename}: \"{word}\"")
                if len(words) > 5:
                    print(f"  ... and {len(words) - 5} more")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        print("Make sure the file exists in the current directory.")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("French Words Categorizer")
    print("=" * 50)
    parse_words_file()