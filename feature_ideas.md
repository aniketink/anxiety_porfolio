# Feature Ideas for Portfolio Lab

Here are several features we could add to enhance your portfolio, categorized by complexity and impact.

## 🚀 High Impact / Low Effort

1.  **RSS Feed**:
    -   *Why*: Let people subscribe to your garden notes and project updates.
    -   *How*: Use `@astrojs/rss` to generate an XML feed automatically.

2.  **Sitemap & SEO Meta Tags**:
    -   *Why*: Improve visibility on Google and social media previews (Open Graph images).
    -   *How*: Use `@astrojs/sitemap` and a reusable `<SEO />` component.

3.  **"Now" Page**:
    -   *Why*: A page that tells visitors what you are focused on *right now* (reading, building, learning).
    -   *How*: A simple new page at `/now`.

## 🎨 Visual & Interactive

4.  **Dark/Light Mode Toggle**:
    -   *Why*: Accessibility and user preference.
    -   *How*: Use Tailwind's `darkMode` class and a small React/JS script to toggle local storage preference.

5.  **Page Transitions**:
    -   *Why*: Make navigation feel seamless and app-like.
    -   *How*: Use Astro's built-in `<ViewTransitions />`.

6.  **Interactive 3D Element**:
    -   *Why*: Show off "mechatronics" vibes.
    -   *How*: Add a simple Three.js or Spline scene to the Hero section (e.g., a rotating wireframe cube or robot arm).

## 🛠️ Functional Enhancements

7.  **Search**:
    -   *Why*: Help users find specific notes or projects.
    -   *How*: Implement a client-side search using `fuse.js` or a simple filter input.

8.  **Tags Page**:
    -   *Why*: Allow users to see all content related to "Robotics" or "Python".
    -   *How*: Create a dynamic route `/tags/[tag].astro` to list content by tag.

9.  **Contact Form**:
    -   *Why*: Make it easy for recruiters/collaborators to reach you.
    -   *How*: A simple form using a service like Formspree or Netlify Forms (if hosting there).

## 📊 Analytics

10. **Privacy-Friendly Analytics**:
    -   *Why*: See which projects are most popular.
    -   *How*: Integrate a lightweight script like Plausible or Umami (free tiers available).
