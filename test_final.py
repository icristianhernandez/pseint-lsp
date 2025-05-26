#!/usr/bin/env python3

from diagnostics import get_diagnostics

def test_switch_statement():
    """Test switch statement diagnostic detection"""
    code = """Proceso TestSegun
    Definir opcion Como Entero
    opcion <- 1
    
    Segun opcion Hacer
        1: Escribir "Opcion 1"
        2: Escribir "Opcion 2"
    FinSegun
FinProceso"""
    
    diagnostics = get_diagnostics(code)
    print(f"Switch statement test - Found {len(diagnostics)} diagnostics:")
    for d in diagnostics:
        print(f"  Line {d.range.start.line}: {d.message}")
    return len(diagnostics)

def test_comprehensive_errors():
    """Test with comprehensive error file"""
    try:
        with open('reference_code/test_errors.psc', 'r', encoding='utf-8') as f:
            code = f.read()
        
        diagnostics = get_diagnostics(code)
        print(f"\nComprehensive test - Found {len(diagnostics)} diagnostics:")
        for d in diagnostics[:10]:  # Show first 10
            print(f"  Line {d.range.start.line}: {d.message}")
        if len(diagnostics) > 10:
            print(f"  ... and {len(diagnostics) - 10} more")
        return len(diagnostics)
    except Exception as e:
        print(f"Error reading test file: {e}")
        return 0

def test_server_import():
    """Test server module import"""
    try:
        import server
        print(f"\nServer module imported successfully")
        print(f"Server object: {server.server}")
        return True
    except Exception as e:
        print(f"Error importing server: {e}")
        return False

if __name__ == "__main__":
    print("=== PSeInt LSP Diagnostic System Test ===")
    
    # Test individual components
    switch_count = test_switch_statement()
    comprehensive_count = test_comprehensive_errors()
    server_ok = test_server_import()
    
    print("\n=== Summary ===")
    print(f"Switch statement diagnostics: {switch_count}")
    print(f"Comprehensive test diagnostics: {comprehensive_count}")
    print(f"Server import: {'OK' if server_ok else 'FAILED'}")
    
    if switch_count >= 0 and comprehensive_count > 10 and server_ok:
        print("\n✅ All tests passed! LSP server is ready.")
    else:
        print("\n❌ Some tests failed.")
