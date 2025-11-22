import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
	schema: z.object({
		title: z.string(),
		description: z.string(),
		date: z.string(),
		tags: z.array(z.string()),
		// We removed the strict .enum() check here so you can type anything
		status: z.string(),
	}),
});

const research = defineCollection({
	schema: z.object({
		title: z.string(),
		description: z.string(),
		date: z.string(),
		pdf: z.string(),
		tags: z.array(z.string()),
	}),
});

export const collections = { projects, research };