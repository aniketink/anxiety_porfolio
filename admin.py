import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime
import re

# --- CONFIGURATION ---
COLORS = {
    "bg": "#050505",        # Deep Black
    "panel": "#121212",     # Card Background
    "border": "#333333",    # Subtle Border
    "text": "#eeeeee",      # White Text
    "muted": "#888888",     # Gray Text
    "accent": "#ffffff",    # Bright Accent
    "input_bg": "#1a1a1a"   # Input fields
}

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(PROJECT_DIR, "src", "content", "projects")
IMAGE_DIR = os.path.join(PROJECT_DIR, "public", "uploads")

# Ensure upload directory exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

class ModernCMS(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ANIKET.INK // CMS")
        self.geometry("1100x750")
        self.configure(bg=COLORS["bg"])
        self.image_path = None

        # --- LAYOUT ---
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # LEFT SIDEBAR (Metadata)
        self.sidebar = tk.Frame(self, bg=COLORS["bg"], width=320, padx=25, pady=25)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.pack_propagate(False)

        # RIGHT MAIN (Editor)
        self.main_area = tk.Frame(self, bg=COLORS["panel"], padx=30, pady=30)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        self.build_sidebar()
        self.build_editor()

    def build_sidebar(self):
        # Header
        tk.Label(self.sidebar, text="NEW ENTRY", bg=COLORS["bg"], fg=COLORS["accent"], 
                 font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 25))

        # Title
        self.create_label(self.sidebar, "PROJECT TITLE")
        self.entry_title = self.create_input(self.sidebar)
        
        # Description
        self.create_label(self.sidebar, "DESCRIPTION")
        self.entry_desc = self.create_input(self.sidebar)

        # Status
        self.create_label(self.sidebar, "STATUS")
        self.status_var = tk.StringVar(value="Building")
        self.status_menu = tk.OptionMenu(self.sidebar, self.status_var, "Building", "Live", "Prototyping", "Idea")
        self.status_menu.config(bg=COLORS["input_bg"], fg=COLORS["text"], highlightthickness=0, borderwidth=0, activebackground=COLORS["border"])
        self.status_menu["menu"].config(bg=COLORS["input_bg"], fg=COLORS["text"])
        self.status_menu.pack(fill="x", pady=(0, 20))

        # Tags
        self.create_label(self.sidebar, "TAGS (comma separated)")
        self.entry_tags = self.create_input(self.sidebar)

        # Image Upload
        self.create_label(self.sidebar, "IPAD SKETCH")
        self.btn_image = tk.Button(self.sidebar, text="+ Select Image", command=self.select_image, 
                                   bg=COLORS["input_bg"], fg=COLORS["text"], borderwidth=0, pady=10, relief="flat")
        self.btn_image.pack(fill="x", pady=(0, 5))
        
        self.lbl_image_status = tk.Label(self.sidebar, text="No image selected", bg=COLORS["bg"], fg=COLORS["muted"], font=("Arial", 10))
        self.lbl_image_status.pack(anchor="w")

        # Publish Button
        self.btn_publish = tk.Button(self.sidebar, text="PUBLISH SITE ->", command=self.publish, 
                                     bg=COLORS["accent"], fg="black", font=("Arial", 12, "bold"), pady=15, borderwidth=0)
        self.btn_publish.pack(side="bottom", fill="x")

    def build_editor(self):
        # Editor Header
        top_frame = tk.Frame(self.main_area, bg=COLORS["panel"])
        top_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(top_frame, text="CONTENT EDITOR (MDX)", bg=COLORS["panel"], fg=COLORS["muted"], 
                 font=("Arial", 10, "bold")).pack(side="left")

        # The Text Editor
        self.editor = tk.Text(self.main_area, bg=COLORS["bg"], fg=COLORS["text"], 
                              insertbackground="white", borderwidth=0, font=("Menlo", 14), padx=20, pady=20)
        self.editor.pack(fill="both", expand=True)

        # Insert Default Template
        default_text = """## The Problem

Describe the engineering challenge here...

<LabNote>
  <div slot="text">
    <p>
      Explain your thought process here. 
      This text will appear on the left side of the screen.
    </p>
  </div>
  <div slot="visual">
    <!-- Your image will auto-insert here -->
    <Handwritten src="/uploads/PLACEHOLDER.png" caption="Figure 1: Initial Sketch" />
  </div>
</LabNote>

## The Solution

Explain how you solved it...
"""
        self.editor.insert("1.0", default_text)

    # --- HELPERS ---
    def create_label(self, parent, text):
        tk.Label(parent, text=text, bg=COLORS["bg"], fg=COLORS["muted"], 
                 font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))

    def create_input(self, parent):
        entry = tk.Entry(parent, bg=COLORS["input_bg"], fg=COLORS["text"], 
                         insertbackground="white", relief="flat", font=("Arial", 12))
        entry.pack(fill="x", pady=(0, 20), ipady=8)
        return entry

    def select_image(self):
        # FIXED: Removed 'filetypes' argument to prevent macOS crash
        file_path = filedialog.askopenfilename(title="Select an Image")
        
        if file_path:
            self.image_path = file_path
            filename = os.path.basename(file_path)
            self.lbl_image_status.config(text=f"✓ {filename}", fg="#4ade80") # Green color for success
            
            # Auto-update the placeholder in the text editor
            current_text = self.editor.get("1.0", tk.END)
            if "PLACEHOLDER.png" in current_text:
                # We don't replace it yet, we wait for Publish so we have the slug
                pass 

    def publish(self):
        title = self.entry_title.get()
        if not title:
            messagebox.showwarning("Wait", "You need a Title first.")
            return

        # 1. Prepare Data
        slug = re.sub(r'[^a-z0-9-]', '', title.lower().strip().replace(" ", "-"))
        today = datetime.now().strftime("%Y-%m-%d")
        tags_raw = self.entry_tags.get()
        tags = str([t.strip() for t in tags_raw.split(",") if t.strip()]).replace("'", '"')
        
        # 2. Handle Image Move
        image_filename = "PLACEHOLDER.png"
        if self.image_path:
            ext = os.path.splitext(self.image_path)[1]
            image_filename = f"{slug}{ext}"
            dest = os.path.join(IMAGE_DIR, image_filename)
            shutil.copy(self.image_path, dest)

        # 3. Get Editor Content and Fix Image Links
        body = self.editor.get("1.0", tk.END)
        if self.image_path:
            body = body.replace("PLACEHOLDER.png", image_filename)

        # 4. Create Full File
        full_content = f"""---
title: "{title}"
description: "{self.entry_desc.get()}"
date: "{today}"
tags: {tags}
status: "{self.status_var.get()}"
---
import Handwritten from '../../components/Handwritten.astro';
import LabNote from '../../components/LabNote.astro';

{body}
"""

        # 5. Write to Disk
        file_path = os.path.join(CONTENT_DIR, f"{slug}.mdx")
        with open(file_path, "w") as f:
            f.write(full_content)

        messagebox.showinfo("Published!", f"Successfully created: {slug}.mdx\n\nGo check your website!")
        
        # Reset
        self.entry_title.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.image_path = None
        self.lbl_image_status.config(text="No image selected", fg=COLORS["muted"])
        # self.editor.delete("1.0", tk.END)

if __name__ == "__main__":
    app = ModernCMS()
    app.mainloop()