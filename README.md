# Line Fixer CLI

Normalize text files (line endings, trailing spaces) in pure Python.

## What It Does

`line-fixer.py` normalizes:
- Line endings (CRLF -> LF)  
- Trailing whitespace removal
- Blank line handling (consecutive blanks -> single blank)  
- Encoding conversion to UTF-8

Pure Python, no external deps.

## Usage

```bash
# Normalize a file to stdout
python3 line-fixer.py logs/app.log

# Write output to different file
python3 line-fixer.py input.txt --output clean.txt

# Fix in-place
python3 line-fixer.py myapp.log --in-place
```

## Examples

### Clean Log File

```bash
python3 line-fixer.py logs/app.log \
  --output /etc/clean-logs/app.log
```

Converts Windows-style CRLF to Unix LF format.

### Normalize Code Files

Before git commit, fix all files:

```bash
find . -name "*.py" -exec python3 line-fixer.py {} +
```

## Implementation Notes

- **UTF-8 fallback**: Reads Latin-1 if UTF-8 fails, then preserves content
- **Line-ending handling**: Converts CRLF and old Mac CR to LF  
- **Blank line collapse**: Reduces consecutive empty lines to single blank
- **Trailing space removal**: Essential for diff-friendly commits

Pure Python makes it portable—works on Linux, macOS, Windows.

## Support

If you find this useful, you can support development: https://www.buymeacoffee.com/poolion