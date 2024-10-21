import type { Face } from '$lib/models/face';
import { writable } from 'svelte/store';

export const media = writable<File|null>(null);
export const status = writable('');
export const result = writable<Face[]>([]);
export const activeFace = writable<Face|null>(null);
export const accessToken = writable<string|null>(null); // Store the access token here