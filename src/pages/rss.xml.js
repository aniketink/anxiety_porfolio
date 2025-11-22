import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
    const projects = await getCollection('projects');
    // Note: Garden notes are currently static in the index page, 
    // but if we migrate them to collections, we can add them here.

    return rss({
        title: 'Aniket.ink | Portfolio Lab',
        description: 'Mechatronics Engineer. I design autonomous systems, write embedded firmware, and document the engineering process.',
        site: context.site,
        items: projects.map((project) => ({
            title: project.data.title,
            pubDate: project.data.date,
            description: project.data.description,
            link: `/projects/${project.slug}/`,
        })),
        customData: `<language>en-us</language>`,
    });
}
