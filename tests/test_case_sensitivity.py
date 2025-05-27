#!/usr/bin/env python3

"""
Test to verify case sensitivity and exact command names.
"""

import sys
from pathlib import Path

# Add current directory to path
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from src.completions import get_contextual_completions
from lsprotocol.types import CompletionItemKind

def test_case_variations():
    # Test document content
    test_code = """Proceso Test
    Definir x Como Entero
    """
    
    # Get completions at line 2 (inside process)
    completions = get_contextual_completions(test_code, 2, 4)
    
    # Check for case variations of the problematic commands
    target_variations = [
        # Original case
        "FinPara", "FinSegun", "FinSi", "FinMientras", "Repetir",
        "BorrarPantalla", "EsperarTecla",
        # All lowercase
        "finpara", "finsegun", "finsi", "finmientras", "repetir",
        "borrarpantalla", "esperartecla",
        # All uppercase (as mentioned by user)
        "FINPARA", "FINSEGUN", "FINSI", "FINMIENTRAS", "REPETIR",
        "BORRARPANTALLA", "ESPERARTECLA"
    ]
    
    print("Checking for all case variations:")
    print("=" * 50)
    
    found_any = {}
    for completion in completions:
        label_lower = completion.label.lower()
        for target in target_variations:
            if completion.label == target:
                if target not in found_any:
                    found_any[target] = []
                found_any[target].append(completion)
    
    for target in target_variations:
        if target in found_any:
            for completion in found_any[target]:
                print(f"{target:15} -> {completion.kind}")
        else:
            print(f"{target:15} -> NOT FOUND")
    
    print("\nAll exact matches found:")
    print("=" * 50)
    
    original_targets = [
        "FinPara", "FinSegun", "FinSi", "FinMientras", "Repetir",
        "BorrarPantalla", "EsperarTecla"
    ]
    
    for completion in completions:
        if completion.label in original_targets:
            result = "✅ KEYWORD" if completion.kind == CompletionItemKind.Keyword else "⚠️  FUNCTION"
            print(f"{completion.label:15} -> {result}")

if __name__ == "__main__":
    test_case_variations()
