<script lang="ts">
    import { createEventDispatcher, getContext } from 'svelte'
    
	import { scale } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';

    import { walletIsReady } from '../../store'

    const { pageStores } = getContext('pageContext')
    const { lpTokenPercentInput } = pageStores

    export let label

    const dispatch = createEventDispatcher();

    $: inputVal = $lpTokenPercentInput || 0;

    const handleButtonInput = (value) => {
        inputVal = value
        dispatchEvent(inputVal)
    }

    const handleInputChange = (e) => {
        dispatchEvent(e.target.value)
    }

    const dispatchEvent = (value) => dispatch('input', value)
</script>

<style>
    input[type="range"]{
        -webkit-appearance: none;  /* Override default CSS styles */
        appearance: none;
        border: none;
        border-radius: 10px;
        outline: none;

        width: 100%; 
        height: 2px; 
        background: #ffffffbd; 
        margin: 1.5rem 0 1rem;
        padding: 2px;
    }

    input[type="range"]:hover{
        background: #ffffffe3; 
    }

    input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        border-radius: 99px;
        width: 20px;
        height: 20px;
        background: var(--text-primary-color);
        cursor: pointer;
    }

    input[type="range"]:hover::-webkit-slider-thumb {
        filter: brightness(110%);
    }

    input[type="range"]:active::-webkit-slider-thumb {
        width: 20px;
        height: 20px;
        filter: brightness(120%);
    }

    .input-container{
        height: unset;
    }

    .big-number{
        font-size: var(--text-size-xlarge);
        margin: 0;
        line-height: 1;
    }

    .input-row-3{
        justify-content: space-between;
    }

    @media screen and (min-width: 430px) {
        .big-number{
            font-size: var(--text-size-massive);
        }
        input[type="range"]{
            height: 3px; 
            margin: 2rem 0;
            padding: 3px;
        }

        input[type="range"]::-webkit-slider-thumb {
            width: 25px;
            height: 25px;
        }

        input[type="range"]:active::-webkit-slider-thumb {
            width: 22px;
            height: 22px;
        }
    }

</style>


<div class="input-container flex-col"
	 in:scale="{{duration: 300, delay: 0, opacity: 0.5, start: 0.6, easing: quintOut}}">
	<div class="input-row-1 flex-row">
		<div class="input-label text-small">
			{label}
		</div>
	</div>
	<div class="input-row-2 flex-col">
        <p class="number big-number">
            {inputVal + "%"}
        </p>
	    <input 
			placeholder="0.0" 
			bind:value={inputVal} 
			type="range"
			on:input={handleInputChange}
            disabled={!$walletIsReady}
        />
	</div>
    <div class="input-row-3 flex-row">
        <button disabled={!$walletIsReady} on:click={() => handleButtonInput(25)} class="primary medium">25%</button> 
        <button disabled={!$walletIsReady} on:click={() => handleButtonInput(50)} class="primary medium">50%</button>
        <button disabled={!$walletIsReady} on:click={() => handleButtonInput(75)} class="primary medium">75%</button>
        <button disabled={!$walletIsReady} on:click={() => handleButtonInput(100)} class="primary medium">MAX</button>
    </div>
</div>