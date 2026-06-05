<script lang="ts">
	import { getContext } from 'svelte';

	import Dropdown from '$lib/components/common/Dropdown.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Sparkles from '$lib/components/icons/Sparkles.svelte';

	type ThinkingLevel = {
		id: string;
		label?: string;
		thinkingBudgetTokens?: number;
		maxTokens?: number;
	};

	const i18n = getContext<any>('i18n');

	export let models: any[] = [];
	export let params: Record<string, any> = {};

	const preferredOrder = ['off', 'light', 'moderate', 'heavy'];
	const fallbackLevels: ThinkingLevel[] = [
		{ id: 'off', label: 'Off' },
		{ id: 'light', label: 'Light' },
		{ id: 'moderate', label: 'Moderate' },
		{ id: 'heavy', label: 'Heavy' }
	];

	let show = false;

	const normalizeEffort = (value: unknown): string | null => {
		if (typeof value !== 'string') {
			return null;
		}
		const normalized = value.trim().toLowerCase();
		if (normalized === 'low') return 'light';
		if (normalized === 'medium') return 'moderate';
		if (normalized === 'high') return 'heavy';
		return normalized || null;
	};

	const displayLabel = (option?: ThinkingLevel | null): string => {
		if (!option) return $i18n.t('Moderate');
		if (option.id === 'off') return $i18n.t('Off');
		if (option.id === 'light') return $i18n.t('Light');
		if (option.id === 'moderate') return $i18n.t('Moderate');
		if (option.id === 'heavy') return $i18n.t('Heavy');
		return option.label ?? option.id;
	};

	const displayDescription = (id: string): string => {
		if (id === 'off') return $i18n.t('Disable model thinking for this response');
		if (id === 'light') return $i18n.t('Use a short thinking budget');
		if (id === 'moderate') return $i18n.t('Use the default thinking budget');
		if (id === 'heavy') return $i18n.t('Use a larger thinking budget');
		return '';
	};

	$: selectedModel = models.length === 1 ? models[0] : null;
	$: selectedModelMeta = (selectedModel?.info?.meta ?? {}) as Record<string, any>;
	$: thinkingMeta = selectedModelMeta?.local_llm?.thinking ?? null;
	$: capabilities = (selectedModelMeta?.capabilities ?? {}) as Record<string, any>;
	$: thinkingCapable = models.length === 1 && capabilities?.['reasoning_effort'] === true;
	$: rawLevels =
		thinkingCapable && Array.isArray(thinkingMeta?.levels) && thinkingMeta.levels.length > 0
			? (thinkingMeta.levels as ThinkingLevel[])
			: fallbackLevels;
	$: availableLevels = preferredOrder
		.map((id) => rawLevels.find((level) => level?.id === id))
		.filter((level): level is ThinkingLevel => Boolean(level));
	$: defaultEffort = normalizeEffort(thinkingMeta?.default) ?? 'moderate';
	$: currentEffort = normalizeEffort(params?.reasoning_effort) ?? defaultEffort;
	$: selectedOption =
		availableLevels.find((level) => level?.id === currentEffort) ??
		availableLevels.find((level) => level?.id === defaultEffort) ??
		availableLevels[0];

	const setEffort = (effort: string) => {
		params = { ...params, reasoning_effort: effort };
		show = false;
	};
</script>

{#if thinkingCapable}
	<Dropdown
		bind:show
		side="top"
		align="start"
		contentClass="w-48 rounded-xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-950 shadow-lg p-1"
	>
		<Tooltip content={$i18n.t('Thinking effort')} placement="top">
			<button
				type="button"
				class="bg-transparent hover:bg-gray-100 text-gray-700 dark:text-white dark:hover:bg-gray-800 rounded-full h-8 px-2.5 flex gap-1.5 justify-center items-center outline-hidden focus:outline-hidden"
				aria-label={$i18n.t('Thinking effort')}
			>
				<Sparkles className="size-4" strokeWidth="1.75" />
				<span class="text-xs font-medium max-w-20 truncate">{displayLabel(selectedOption)}</span>
			</button>
		</Tooltip>

		<div slot="content" class="flex flex-col">
			{#each availableLevels as option}
				<Tooltip content={displayDescription(option.id)} placement="left">
					<button
						type="button"
						class="flex w-full items-center gap-2 rounded-lg px-2.5 py-2 text-left text-sm hover:bg-gray-50 dark:hover:bg-gray-800/60"
						on:click={() => setEffort(option.id)}
					>
						<span
							class="size-1.5 rounded-full shrink-0 {option.id === selectedOption?.id
								? 'bg-gray-900 dark:bg-gray-100'
								: 'bg-transparent'}"
						></span>
						<span class="flex-1 truncate">{displayLabel(option)}</span>
					</button>
				</Tooltip>
			{/each}
		</div>
	</Dropdown>
{/if}
