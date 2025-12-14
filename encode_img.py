import base64

with open("library_bg.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()
    
print(encoded_string[:50]) # Print first 50 chars to verify
# I will output the whole thing to a file or just read it in style.py
# Actually, better to just read it directly in style.py if I can, but verify first.
