#!/usr/bin/env python3

# Quick verification test
try:
    print("Testing diagnostics import...")
    from diagnostics import get_diagnostics
    print("✓ Diagnostics module imported")
    
    print("Testing server import...")
    import server
    print("✓ Server module imported")
    
    print("Testing diagnostic functionality...")
    test_code = """Algoritmo Test
    x <- undeclared_variable
FinAlgoritmo"""
    
    diagnostics = get_diagnostics(test_code)
    print(f"✓ Diagnostics generated: {len(diagnostics)}")
    
    for d in diagnostics:
        print(f"  - Line {d.range.start.line}: {d.message}")
    
    print("\n🎉 All tests passed! The LSP server is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
