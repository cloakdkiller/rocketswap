<script lang="ts">
    import { getContext } from 'svelte'

    //Icons
    import LamdenLogo from '../../icons/lamden-logo.svelte'
    import TokenLogo from '../../icons/token-logo.svelte'

    //Misc
    import { stringToFixed, quoteCalculator, toBigNumber } from '../../utils' 
    import { config } from '../../config'

    const { pageStats, pageStores } = getContext('pageContext');
    const { selectedToken  } = pageStores

    $: tokenSymbol = $selectedToken?.token_symbol || "—";
    $: tokensToReceive = $pageStats?.amounts ? $pageStats.amounts.currency : toBigNumber("0");
    $: currencyToReceive = $pageStats?.amounts ? $pageStats.amounts.token : toBigNumber("0");

</script>

<style>
    .container{
        border: 1px solid var(--box-border-color);
        border-radius: var(--border-radius);
        padding: 0.5rem 20px;
        font-size: var(--text-size-small);

        flex-wrap: wrap;
        margin: 1rem 0;
    }
    p{
        margin: 0;
    }
    .flex-row{
        justify-content: flex-end;
        align-items: center;
    }
    .number{
        position: relative;
        top: -1px;
        font-weight: 400;
    }
</style>

<div class="container flex-col">
    <div class="flex-row">
        <p class="number flex-grow text-large number-span">{currencyToReceive.isNaN() ? "0" : stringToFixed(currencyToReceive, 8)}</p>
        <div class="flex-row">
            <p class="input-token-label text-large">{tokenSymbol}</p>
            <TokenLogo tokenMeta={$selectedToken} width={'25px'}  margin={"0 10px"}/>
        </div>
    </div>
    <div class="flex-row">
        <p class="number flex-grow text-large number-span">{tokensToReceive.isNaN() ? "0" : stringToFixed(tokensToReceive, 8)}</p>
        <div class="flex-row">
            <p class="input-token-label text-large">{config.currencySymbol}</p>
            <LamdenLogo width={'25px'} margin={"0 10px"} />
        </div>

    </div>
</div>