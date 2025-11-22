# Portfolio Lab - Beginner's Guide

Welcome! This is the documentation for your personal portfolio website. This guide is written for someone with **little to no coding experience**. Follow these steps to edit your site and publish new content.

## �️ Prerequisites (What you need installed)

Before you start, make sure you have these two free tools installed on your computer:

1.  **Node.js**: This is the engine that runs the website code.
    -   [Download Node.js here](https://nodejs.org/en/download/). Choose the "LTS" (Long Term Support) version.
    -   Install it like any other program.
2.  **VS Code**: This is the text editor where you will write your code.
    -   [Download VS Code here](https://code.visualstudio.com/).

---

## � Getting Started

### 1. Open the Project
1.  Open **VS Code**.
2.  Go to `File > Open Folder...` and select the `portfolio-lab` folder on your computer.

### 2. Install Dependencies
Think of "dependencies" as the parts of the car engine that we need to download before we can drive.
1.  In VS Code, go to `Terminal > New Terminal` (at the top menu). A panel will open at the bottom.
2.  Type this command and press **Enter**:
    ```sh
    npm install
    ```
    *You will see a bunch of text scrolling. Wait until it stops.*

### 3. Start the Website
Now let's turn the engine on.
1.  In the same terminal, type:
    ```sh
    npm run dev
    ```
2.  You will see a message saying `Local: http://localhost:4321`.
3.  **Hold Command (Mac) or Ctrl (Windows)** and click that link. Your website will open in your browser!

---

## 📝 How to Edit Content

### Changing the Homepage Text
1.  In the file explorer on the left of VS Code, navigate to `src` -> `pages` -> `index.astro`.
2.  Click `index.astro` to open it.
3.  Scroll down until you see the text you want to change (e.g., "I bridge the gap between").
4.  Edit the text inside the tags.
    -   **Tip**: Be careful not to delete the `<` and `>` tags around the text.
5.  Save the file (`Cmd + S` or `Ctrl + S`). The website in your browser will update automatically!

### Adding a New Project
1.  Go to `src` -> `content` -> `projects`.
2.  You will see files ending in `.mdx`. These are your project files.
3.  **Copy and Paste** one of the existing files (like `robot-arm.mdx`) and rename it (e.g., `my-new-project.mdx`).
4.  Open your new file.

### 📄 Adding Research Papers

1.  **Add the PDF**: Place your PDF file in the `public/pdfs/` folder.
    *   Example: `public/pdfs/my-paper.pdf`
2.  **Create Content File**: Create a new `.mdx` file in `src/content/research/`.
    *   Example: `src/content/research/my-paper.mdx`
3.  **Add Metadata**: Use the following frontmatter:
    ```yaml
    ---
    title: "My Research Paper"
    description: "A brief summary of the paper."
    date: "2023-11-22"
    pdf: "/pdfs/my-paper.pdf"  <-- Path relative to public folder
    tags: ["ROBOTICS", "AI"]
    ---
    
    ## Abstract
    
    Write your abstract or additional notes here.
    ```
5.  **Edit the Top Section (Frontmatter)**:
    This is the metadata between the `---` lines.
    ```yaml
    title: "My New Project"
    description: "What I did..."
    date: "2023-10-27"
    tags: ["DESIGN", "CODE"]
    status: "Completed"
    ```
6.  **Edit the Content**:
    Below the second `---`, write your article. You can use standard text.
    -   To make a heading, use `## Heading Name`.
    -   To make a list, use `- Item 1`.
    -   To make text bold, use `**bold text**`.

### Adding a Book to the Library
1.  Go to `src` -> `pages` -> `bookshelf.astro`.
2.  Look for the list that starts with `const books = [`.
3.  Copy one of the `{ ... }` blocks and paste it inside the list.
4.  Update the `title`, `author`, `rating`, `note`, and `status`.

---

## 🎨 Changing Colors and Fonts

If you want to change the "theme" of the site (like the background color or the accent color):

1.  Open the file `tailwind.config.mjs` (it's in the main folder).
2.  Look for the `colors` section.
    ```js
    colors: {
      background: '#09090b', // This is the dark background color
      primary: '#fafafa',    // This is the main text color
      // ...
    }
    ```
3.  You can change these hex codes (e.g., `#09090b`) to any color you want. Google "Color Picker" to find hex codes.

---

## 🚢 Publishing Your Website

When you are ready to show the world:

1.  **Stop the server**: Go to the terminal and press `Ctrl + C`.
2.  **Build the site**: Type this command:
    ```sh
    npm run build
    ```
3.  This creates a `dist` folder. This folder contains your final website.
4.  **Upload**: You can drag and drop this `dist` folder to a host like **Netlify Drop** (search for it online) to put it online for free instantly.

---

## ❓ Troubleshooting

-   **"Command not found"**: Make sure you installed Node.js (Step 1 of Prerequisites).
-   **Red squiggly lines in VS Code**: You might have made a typo in the code. Undo your last change (`Cmd + Z`) and try again.
-   **Website isn't updating**: Make sure you saved the file (`Cmd + S`).

Need more help? Ask a developer friend or search for "Astro tutorial" on YouTube!
