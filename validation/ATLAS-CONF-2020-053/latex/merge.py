import re
with open('merge.md') as f:
    temp = f.read()
def replace_file_placeholder(text):
    # Use a regular expression to find all occurrences of <<file_name>> with file name in capture group
    pattern = r"<<file_name=([_\w./-]+)>>"
    matches = re.findall(pattern, text)
    # Iterate over matches and replace <<file_name>> with contents of file
    for match in matches:
        file_path = match
        with open(file_path, "r") as f:
            file_contents = f.read()
        # Replace <<file_name>> with contents of file
        text = text.replace(f"<<file_name={file_path}>>", file_contents)
        
    return text
with open('merged.md','w') as f:
    f.write(replace_file_placeholder(temp))