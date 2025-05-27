#!/usr/bin/env python3

"""
Test completions in different contexts to see Fin* commands.
"""

import sys
from pathlib import Path

# Add current directory to path
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from completions import get_contextual_completions
from lsprotocol.types import CompletionItemKind

def test_context(context_name, test_code, line_num, char_num):
    print(f"\n{context_name}")
    print("=" * 50)
    
    completions = get_contextual_completions(test_code, line_num, char_num)
    
    target_commands = [
        "FinPara", "FinSegun", "FinSi", "FinMientras", "Repetir",
        "BorrarPantalla", "EsperarTecla"
    ]
    
    found_targets = []
    for completion in completions:
        if completion.label in target_commands:
            found_targets.append(completion)
    
    print(f"Found {len(found_targets)} target commands:")
    for completion in found_targets:
        print(f"  {completion.label:15} -> {completion.kind}")
        if completion.kind == CompletionItemKind.Function:
            print(f"    ⚠️  WARNING: Function type may trigger ()")
        elif completion.kind == CompletionItemKind.Keyword:
            print(f"    ✅ OK: Keyword type - no automatic ()")

def main():
    # Test 1: Inside a simple process
    test_context("Inside Process", 
                """Proceso Test
    Definir x Como Entero
    """, 2, 4)
    
    # Test 2: Inside a Si block
    test_context("Inside Si block",
                """Proceso Test
    Si x > 0 Entonces
        Escribir "Positivo"
        """, 3, 8)
    
    # Test 3: Inside a Para block
    test_context("Inside Para block",
                """Proceso Test
    Para i <- 1 Hasta 10 Hacer
        Escribir i
        """, 3, 8)
    
    # Test 4: Inside a Mientras block
    test_context("Inside Mientras block",
                """Proceso Test
    Mientras x > 0 Hacer
        x <- x - 1
        """, 3, 8)
    
    # Test 5: Inside a Segun block
    test_context("Inside Segun block",
                """Proceso Test
    Segun x Hacer
        Caso 1:
            Escribir "Uno"
            """, 4, 12)

if __name__ == "__main__":
    main()
