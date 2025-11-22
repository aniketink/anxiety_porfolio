// Configuration
const API_URL = 'http://localhost:8000/api';
let currentType = 'projects';
let currentFile = null;
let previewMode = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadContent('projects');
});

// Switch content type
async function switchType(type) {
    currentType = type;
    currentFile = null;

    // Show/hide status field for projects
    document.getElementById('statusField').style.display =
        type === 'projects' ? 'block' : 'none';

    await loadContent(type);
}

// Load content list
async function loadContent(type) {
    try {
        const response = await fetch(`${API_URL}/content/${type}`);
        const content = await response.json();

        const listEl = document.getElementById('contentList');
        listEl.innerHTML = '';

        content.forEach(item => {
            const div = document.createElement('div');
            div.className = 'p-4 rounded-lg hover:bg-surface-hover cursor-pointer transition-all content-card border border-transparent hover:border-border';
            div.onclick = () => loadFile(type, item.filename);

            div.innerHTML = `
                <div class="font-medium text-sm mb-1">${item.metadata.title || item.filename}</div>
                <div class="text-xs text-secondary font-mono">${formatDate(item.modified)}</div>
                ${item.metadata.tags ? `<div class="flex flex-wrap gap-1.5 mt-2.5">
                    ${item.metadata.tags.map(tag =>
                `<span class="text-xs px-2 py-0.5 bg-secondary/10 text-secondary rounded-md font-mono">${tag}</span>`
            ).join('')}
                </div>` : ''}
            `;

            listEl.appendChild(div);
        });

        if (content.length === 0) {
            listEl.innerHTML = '<div class="p-4 text-center text-gray-500 text-sm">No content yet</div>';
        }
    } catch (error) {
        console.error('Error loading content:', error);
        alert('Failed to load content. Is the server running?');
    }
}

// Load specific file
async function loadFile(type, filename) {
    try {
        const response = await fetch(`${API_URL}/content/${type}/${filename}`);
        const data = await response.json();

        currentFile = { type, filename, data };

        // Update UI
        document.getElementById('editorTitle').textContent = data.metadata.title || filename;
        document.getElementById('titleInput').value = data.metadata.title || '';
        document.getElementById('descriptionInput').value = data.metadata.description || '';
        document.getElementById('dateInput').value = data.metadata.date || '';
        document.getElementById('tagsInput').value = (data.metadata.tags || []).join(', ');
        document.getElementById('statusInput').value = data.metadata.status || 'Active';
        document.getElementById('editor').value = data.body;

        if (previewMode) {
            updatePreview();
        }
    } catch (error) {
        console.error('Error loading file:', error);
        alert('Failed to load file');
    }
}

// Save content
async function saveContent() {
    if (!currentFile) {
        alert('No file selected');
        return;
    }

    const metadata = {
        title: document.getElementById('titleInput').value,
        description: document.getElementById('descriptionInput').value,
        date: document.getElementById('dateInput').value,
        tags: document.getElementById('tagsInput').value.split(',').map(t => t.trim()).filter(t => t),
    };

    if (currentFile.type === 'projects') {
        metadata.status = document.getElementById('statusInput').value;
    }

    const body = document.getElementById('editor').value;

    try {
        const response = await fetch(
            `${API_URL}/content/${currentFile.type}/${currentFile.filename}`,
            {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ metadata, body })
            }
        );

        if (response.ok) {
            showNotification('✓ Saved and committed to git!', 'success');
            await loadContent(currentFile.type);
        } else {
            throw new Error('Save failed');
        }
    } catch (error) {
        console.error('Error saving:', error);
        showNotification('✗ Failed to save', 'error');
    }
}

// New content
function newContent() {
    const title = prompt('Enter title for new content:');
    if (!title) return;

    currentFile = null;
    document.getElementById('editorTitle').textContent = title;
    document.getElementById('titleInput').value = title;
    document.getElementById('descriptionInput').value = '';
    document.getElementById('dateInput').value = new Date().toISOString().split('T')[0];
    document.getElementById('tagsInput').value = '';
    document.getElementById('statusInput').value = 'Active';
    document.getElementById('editor').value = '# ' + title + '\n\n';

    setTimeout(() => createNewContent(title), 100);
}

async function createNewContent(title) {
    const metadata = {
        title,
        description: '',
        date: document.getElementById('dateInput').value,
        tags: [],
    };

    if (currentType === 'projects') {
        metadata.status = 'Active';
    }

    try {
        const response = await fetch(`${API_URL}/content/${currentType}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title,
                body: `# ${title}\n\n`,
                metadata
            })
        });

        const result = await response.json();
        if (result.success) {
            await loadContent(currentType);
            await loadFile(currentType, result.filename);
            showNotification('✓ Content created!', 'success');
        }
    } catch (error) {
        console.error('Error creating content:', error);
        showNotification('✗ Failed to create', 'error');
    }
}

// Toggle preview
function togglePreview() {
    const previewPane = document.getElementById('previewPane');
    previewPane.classList.toggle('hidden');

    if (!previewPane.classList.contains('hidden')) {
        updatePreview();
    }
}

// Update preview
function updatePreview() {
    const markdown = document.getElementById('editor').value;
    let html = simpleMarkdown(markdown);

    // Render backlinks
    html = html.replace(/\[\[([^\]]+)\]\]/g, '<span class="text-blue-400 font-mono">→ $1</span>');

    document.getElementById('preview').innerHTML = html;

    // Render LaTeX
    renderMathInElement(document.getElementById('preview'), {
        delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false }
        ]
    });
}

// Simple markdown renderer
function simpleMarkdown(text) {
    // Escape HTML
    text = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Headers
    text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Bold and italic
    text = text.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Code blocks
    text = text.replace(/```(\w+)?\n([\s\S]+?)```/g, '<pre><code>$2</code></pre>');

    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Lists
    text = text.replace(/^\* (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

    // Paragraphs
    text = text.split('\n\n').map(para => {
        if (!para.match(/^<[hup]/)) {
            return '<p>' + para + '</p>';
        }
        return para;
    }).join('\n');

    return text;
}

// Search
async function searchContent() {
    const query = document.getElementById('searchInput').value;
    if (query.length < 2) {
        await loadContent(currentType);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/search?query=${encodeURIComponent(query)}`);
        const results = await response.json();

        const listEl = document.getElementById('contentList');
        listEl.innerHTML = '';

        results.forEach(item => {
            const div = document.createElement('div');
            div.className = 'p-3 mb-2 rounded hover:bg-border-dark cursor-pointer transition-colors';
            div.onclick = () => loadFile(item.type, item.filename);

            div.innerHTML = `
                <div class="text-xs text-blue-400 mb-1">${item.type}</div>
                <div class="font-medium text-sm">${item.metadata.title || item.filename}</div>
                <div class="text-xs text-gray-500 mt-1 line-clamp-2">${item.body.substring(0, 100)}...</div>
            `;

            listEl.appendChild(div);
        });
    } catch (error) {
        console.error('Search error:', error);
    }
}

// Utilities
function formatDate(isoString) {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-6 right-6 px-5 py-3 rounded-lg shadow-2xl ${type === 'success' ? 'bg-white text-background' : 'bg-red-600 text-white'
        } z-50 font-medium text-sm border ${type === 'success' ? 'border-border' : 'border-red-700'}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(10px)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Auto-save draft every 30 seconds
setInterval(() => {
    if (currentFile && document.getElementById('editor').value.trim()) {
        localStorage.setItem(
            `draft_${currentFile.type}_${currentFile.filename}`,
            document.getElementById('editor').value
        );
    }
}, 30000);
