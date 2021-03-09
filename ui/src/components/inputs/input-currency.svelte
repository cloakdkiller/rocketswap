<script lang="ts">
	import { createEventDispatcher, afterUpdate, getContext, onMount } from 'svelte'
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	//Icons
	import LamdenLogo from '../../icons/lamden-logo.svelte'

	//Stores
	import { walletBalance, payInRswp } from '../../store'

	//Services
	import { WalletService } from '../../services/wallet.service'
	const walletService = WalletService.getInstance();

	//Misc
	import { config } from '../../config'
	import { stringToFixed, toBigNumber, determinePrecision, stampsToTAU } from '../../utils.js'

	//Props
	export let label

	const dispatch = createEventDispatcher();

	const { pageStores, getStampCost } = getContext('pageContext')
	const { currencyAmount, buy, selectedToken  } = pageStores

	let inputElm;
	let pressedMaxValue = false;

	$: inputValue = $currencyAmount;

	onMount(() => {
		payInRswp.subscribe(val => {
			if ($currencyAmount && typeof inputValue !== 'undefined'){
				if (inputValue > 0) dispatchEvent(inputValue)
			}
		})

		let small = toBigNumber("0.000000008")
		console.log(small.toPrecision(8)) // 0.0000000080000000
		console.log(small.toFixed(8)) // 0.00000000
		console.log(stringToFixed(small, 8)) // 0
	})


	const handleInputChange = (e) => {
		let validateValue = e.target.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1')
		if (validateValue !== e.target.value) {
			inputElm.value = validateValue
		}else{
			let value = toBigNumber(e.target.value)
			if (determinePrecision(value) > 8){
				value = toBigNumber(stringToFixed(value, 8))
				inputElm.value = stringToFixed(value, 8)
			}
			pressedMaxValue = false;
			dispatchEvent(value)
		}
	}

	const handleMaxInput = async () => {
		let adjustedValue = 0;
		let txTAUCost = stampsToTAU(await getStampCost())
		if ($walletBalance.isGreaterThan(txTAUCost)){
			adjustedValue = $walletBalance.minus(toBigNumber(txTAUCost))
		}
		inputValue = toBigNumber(stringToFixed(adjustedValue, 8))
		inputElm.value = stringToFixed(inputValue, 8)
		pressedMaxValue = true;
		dispatchEvent(inputValue)
	}
	
	const dispatchEvent = (value) => dispatch('input', value)
</script>

<style>
	button.primary.small{
		margin-right: 6px;
	}
	.input-container {
  		position: relative;
  	}
</style>

<div class="input-container flex-col"
	 in:scale="{{duration: 300, delay: 0, opacity: 0.5, start: 0.6, easing: quintOut}}">
	<div class="input-row-1 flex-row">
		<div class="input-label text-primary">
			{label}
		</div>
		<span class="number text-small">
			{`Balance: ${stringToFixed($walletBalance, 8)}`}
		</span>
	</div>
	<div class="input-row-2 flex-row">
	    <input 
			class="input-amount-value number"
			placeholder="0.0" 
			value={inputValue ? inputValue.isNaN() ? "" : stringToFixed(inputValue, 8) : ""} 
			bind:this={inputElm}
			on:input={handleInputChange}
        />

		<div class="input-controls">
			{#if ($buy === true || typeof $buy === 'undefined') && !pressedMaxValue && $selectedToken}
				<button on:click={handleMaxInput} class="primary small">MAX</button> 
			{/if}
			<LamdenLogo width="23px" margin="0 3px 0 0" />
			<span class="input-token-label text-xlarge"> {config.currencySymbol} </span>
		</div>
	</div>
	{#if pressedMaxValue}
		<p class="tx-fee-label text-xsmall text-primary-dim">** adjusted for tx fees</p>
	{/if}
</div>