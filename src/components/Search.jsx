import React, { useState } from 'react';
import Fuse from 'fuse.js';

export default function Search({ searchList }) {
    const [query, setQuery] = useState('');

    const fuse = new Fuse(searchList, {
        keys: ['title', 'description', 'tags'],
        includeScore: true,
        threshold: 0.4,
    });

    const results = fuse.search(query);

    return (
        <div className="relative w-full max-w-xl mx-auto mb-12 z-50">
            <input
                type="text"
                placeholder="Search projects and notes..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full px-6 py-4 bg-surface border border-border rounded-full text-primary focus:outline-none focus:border-accent transition-colors"
            />

            {query && (
                <div className="absolute top-full left-0 w-full mt-2 bg-surface border border-border rounded-xl shadow-2xl overflow-hidden z-50">
                    {results.length === 0 ? (
                        <div className="p-4 text-secondary text-center">No results found.</div>
                    ) : (
                        <ul>
                            {results.map(({ item }) => (
                                <li key={item.slug}>
                                    <a href={`/${item.collection}/${item.slug}`} className="block p-4 hover:bg-surface-hover transition-colors border-b border-border last:border-none">
                                        <h4 className="text-primary font-serif text-lg mb-1">{item.title}</h4>
                                        <p className="text-secondary text-sm line-clamp-1">{item.description}</p>
                                    </a>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            )}
        </div>
    );
}
