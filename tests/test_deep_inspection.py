#!/usr/bin/env python3

"""
Deep inspection of completion items to find any issues.
"""

import sys
from pathlib import Path

# Add current directory to path
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from src.completions import (
    get_contextual_completions, 
    PSEINT_KEYWORDS_DEFINITIONS, 
    ALL_KEYWORD_COMPLETION_ITEMS,
    ALL_SNIPPET_COMPLETION_ITEMS
)
from lsprotocol.types import CompletionItemKind

def main():
    # Check all keyword definitions for the target commands
    target_commands = [
        "FinPara", "FinSegun", "FinSi", "FinMientras", "Repetir",
        "BorrarPantalla", "EsperarTecla", "Milisegundos", "Segundos"
    ]
    
    print("Checking raw PSEINT_KEYWORDS_DEFINITIONS:")
    print("=" * 60)
    
    for cmd in target_commands:
        if cmd in PSEINT_KEYWORDS_DEFINITIONS:
            definition = PSEINT_KEYWORDS_DEFINITIONS[cmd]
            print(f"{cmd:15} -> {definition['kind']} | {definition['doc']}")
        else:
            print(f"{cmd:15} -> NOT FOUND")
    
    print("\nChecking ALL_KEYWORD_COMPLETION_ITEMS:")
    print("=" * 60)
    
    for item in ALL_KEYWORD_COMPLETION_ITEMS:
        if item.label in target_commands:
            print(f"{item.label:15} -> {item.kind} | Insert: '{item.insert_text}'")
            print(f"{'':15}    Format: {item.insert_text_format}")
    
    print("\nChecking for ANY Function-type items with these labels:")
    print("=" * 60)
    
    # Check if there are any functions with the same name
    all_functions = [item for item in ALL_KEYWORD_COMPLETION_ITEMS 
                     if item.kind == CompletionItemKind.Function]
    
    for item in all_functions:
        if any(target.lower() in item.label.lower() or 
               item.label.lower() in target.lower() 
               for target in target_commands):
            print(f"Function: {item.label} -> {item.insert_text}")
    
    print("\nChecking for duplicates or conflicts:")
    print("=" * 60)
    
    # Look for any duplicate labels
    all_labels = [item.label for item in ALL_KEYWORD_COMPLETION_ITEMS]
    label_counts = {}
    for label in all_labels:
        label_counts[label] = label_counts.get(label, 0) + 1
    
    for label, count in label_counts.items():
        if count > 1 and label in target_commands:
            print(f"DUPLICATE: {label} appears {count} times")
    
    # Check snippet items for conflicts
    print("\nChecking snippet items for conflicts:")
    print("=" * 60)
    
    for item in ALL_SNIPPET_COMPLETION_ITEMS:
        if any(target.lower() in item.label.lower() for target in target_commands):
            print(f"Snippet: {item.label} -> {item.kind}")

if __name__ == "__main__":
    main()
