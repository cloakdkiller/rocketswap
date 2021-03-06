<script lang="ts">
	import { createEventDispatcher, getContext, onMount } from 'svelte'
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';


	//Components
	import TokenSelect from '../misc/token-select-toggle.svelte'

	//Misc
	import { config } from '../../config'
	import { stringToFixed, toBigNumber, determinePrecision } from '../../utils.js'
	import { tokenBalances, payInRswp } from '../../store'

	//Props
	export let label

	const dispatch = createEventDispatcher();
	
	let { pageStores, showMax } = getContext('pageContext')
	const { selectedToken, tokenAmount, buy } = pageStores

	let inputElm;
	let pressedMaxValue = false;

	$: tokenBalance = $selectedToken ? $tokenBalances[$selectedToken.contract_name] : toBigNumber("0.0")
	let inputValue;

	tokenAmount.subscribe(newTokenAmount => {
		if (!inputValue) {
			inputValue = newTokenAmount
			return
		}
		if (newTokenAmount?.isEqualTo(inputValue)) return
		else{
			inputValue = newTokenAmount
			pressedMaxValue = false;
		}
	})

	onMount(() => {
		payInRswp.subscribe(val => {
			if ($tokenAmount && typeof inputValue !== 'undefined' && !$buy){
				if (inputValue > 0) dispatchEvent(inputValue)
			}
		})
	})

	const handleInputChange = (e) => {
		let validateValue = e.target.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1')
		if (validateValue !== e.target.value) {
			inputElm.value = validateValue
		}else{
			let value = toBigNumber(e.target.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1'))
			if (determinePrecision(value) > 8){
				value = toBigNumber(stringToFixed(value, 8))
				inputElm.value = stringToFixed(value, 8)
			}
			pressedMaxValue = false
			dispatchEvent(value)
		}
	}

	const handleMaxInput = () => {
		inputValue = tokenBalance
		inputElm.value = stringToFixed(inputValue, 8)
		pressedMaxValue = true
		dispatchEvent(inputValue)
	}

	const handleTokenSelect = (e) => {
		pressedMaxValue = false
		dispatchEvent(inputValue, e.detail)
	}

	const dispatchEvent = (value, selected) => dispatch('input', {tokenAmount: value, selected})
</script>

<div class="input-container flex-col"
	 in:scale="{{duration: 300, delay: 0, opacity: 0.0, start: 0.6, easing: quintOut}}">
	<div class="input-row-1 flex-row">
		<div class="input-label text-primary">
			{label}
		</div>
		<div class="input-balance">
			{#if $selectedToken}
				<span class="number text-small">
					{`Balance: ${stringToFixed(tokenBalance, 8)}`}
				</span>
			{/if}
		</div>
	</div>
	<div class="input-row-2 flex-row">
		<input 
			class="input-amount-value number"
			placeholder="0.0" 
			value={inputValue ? stringToFixed(inputValue, 8) : ""}
			bind:this={inputElm} 
			on:input={handleInputChange}
			disabled={!$selectedToken} 
		/>
		<div class="input-controls">
			{#if ($buy === false && $selectedToken && !pressedMaxValue) || (showMax &&  !pressedMaxValue && $selectedToken)}
				<button disabled={!$selectedToken} on:click={handleMaxInput} class="primary small">MAX</button>
			{/if}
			<TokenSelect on:selected={handleTokenSelect} />
		</div>
	</div>
</div>
