import type { Face } from '$lib/models/face';
import { writable } from 'svelte/store';

export const media = writable<File|null>(null);
export const status = writable('');
export const result = writable<Face[]>([]);