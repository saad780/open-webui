export const normalizeThinkingEffort = (value: unknown): string | null => {
	if (typeof value !== 'string') {
		return null;
	}
	const normalized = value.trim().toLowerCase();
	if (['0', 'false', 'none', 'no', 'off', 'disabled', 'disable'].includes(normalized)) {
		return 'off';
	}
	if (normalized === 'low') return 'light';
	if (normalized === 'medium') return 'moderate';
	if (normalized === 'high') return 'heavy';
	return normalized || null;
};

export const thinkingIsEnabled = (requestedEffort: unknown, defaultEffort: unknown): boolean => {
	return (normalizeThinkingEffort(requestedEffort) ?? normalizeThinkingEffort(defaultEffort) ?? 'off') !== 'off';
};

export const toggledThinkingEffort = (enabled: boolean): 'off' | 'moderate' =>
	enabled ? 'off' : 'moderate';
