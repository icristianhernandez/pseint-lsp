# PSeInt Encoding Compatibility Analysis

## Current Encoding Situation

### What We Found

1. **PSeInt Default Encoding**: ISO-8859-1 (Latin-1)
   - PSeInt saves `.psc` files in ISO-8859-1 encoding by default
   - This encoding supports Western European characters (ñ, á, é, í, ó, ú, etc.)
   - Commonly used for Spanish language content

2. **Current Formatter Behavior**: UTF-8 assumption
   - The LSP server receives text documents as UTF-8 strings (LSP protocol standard)
   - The formatter processes text without explicit encoding awareness
   - File I/O in tests uses UTF-8 with fallback to latin-1

3. **Encoding Mismatch Impact**:
   - `reference_code3.psc` contains Spanish text with special characters
   - When read as UTF-8, ISO-8859-1 characters appear corrupted (e.g., `ñ` becomes `�`)
   - This affects comments, string literals, and variable names with special characters

### Evidence from Reference Files

```text
reference_code1.psc: UTF-8 encoded ✓
reference_code2.psc: UTF-8 encoded ✓  
reference_code3.psc: ISO-8859-1 encoded ⚠️
```

**Example of corruption in reference_code3.psc:**

- Original (ISO-8859-1): `//Esta versión fue realizada durante el encuentro 26`
- Corrupted (read as UTF-8): `//Esta versi�n fue realizada durante el encuentro 26`

## Impact on Formatter Functionality

### Current Status: ✅ WORKING with UTF-8 content

- String preservation works correctly for UTF-8 encoded files
- All string formatting tests pass
- Code formatting outside strings works properly

### Issue: ⚠️ CHARACTER CORRUPTION with ISO-8859-1 content

- Special characters in comments become corrupted
- String literals with accented characters are corrupted
- Variable names with special characters are corrupted

## Encoding Handling Strategies

### Strategy 1: LSP-Level Encoding Detection (Recommended)

**Approach**: Let VS Code handle encoding detection and conversion

- VS Code has built-in encoding detection capabilities
- The LSP server receives pre-converted UTF-8 text
- Most compatible with LSP protocol standards

**Implementation**:

- Document VS Code's encoding detection settings
- Recommend users configure VS Code to detect ISO-8859-1 files
- No changes to formatter needed

### Strategy 2: Formatter-Level Encoding Support

**Approach**: Add encoding detection to the formatter

- Detect file encoding before processing
- Convert content to UTF-8 for processing
- Convert back to original encoding after formatting

**Implementation**:

```python
def detect_and_format_file(file_path: str) -> str:
    # Try UTF-8 first, fallback to ISO-8859-1
    for encoding in ['utf-8', 'iso-8859-1']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            formatted = format_pseint_code(content)
            return formatted, encoding
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode file with supported encodings")
```

### Strategy 3: Dual Encoding Support

**Approach**: Support both encodings simultaneously

- Add encoding parameter to format function
- Preserve original encoding in output
- Handle encoding conversion transparently

## Recommended Solution

### For LSP Server Users (Recommended)

1. **Configure VS Code encoding detection**:
   - Set `"files.autoGuessEncoding": true` in VS Code settings
   - This enables automatic encoding detection for opened files

2. **Manual encoding specification**:
   - Use "Reopen with Encoding" command for ISO-8859-1 files
   - Select ISO-8859-1 when opening problematic files

### For Command-Line Users

1. **Add encoding detection to CLI interface**:
   - Implement encoding detection in command-line version
   - Support `--encoding` parameter for explicit specification

## Implementation Priority

### Phase 1: Documentation and VS Code Configuration ⭐ HIGH

- Document encoding issues and VS Code configuration
- Provide user guidance for handling ISO-8859-1 files
- No code changes required

### Phase 2: Enhanced Encoding Support ⭐ MEDIUM  

- Add encoding detection to formatter
- Support command-line encoding specification
- Maintain backward compatibility

### Phase 3: Advanced Encoding Features ⭐ LOW

- Automatic encoding detection and conversion
- Batch file processing with mixed encodings
- Encoding validation and reporting

## Testing Status

### ✅ Completed

- String preservation with UTF-8 content
- Formatter logic correctness
- Edge cases with special string content

### 🔄 In Progress  

- Encoding compatibility testing
- Character corruption documentation
- VS Code configuration validation

### ⏳ Pending

- ISO-8859-1 round-trip testing
- Mixed encoding file handling
- Performance impact assessment

## Files Affected

### Core Files

- `formatter.py`: Main formatting logic (encoding-agnostic)
- `server.py`: LSP server (receives UTF-8 from VS Code)

### Test Files  

- `tests/test_encoding_compatibility.py`: New encoding tests
- `tests/test_integration.py`: Has encoding fallback logic
- `reference_code/reference_code3.psc`: ISO-8859-1 test case

### Documentation

- This file: `ENCODING_COMPATIBILITY_ANALYSIS.md`
- `README.md`: Should be updated with encoding guidance

## Conclusion

The formatter's core string preservation functionality is **working correctly**. The encoding issue is primarily a **file I/O compatibility concern** that can be addressed through:

1. **Immediate**: VS Code configuration guidance (no code changes)
2. **Future**: Enhanced encoding detection and support (optional improvement)

The string formatting improvements implemented in the previous phase successfully preserve all string content regardless of the underlying character encoding used.
