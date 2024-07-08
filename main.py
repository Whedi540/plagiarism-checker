import tkinter as tk
from tkinter import filedialog, Text
import difflib


def load_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        entry.delete(1.0, tk.END)
        entry.insert(tk.END, content)


def get_similarity(text1, text2):
    seq = difflib.SequenceMatcher(None, text1, text2)
    return seq.ratio()


def compare_texts():
    text1 = text_entry1.get(1.0, tk.END)
    text2 = text_entry2.get(1.0, tk.END)

    similarity = get_similarity(text1, text2)
    result_text.set(f"Similarity Score: {similarity:.2f}")

    highlight_differences(text1, text2)


def highlight_differences(text1, text2):
    seq = difflib.SequenceMatcher(None, text1, text2)
    text_entry1.tag_remove('highlight', "1.0", tk.END)
    text_entry2.tag_remove('highlight', "1.0", tk.END)
    text_entry1.tag_remove('replace', "1.0", tk.END)
    text_entry2.tag_remove('replace', "1.0", tk.END)
    text_entry1.tag_remove('delete', "1.0", tk.END)
    text_entry2.tag_remove('delete', "1.0", tk.END)
    text_entry1.tag_remove('insert', "1.0", tk.END)

    for tag, i1, i2, j1, j2 in seq.get_opcodes():
        if tag == 'equal':
            text_entry1.tag_add('highlight', f"1.0+{i1}c", f"1.0+{i2}c")
            text_entry2.tag_add('highlight', f"1.0+{j1}c", f"1.0+{j2}c")
        elif tag == 'replace':
            text_entry1.tag_add('replace', f"1.0+{i1}c", f"1.0+{i2}c")
            text_entry2.tag_add('replace', f"1.0+{j1}c", f"1.0+{j2}c")
        elif tag == 'delete':
            text_entry1.tag_add('delete', f"1.0+{i1}c", f"1.0+{i2}c")
        elif tag == 'insert':
            text_entry2.tag_add('insert', f"1.0+{j1}c", f"1.0+{j2}c")


def configure_tags():
    text_entry1.tag_config('highlight', background='yellow')
    text_entry2.tag_config('highlight', background='yellow')
    text_entry1.tag_config('replace', background='orange')
    text_entry2.tag_config('replace', background='orange')
    text_entry1.tag_config('delete', background='red')
    text_entry2.tag_config('delete', background='red')
    text_entry1.tag_config('insert', background='green')
    text_entry2.tag_config('insert', background='green')


root = tk.Tk()
root.title("Plagiarism Detection Tool")
root.configure(background='#f0f0f0')  # Light gray background

frame = tk.Frame(root, bg='#f0f0f0')
frame.pack(pady=20)

text_entry1 = Text(frame, width=60, height=20)
text_entry1.pack(side=tk.LEFT, padx=10)

text_entry2 = Text(frame, width=60, height=20)
text_entry2.pack(side=tk.RIGHT, padx=10)

button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=20)

load_button1 = tk.Button(button_frame, text="Load File 1", command=lambda: load_file(text_entry1), bg='#4CAF50', fg='white')
load_button1.pack(side=tk.LEFT, padx=10)

load_button2 = tk.Button(button_frame, text="Load File 2", command=lambda: load_file(text_entry2), bg='#4CAF50', fg='white')
load_button2.pack(side=tk.RIGHT, padx=10)

compare_button = tk.Button(root, text="Compare Texts", command=compare_texts, bg='#2196F3', fg='white')
compare_button.pack(pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, bg='#f0f0f0')
result_label.pack(pady=10)

configure_tags()

root.mainloop()


