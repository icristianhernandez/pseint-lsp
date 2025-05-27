#!/usr/bin/env python3

"""
Test script to simulate LSP client completion behavior and check for parentheses issues.
"""

import asyncio
from pathlib import Path
import tempfile
import sys

# Ensure we can import from the current directory
script_dir = Path(__file__).parent.absolute()
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

from lsprotocol.types import (
    CompletionParams, Position, TextDocumentIdentifier,
    InitializeParams, CompletionItemKind
)
from src.server import server

async def test_completion_behavior():
    """Test the actual completion behavior from the LSP server."""
    
    # Initialize the server
    init_params = InitializeParams(
        root_uri="file:///tmp",
        capabilities={}
    )
    
    result = server.lsp.initialize(init_params)
    print(f"Server initialized: {result.server_info.name} v{result.server_info.version}")
    print("Completion provider enabled:", result.capabilities.completion_provider is not None)
    
    # Create a test document content
    test_content = """Proceso Test
    Definir x Como Entero
    
FinProceso"""
    
    # Create a temporary document
    with tempfile.NamedTemporaryFile(mode='w', suffix='.psc', delete=False) as f:
        f.write(test_content)
        f.flush()
        
        doc_uri = f"file://{f.name}"
        
        # Simulate opening the document
        server.workspace.put_document(doc_uri, test_content)
        
        # Test completion at line 2 (inside the process)
        completion_params = CompletionParams(
            text_document=TextDocumentIdentifier(uri=doc_uri),
            position=Position(line=2, character=4)  # After some indentation
        )
        
        try:
            # Get completions
            completion_result = await server.lsp.text_document_completion(completion_params)
            
            print(f"\nFound {len(completion_result.items)} completion items")
            print("=" * 60)
            
            # Check specific items we're interested in
            target_items = [
                "FinPara", "FinSegun", "FinSi", "FinMientras", "Repetir",
                "BorrarPantalla", "EsperarTecla", "Milisegundos", "Segundos"
            ]
            
            found_items = {}
            for item in completion_result.items:
                if item.label in target_items:
                    found_items[item.label] = item
            
            print("Target completion items:")
            for label in target_items:
                if label in found_items:
                    item = found_items[label]
                    print(f"{label:15} -> Kind: {item.kind:20} Insert: '{item.insert_text}'")
                    
                    # Check if this would cause inappropriate parentheses
                    if item.kind == CompletionItemKind.Function:
                        print(f"  ⚠️  WARNING: {label} is marked as Function - may trigger ()")
                    elif item.kind == CompletionItemKind.Keyword:
                        print(f"  ✅ OK: {label} is marked as Keyword - no ()")
                else:
                    print(f"{label:15} -> NOT FOUND")
            
            # Also check if there are any functions that might be problematic
            print("\nAll Function-type completions:")
            for item in completion_result.items:
                if item.kind == CompletionItemKind.Function:
                    print(f"  {item.label} -> {item.insert_text}")
                    
        except Exception as e:
            print(f"Error getting completions: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_completion_behavior())
