# PSeInt LSP Formatter Test Suite Documentation

## Overview

This document describes the comprehensive test suite for the PSeInt LSP formatter, organized by categories and preserved for future development and regression testing.

## Test Categories

### 1. Core Formatter Tests ⚙️

**Purpose**: Test the fundamental formatting logic and algorithms.

- **`test_formatter.py`**: Core formatting functionality
  - Keyword casing (Proceso, FinProceso, etc.)
  - Indentation logic
  - Operator spacing
  - Comment preservation
  - Basic string handling

- **`test_edge_cases.py`**: Edge cases and boundary conditions
  - Empty files
  - Files with only comments
  - Malformed code structures
  - Unusual spacing patterns

### 2. String Formatting Tests 🔤

**Purpose**: Comprehensive testing of string content preservation during formatting.

- **`test_string_formatting.py`**: Advanced string preservation
  - ASCII art preservation
  - Whitespace patterns in strings
  - Keywords inside strings (should not be changed)
  - Operators inside strings (should not be spaced)
  - Special characters and encoding
  - Multi-line string handling
  - 16 comprehensive test cases covering all string scenarios

### 3. Integration Tests 🔗

**Purpose**: Test formatter with real-world PSeInt code and complete workflows.

- **`test_integration.py`**: Integration with reference files
  - Tests with `reference_code1.psc`, `reference_code2.psc`, `reference_code3.psc`
  - End-to-end formatting verification
  - File encoding fallback handling

- **`test_comprehensive_integration.py`**: Complete reference code testing
  - Full battleship game code formatting
  - Complex nested structures
  - Real-world code complexity testing
  - Output verification

- **`test_real_world_code.py`**: Specific real-world scenarios
  - ASCII art sections
  - Complex string literals
  - University project code structures
  - Practical formatting verification

### 4. Server Tests 🖥️

**Purpose**: Test the LSP server functionality and protocol compliance.

- **`test_server.py`**: LSP server functionality
  - Server initialization
  - Document formatting requests
  - LSP protocol compliance
  - Error handling
  - Client-server communication

### 5. Encoding Compatibility 🌍

**Purpose**: Test encoding handling and international character support.

- **`test_encoding_compatibility.py`**: Formal encoding tests
  - UTF-8 vs ISO-8859-1 handling
  - Spanish special characters (ñ, á, é, í, ó, ú)
  - Round-trip encoding conversion
  - Character preservation verification

- **`test_encoding_investigation.py`**: Encoding debugging and analysis
  - File encoding detection
  - Character corruption investigation
  - Encoding conversion testing
  - Diagnostic output for troubleshooting

## Test Execution

### Run All Tests

```bash
cd tests/
python run_all_tests.py
```

### Run Individual Test Categories

```bash
# Core formatter tests
python -m pytest test_formatter.py test_edge_cases.py -v

# String formatting tests
python -m pytest test_string_formatting.py -v

# Integration tests
python -m pytest test_integration.py test_comprehensive_integration.py test_real_world_code.py -v

# Server tests
python -m pytest test_server.py -v

# Encoding tests
python -m pytest test_encoding_compatibility.py test_encoding_investigation.py -v
```

### Run Specific Test Files

```bash
python -m pytest test_string_formatting.py::TestStringFormatting::test_ascii_art_preservation -v
```

## Test Status Summary

### ✅ Fully Implemented and Passing

- Core formatter functionality
- String content preservation
- Real-world code integration
- ASCII art and complex strings
- Basic LSP server operations

### 🔄 Implemented with Known Issues

- Encoding compatibility (requires VS Code configuration)
- ISO-8859-1 file handling (documented workarounds)

### 📋 Test Coverage Metrics

- **String Formatting**: 16 comprehensive test cases
- **Integration Testing**: 3 reference files + real-world scenarios
- **Edge Cases**: Multiple boundary conditions covered
- **Encoding**: UTF-8 and ISO-8859-1 compatibility tested

## Key Testing Achievements

### 1. String Preservation Revolution 🎯

- **Problem Solved**: Formatter was corrupting string content
- **Solution**: String-boundary-aware formatting functions
- **Tests**: 16 specific test cases covering all string scenarios
- **Result**: 100% string content preservation

### 2. Real-World Validation ✅

- **Tested With**: Actual PSeInt battleship game code
- **Complexity**: 1000+ lines with ASCII art, complex strings
- **Verification**: Character-by-character content preservation
- **Outcome**: Production-ready formatting

### 3. Encoding Compatibility Analysis 🌐

- **Investigation**: ISO-8859-1 vs UTF-8 handling
- **Documentation**: Complete encoding compatibility guide
- **Workarounds**: VS Code configuration solutions
- **Future-Proofing**: Tests ready for enhanced encoding support

## Test File Organization

```text
tests/
├── run_all_tests.py                 # Comprehensive test runner
├── test_formatter.py                # Core formatting logic
├── test_edge_cases.py               # Boundary conditions
├── test_string_formatting.py        # String preservation (16 tests)
├── test_integration.py              # Reference file integration
├── test_comprehensive_integration.py # Complete code testing
├── test_real_world_code.py          # Real-world scenarios
├── test_server.py                   # LSP server functionality
├── test_encoding_compatibility.py   # Formal encoding tests
└── test_encoding_investigation.py   # Encoding debugging
```

## Regression Testing

These tests serve as a comprehensive regression testing suite:

1. **Before any formatter changes**: Run full test suite
2. **After implementing new features**: Verify all existing tests pass
3. **Before releases**: Complete test validation
4. **When debugging issues**: Use specific test categories

## Future Test Enhancements

### Planned Additions

- Performance benchmarking tests
- Memory usage validation
- Large file handling tests
- Concurrent formatting tests
- Extended encoding support tests

### Test Infrastructure Improvements

- Automated test result reporting
- Code coverage analysis integration
- Continuous integration setup
- Test data management

## Contributing to Tests

When adding new functionality:

1. **Add corresponding tests** in the appropriate category
2. **Update this documentation** with new test descriptions
3. **Ensure all existing tests pass** before submitting changes
4. **Follow naming conventions** for consistency

This test suite represents a significant investment in code quality and reliability, ensuring the PSeInt formatter remains robust and trustworthy across all use cases.
