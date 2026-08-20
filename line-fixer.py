#!/usr/bin/env python3
"""Line Fixer - Normalize text files (line endings, trailing spaces, etc.)

Normalizes:
- Line endings (CRLF -> LF)  
- Trailing whitespace removal
- Blank line handling (consecutive blanks -> single blank)
- Encoding detection and conversion to UTF-8

Pure Python, no external dependencies.

Usage:
  python3 line-fixer.py input.txt output.txt [--in-place]

Examples:
  python3 line-fixer.sh logs/app.log --clean
"""

import argparse
import os


def read_file(path):
    """Read file with UTF-8 fallback."""
    try:
        # First try UTF-8
        content = open(path, 'r', encoding='utf-8').read()
        return content
    except UnicodeDecodeError:
        # Fall back to Latin-1 (always works) and re-encode as UTF-8
        try:
            raw = open(path, 'rb').read()
            content = raw.decode('latin-1').encode('utf-8').decode('utf-8')
            return content.replace('\n', '\r\n')  # Assume it might be Windows lines
        except Exception as e:
            raise SystemExit(f'Error reading {path}: {e}')


def normalize_content(content):
    """Normalize line endings and whitespace."""
    
    # Convert CRLF to LF (Unix standard)
    content = content.replace('\r\n', '\n')
    content = content.replace('\r', '\n')  # Handle old Mac OS lines
    
    # Remove trailing whitespace from each line
    lines = content.splitlines()
    normalized_lines = [line.rstrip() for line in lines]
    
    # Collapse consecutive blank lines to single blank
    result_lines = []
    prev_blank = False
    
    for line in normalized_lines:
        is_blank = line == ''
        
        if is_blank and not prev_blank:  # Add only first of consecutive blanks
            result_lines.append(line)
        
        prev_blank = is_blank
    
    content = '\n'.join(result_lines) + '\n' if normalized_lines else '\n'
    
    return content


def write_file(path, content):
    """Write content to file with proper encoding."""
    try:
        open(path, 'w', encoding='utf-8').write(content)
        return True
    except Exception as e:
        raise SystemExit(f'Error writing {path}: {e}')


def main():
    parser = argparse.ArgumentParser(description='Normalize text files (line endings, trailing spaces)')
    
    parser.add_argument('input', help='Input file path or - for stdin')
    
    parser.add_argument('-o', '--output', metavar='FILE', default=None, 
                       help='Output file (omit for stdout)')
    
    parser.add_argument('--in-place', action='store_true',
                       help='Overwrite input file instead of writing to output')
    
    parser.add_argument('--show-diff', action='store_true',
                       help='Print changes before writing')
    
    args = parser.parse_args()

    # Read input  
    try:
        if args.input == '-':
            content = sys.stdin.read()
        else:
            content = read_file(args.input)
    except SystemExit as e:
        raise
    
    # Normalize
    normalized = normalize_content(content)
    
    # Handle output
    if args.output is None and not args.in_place:
        # Write to stdout
        print(normalized, end='')
        
    elif args.in_place:
        write_file(args.input, normalized)
        print(f'Fixed {args.input}')
    
    else:
        write_file(args.output, normalized)
        print(f'Fixed {args.input} -> {args.output}')


if __name__ == '__main__':  
    main()
