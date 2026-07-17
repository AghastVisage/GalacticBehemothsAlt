
import os
import sys

def sanitize_file(file_path):
    print(f"Sanitizing {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Fallback to utf-8 if sig fails (though sig usually handles non-sig too, but just in case)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return

    sanitized_lines = []
    inside_l_english = False
    
    last_processed_line_content = None
    last_was_comment = False

    for line in lines:
        stripped = line.strip()
        
        # Handle BOM on first line if read with utf-8 (utf-8-sig removes it automatically)
        if not sanitized_lines and stripped.startswith(u'\ufeff'):
            stripped = stripped[1:]

        if not stripped:
            if inside_l_english:
                sanitized_lines.append("\n")
                last_processed_line_content = None
                last_was_comment = False
            else:
                sanitized_lines.append(line)
            continue

        if stripped.startswith("l_english:") or stripped.startswith("l_simp_chinese:"): 
            # Detect language block
            sanitized_lines.append(stripped + "\n")
            inside_l_english = True
            last_processed_line_content = None
            last_was_comment = False
            continue
            
        if inside_l_english:
            is_comment = stripped.startswith("#")
            
            if is_comment:
                # Check for duplicates
                # We check compatibility with the *last added line*
                if last_was_comment and last_processed_line_content == stripped:
                    # Duplicate comment, skip
                    continue
                
                # Add comment with 2 spaces indentation
                sanitized_lines.append("  " + stripped + "\n")
                last_processed_line_content = stripped
                last_was_comment = True
            else:
                # Key or content
                # Ensure 2 spaces indentation
                # If it already has indentation, stripped removes it.
                # Just add 2 spaces. 
                # Note: Paradox keys can be "key:0", "key:", etc.
                sanitized_lines.append("  " + stripped + "\n")
                last_processed_line_content = stripped
                last_was_comment = False
        else:
            # Outside language block, keep as is
            sanitized_lines.append(line)

    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.writelines(sanitized_lines)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".yml"):
                file_path = os.path.join(root, file)
                sanitize_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "localisation", "english")
    
    if os.path.isfile(target):
        sanitize_file(target)
    elif os.path.isdir(target):
        process_directory(target)
    else:
        print(f"Target not found: {target}")
