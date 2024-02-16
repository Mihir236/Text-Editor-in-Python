import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.text_area = tk.Text(self.root, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        self.create_menu()
        self.add_status_bar()
        self.syntax_highlighting()
        self.file_path = None  # Store the current file path

        # Save changes when closing the application
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Word Count", command=self.count_words)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menu_bar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())
                self.file_path = file_path
                self.syntax_highlighting()

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
                self.file_path = file_path

    def add_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.save_file()  # Save changes before closing
            self.root.destroy()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def count_words(self):
        content = self.text_area.get(1.0, tk.END)
        words = content.split()
        word_count = len(words)
        messagebox.showinfo("Word Count", f"Total Words: {word_count}")

    def syntax_highlighting(self):
        self.text_area.tag_configure("keyword", foreground="blue")
        self.text_area.tag_configure("string", foreground="green")
        self.text_area.tag_configure("comment", foreground="gray")

        keywords = ["def", "class", "if", "else", "elif", "for", "while", "import", "from", "as", "return", "True", "False"]
        for keyword in keywords:
            self.highlight_pattern(keyword, "keyword")

        self.highlight_string_literals()
        self.highlight_comments()

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=True):
        start = self.text_area.index(start)
        end = self.text_area.index(end)
        self.text_area.mark_set("matchStart", start)
        self.text_area.mark_set("matchEnd", start)
        self.text_area.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.text_area.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "": break
            self.text_area.mark_set("matchStart", index)
            self.text_area.mark_set("matchEnd", f"{index}+{count.get()}c")
            self.text_area.tag_add(tag, "matchStart", "matchEnd")

    def highlight_string_literals(self):
        self.highlight_pattern(r'\".*?\"', "string", regexp=False)
        self.highlight_pattern(r'\'.*?\'', "string", regexp=False)

    def highlight_comments(self):
        self.highlight_pattern(r'#.*$', "comment")

def main():
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
