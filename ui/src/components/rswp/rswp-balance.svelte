<script>
    // Components
    import RSWPPayFeesChkBox from './rswp-pay-fees-chkbox.svelte'
    
    // Icons
    import RocketSwapCircleLogo from '../../icons/rocketswap-circle-logo.svelte'

    //Misc
    import { rswpBalance, rswpPriceUSD } from '../../store'
    import { displayBalanceToPrecision } from '../../utils'
    import { config } from '../../config'

    let logoSize = "80px";
</script>

<style>
    .container{
        flex-direction: column;
        box-sizing: border-box;
        color: var(--text-primary-color);
        font-size: var(--text-size-small);
        border-radius: 0;
        padding: 10px 20px;
        padding-top: 15px;
        width: 100%;
    }
    p{
        margin: 0
    }
    .rswp-balance-info{
        line-height: 1.3;
    }
    @media screen and (min-width: 430px) {
        .container{
            flex-direction: row;
        }
    }
    @media screen and (min-width: 650px) {
        .container{
            flex-direction: row;
        }
    }
</style>
<div>

</div>
<div class="flex-row container">
    <div class="flex">
        <RocketSwapCircleLogo 
            styles={`width: ${logoSize}; height: ${logoSize}; min-width: ${logoSize}; min-height: ${logoSize};`} 
            margin="0 16px 0 0 "
        />
        <div class="flex-col rswp-balance-info text-large">
            <p class="text-color-highlight weight-600">{`${displayBalanceToPrecision($rswpBalance, 8)} ${config.ammTokenSymbol}`}</p>
            <p class="text-primary-dim">{`$${displayBalanceToPrecision($rswpBalance.multipliedBy($rswpPriceUSD), 2)} USD`}</p>
        </div>
    </div>
    <div class="flex flex-grow">
        <RSWPPayFeesChkBox />
    </div>
</div>