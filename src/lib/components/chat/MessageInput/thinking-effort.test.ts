import { describe, expect, it } from 'vitest';

import {
	normalizeThinkingEffort,
	thinkingIsEnabled,
	toggledThinkingEffort
} from './thinking-effort';

describe('thinking effort toggle', () => {
	it('defaults to off when the model metadata says off', () => {
		expect(thinkingIsEnabled(undefined, 'off')).toBe(false);
	});

	it('treats standard reasoning effort aliases as thinking enabled', () => {
		expect(normalizeThinkingEffort('medium')).toBe('moderate');
		expect(thinkingIsEnabled('high', 'off')).toBe(true);
	});

	it('toggles between the binary gateway values', () => {
		expect(toggledThinkingEffort(false)).toBe('moderate');
		expect(toggledThinkingEffort(true)).toBe('off');
	});
});
