#!/usr/bin/env python3

"""
Simple test to check completion generation directly.
"""

import sys
from pathlib import Path

# Add current directory to path
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from completions import get_contextual_completions, PSEINT_KEYWORDS_DEFINITIONS
from lsprotocol.types import CompletionItemKind

def main():
    # Test document content
    test_code = """Proceso Test
    Definir x Como Entero
    """
    
    # Get completions at line 2 (inside process)
    completions = get_contextual_completions(test_code, 2, 4)
    
    print(f"Total completions: {len(completions)}")
    
    # Check the specific problematic commands
    target_commands = [
        "FinPara", "FinSegun", "FinSi", "FinMientras", "Repetir",
        "BorrarPantalla", "EsperarTecla"
    ]
    
    print("\nChecking problematic commands:")
    print("-" * 50)
    
    for completion in completions:
        if completion.label in target_commands:
            # Print details about this completion
            print(f"Label: {completion.label}")
            print(f"  Kind: {completion.kind}")
            print(f"  Insert Text: '{completion.insert_text}'")
            print(f"  Insert Format: {completion.insert_text_format}")
            
            # Check if this would trigger parentheses
            if completion.kind == CompletionItemKind.Function:
                print(f"  ⚠️  WARNING: Marked as Function - LSP clients may add ()")
            elif completion.kind == CompletionItemKind.Keyword:
                print(f"  ✅ OK: Marked as Keyword - no automatic ()")
            print()
    
    # Also check for any duplicate or conflicting definitions
    print("\nAll completions containing target commands:")
    print("-" * 50)
    
    for completion in completions:
        label_lower = completion.label.lower()
        for target in target_commands:
            if target.lower() in label_lower or label_lower in target.lower():
                print(f"{completion.label} -> {completion.kind} -> '{completion.insert_text}'")

if __name__ == "__main__":
    main()
