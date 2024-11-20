#!/usr/bin/env python3

"""
First, create a simple deck in Obsidian.
Next, leverage: "Pandoc Plugin: Export as Beamer Slides"
Finally, convert to PDF via this tool.

usage: obsidian-compile-slides [-h] [--nodracula] [--nomono]

Compile beamer slides with optional Dracula theme

options:
  -h, --help   show this help message and exit
  --nodracula  Disable applying Dracula theme to the slides
  --nomono     Disable using monospace font for all text
"""

import os
import shutil
import re
import subprocess
from pathlib import Path
import argparse

def sanitize_filename(filename):
    """Remove spaces and special characters from filename."""
    return filename.replace(' ', '_')

def copy_and_sanitize_images(tex_content):
    """Copy images to temp directory and update references in tex content."""
    # Create temp attachments directory if it doesn't exist
    temp_dir = Path('_attachments_temp')
    temp_dir.mkdir(exist_ok=True)

    # Find all \includegraphics commands
    img_pattern = r'\\includegraphics\{([^}]+)\}'
    matches = re.finditer(img_pattern, tex_content)

    new_content = tex_content
    for match in matches:
        orig_path = match.group(1)
        # Look for the image in _attachments directory
        orig_img = Path('_attachments') / Path(orig_path).name

        # Create sanitized filename
        new_filename = sanitize_filename(orig_img.name)
        new_path = f"./_attachments_temp/{new_filename}"

        # Copy file if it exists
        if orig_img.exists():
            shutil.copy2(orig_img, temp_dir / new_filename)
            print(f"Copied {orig_img} to {temp_dir / new_filename}")
        else:
            print(f"Warning: Image not found: {orig_img}")

        # Update reference in tex content
        new_content = new_content.replace(orig_path, new_path)

    return new_content

def add_dracula_theme(content):
    """Add Dracula theme colors to beamer presentation."""
    dracula_theme = '''
\\definecolor{draculaBg}{HTML}{282A36}
\\definecolor{draculaFg}{HTML}{F8F8F2}
\\definecolor{draculaComment}{HTML}{6272A4}
\\definecolor{draculaPurple}{HTML}{BD93F9}
\\definecolor{draculaGreen}{HTML}{50FA7B}
\\definecolor{draculaOrange}{HTML}{FFB86C}
\\definecolor{draculaPink}{HTML}{FF79C6}
\\definecolor{draculaRed}{HTML}{FF5555}
\\definecolor{draculaYellow}{HTML}{F1FA8C}
\\definecolor{draculaCyan}{HTML}{8BE9FD}

\\setbeamercolor{normal text}{fg=draculaFg, bg=draculaBg}
\\setbeamercolor{structure}{fg=draculaPurple}
\\setbeamercolor{alerted text}{fg=draculaRed}
\\setbeamercolor{example text}{fg=draculaGreen}
\\setbeamercolor{block title}{fg=draculaPurple, bg=draculaComment}
\\setbeamercolor{block body}{fg=draculaFg, bg=draculaBg}
\\setbeamercolor{block title example}{fg=draculaGreen, bg=draculaComment}
\\setbeamercolor{block title alerted}{fg=draculaRed, bg=draculaComment}
\\setbeamercolor{itemize item}{fg=draculaPurple}
\\setbeamercolor{itemize subitem}{fg=draculaPink}
\\setbeamercolor{itemize subsubitem}{fg=draculaCyan}
'''
    # Find the \begin{document} and insert the theme just before it
    pattern = r'\\begin\{document\}'
    try:
        def replacement(match):
            return dracula_theme + match.group(0)
        return re.sub(pattern, replacement, content)
    except Exception as e:
        print(f"Error in add_dracula_theme: {str(e)}")
        raise

def add_mono_font(content):
    """Set monospace font for all text in the presentation."""
    mono_settings = '''
\\usepackage{courier}
\\renewcommand{\\familydefault}{\\ttdefault}
\\renewcommand{\\rmdefault}{\\ttdefault}
'''
    # Find the \documentclass and insert the font settings right after it
    pattern = r'(\\documentclass[^}]*})'
    try:
        def replacement(match):
            return match.group(1) + mono_settings
        return re.sub(pattern, replacement, content)
    except Exception as e:
        print(f"Error in add_mono_font: {str(e)}")
        raise

def process_tex_file(tex_file, use_dracula=True, use_mono=True):
    """Process a single tex file."""
    tex_path = Path(tex_file)

    # Create sanitized filename
    new_filename = sanitize_filename(tex_path.name)
    new_path = tex_path.parent / new_filename

    # Read content
    with open(tex_path, 'r') as f:
        content = f.read()

    # Process images and update content
    new_content = copy_and_sanitize_images(content)

    # Add Dracula theme if requested
    if use_dracula:
        new_content = add_dracula_theme(new_content)

    # Add monospace font if requested
    if use_mono:
        new_content = add_mono_font(new_content)

    # Write to new file
    with open(new_path, 'w') as f:
        f.write(new_content)

    # Compile PDF with completely suppressed output
    with open(os.devnull, 'w') as devnull:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', str(new_path)],
            stdout=devnull,
            stderr=devnull
        )

    if result.returncode != 0:
        raise Exception(f"PDF compilation failed for {new_path}")

    return new_path

def cleanup_files():
    """Clean up intermediary files after compilation."""
    # File extensions to remove
    temp_extensions = [
        '.aux', '.log', '.nav', '.snm', '.toc',
        '.out', '.synctex.gz', '.fls', '.fdb_latexmk'
    ]

    # Remove temp files
    for ext in temp_extensions:
        for file in Path('.').glob(f'*{ext}'):
            try:
                file.unlink()
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Could not remove {file}: {e}")

    # Remove sanitized tex files (keeping originals)
    for file in Path('.').glob('*_*.beamer.tex'):
        try:
            file.unlink()
            print(f"Removed: {file}")
        except Exception as e:
            print(f"Could not remove {file}: {e}")

    # Remove temp attachments directory
    if Path('_attachments_temp').exists():
        try:
            shutil.rmtree('_attachments_temp')
            print("Removed: _attachments_temp directory")
        except Exception as e:
            print(f"Could not remove _attachments_temp: {e}")

def main():
    # Add argument parser
    parser = argparse.ArgumentParser(description='Compile beamer slides with optional Dracula theme')
    parser.add_argument('--nodracula', action='store_true', help='Disable applying Dracula theme to the slides')
    parser.add_argument('--nomono', action='store_true', help='Disable using monospace font for all text')
    args = parser.parse_args()

    # Find all .beamer.tex files in current directory
    tex_files = list(Path('.').glob('*.beamer.tex'))

    if not tex_files:
        print("No .beamer.tex files found in current directory")
        return

    print(f"Found {len(tex_files)} .beamer.tex files to process")

    for tex_file in tex_files:
        try:
            new_path = process_tex_file(str(tex_file), use_dracula=not args.nodracula, use_mono=not args.nomono)
            print(f"Processed {tex_file} -> {new_path}")
        except Exception as e:
            print(f"Error processing {tex_file}: {str(e)}")
            import traceback
            print(traceback.format_exc())

    # Clean up after successful compilation
    cleanup_files()

if __name__ == '__main__':
    main()

