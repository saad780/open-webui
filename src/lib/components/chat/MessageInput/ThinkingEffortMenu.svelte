<script lang="ts">
	import { getContext } from 'svelte';
	import type { Readable } from 'svelte/store';

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Sparkles from '$lib/components/icons/Sparkles.svelte';
	import {
		normalizeThinkingEffort,
		thinkingIsEnabled,
		toggledThinkingEffort
	} from './thinking-effort';

	type I18n = { t: (key: string, ...args: unknown[]) => string };
	type ThinkingModel = {
		info?: {
			meta?: {
				capabilities?: Record<string, unknown>;
				local_llm?: { thinking?: { default?: unknown } };
			};
		};
	};

	const i18n = getContext<Readable<I18n>>('i18n');

	export let models: ThinkingModel[] = [];
	export let params: Record<string, unknown> = {};

	$: selectedModel = models.length === 1 ? models[0] : null;
	$: selectedModelMeta = selectedModel?.info?.meta ?? {};
	$: capabilities = selectedModelMeta?.capabilities ?? {};
	$: thinkingMeta = selectedModelMeta?.local_llm?.thinking ?? null;
	$: thinkingCapable = models.length === 1 && capabilities?.['reasoning_effort'] === true;
	$: defaultEffort = normalizeThinkingEffort(thinkingMeta?.default) ?? 'off';
	$: enabled = thinkingIsEnabled(params?.reasoning_effort, defaultEffort);

	const toggleThinking = () => {
		params = { ...params, reasoning_effort: toggledThinkingEffort(enabled) };
	};
</script>

{#if thinkingCapable}
	<Tooltip
		content={enabled
			? $i18n.t('Disable model thinking for upcoming responses')
			: $i18n.t('Enable model thinking for upcoming responses')}
		placement="top"
	>
		<button
			type="button"
			class="h-8 px-2.5 flex gap-1.5 justify-center items-center rounded-full outline-hidden focus:outline-hidden transition-colors {enabled
				? 'text-sky-500 dark:text-sky-300 bg-sky-50 hover:bg-sky-100 dark:bg-sky-400/10 dark:hover:bg-sky-600/10 border border-sky-200/40 dark:border-sky-500/20'
				: 'bg-transparent hover:bg-gray-100 text-gray-700 dark:text-white dark:hover:bg-gray-800'}"
			aria-label={enabled ? $i18n.t('Thinking on') : $i18n.t('Thinking off')}
			aria-pressed={enabled}
			on:click={toggleThinking}
		>
			<Sparkles className="size-4" strokeWidth="1.75" />
			<span class="text-xs font-medium">{$i18n.t('Thinking')}</span>
		</button>
	</Tooltip>
{/if}
