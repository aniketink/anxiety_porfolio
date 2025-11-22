import fs from 'fs';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Helper to format today's date as YYYY-MM-DD
const today = new Date().toISOString().split('T')[0];

console.log('\n🌱 \x1b[32mNEW ENTRY GENERATOR\x1b[0m 🌱');
console.log('-----------------------------------');

rl.question('Type (1) Project or (2) Garden Note? [1/2]: ', (type) => {
  
  const folder = type === '1' ? 'src/content/projects' : 'src/pages/garden'; // Adjust if you move garden to content later
  // Since your Garden is currently hardcoded in the file, let's stick to Projects for MDX for now.
  // Actually, let's assume you will move Garden to content soon. For now, let's focus on Projects.
  
  if (type !== '1') {
    console.log("⚠️  Currently only Projects are fully automated with MDX. Let's make a Project.");
  }

  rl.question('Title of post: ', (title) => {
    const slug = title.toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g, '');
    const filename = `${slug}.mdx`;
    const path = `src/content/projects/${filename}`;

    const content = `---
title: "${title}"
description: "Brief description here..."
date: "${today}"
tags: ["TAG1", "TAG2"]
status: "In Progress"
---
import Handwritten from '../../components/Handwritten.astro';
import LabNote from '../../components/LabNote.astro';

## The Idea

Write your thoughts here...

<Handwritten src="/YOUR_IMAGE.png" caption="Sketch" />
`;

    fs.writeFileSync(path, content);
    console.log(`\n✅ Created: \x1b[36m${path}\x1b[0m`);
    console.log(`Go start writing!`);
    rl.close();
  });
});