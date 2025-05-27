#!/usr/bin/env python3

"""
Test script to check completion behavior for the specific commands mentioned.
"""

from completions import get_contextual_completions, PSEINT_KEYWORDS_DEFINITIONS
from lsprotocol.types import CompletionItemKind

def test_completion_kinds():
    """Test that specific commands have the correct completion item kinds."""
    
    # Commands that should NOT have parentheses (should be Keywords, not Functions)
    parameterless_commands = [
        "FinPara", "FinSegun", "FinSi", "FinMientras", "Repetir",
        "BorrarPantalla", "EsperarTecla", "Milisegundos", "Segundos"
    ]
    
    print("Checking completion item kinds for parameterless commands...")
    print("=" * 60)
    
    for cmd in parameterless_commands:
        if cmd in PSEINT_KEYWORDS_DEFINITIONS:
            kind = PSEINT_KEYWORDS_DEFINITIONS[cmd]["kind"]
            print(f"{cmd:15} -> {kind}")
            
            if kind != CompletionItemKind.Keyword:
                print(f"  ⚠️  ERROR: {cmd} should be Keyword but is {kind}")
            else:
                print(f"  ✅ OK: {cmd} is correctly marked as Keyword")
        else:
            print(f"  ❌ MISSING: {cmd} not found in definitions")
    
    print("\n" + "=" * 60)
    print("Testing contextual completions...")
    
    # Test contextual completions in a simple process
    test_code = """Proceso Test
    Definir x Como Entero
    """
    
    completions = get_contextual_completions(test_code, 2, 4)
    
    print(f"Found {len(completions)} completions")
    
    # Check specific commands in completions
    for completion in completions:
        if completion.label in parameterless_commands:
            print(f"{completion.label:15} -> {completion.kind} (insert: '{completion.insert_text}')")

if __name__ == "__main__":
    test_completion_kinds()
