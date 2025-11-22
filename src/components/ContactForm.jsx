import React from 'react';

export default function ContactForm() {
    return (
        <form
            action="https://formspree.io/f/YOUR_FORM_ID" // Replace with actual Formspree ID or similar
            method="POST"
            className="max-w-xl mx-auto space-y-6"
        >
            <div>
                <label htmlFor="email" className="block text-sm font-mono text-secondary mb-2">EMAIL</label>
                <input
                    type="email"
                    name="email"
                    id="email"
                    required
                    className="w-full px-4 py-3 bg-surface border border-border rounded-lg text-primary focus:outline-none focus:border-accent transition-colors"
                />
            </div>

            <div>
                <label htmlFor="message" className="block text-sm font-mono text-secondary mb-2">MESSAGE</label>
                <textarea
                    name="message"
                    id="message"
                    rows="5"
                    required
                    className="w-full px-4 py-3 bg-surface border border-border rounded-lg text-primary focus:outline-none focus:border-accent transition-colors"
                ></textarea>
            </div>

            <button
                type="submit"
                className="w-full px-8 py-4 rounded-full bg-primary text-background font-bold hover:opacity-90 transition-opacity"
            >
                SEND TRANSMISSION
            </button>
        </form>
    );
}
