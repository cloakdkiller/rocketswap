<script>
    import { onMount } from 'svelte'

    // Icons
    import Warning from '../../icons/warning.svelte'
    import Stop from '../../icons/stop.svelte'
    import Clock from '../../icons/clock.svelte'

    export let startTime
    export let endTime
    export let horizontal = false

    let timer = null

    $: currentTime = new Date()
    $: hasStarted = startTime < currentTime
    $: deltaTime = !hasStarted ? getDelta(currentTime) : {}
    $: hasEnded = currentTime > endTime

    onMount(() => {
        timer = setInterval(updateTime, 1000)
        return () => {
            clearInterval(updateTime)
            timer = null
        }
    })

    const updateTime = () => currentTime = new Date();

    const getDelta = (currTime) => {
         // get total seconds between the times
        var delta = Math.abs(startTime - currTime) / 1000;

        // calculate (and subtract) whole days
        var days = Math.floor(delta / 86400);
        delta -= days * 86400;

        // calculate (and subtract) whole hours
        var hours = Math.floor(delta / 3600) % 24;
        delta -= hours * 3600;

        // calculate (and subtract) whole minutes
        var minutes = Math.floor(delta / 60) % 60;
        delta -= minutes * 60;

        // what's left is seconds
        var seconds = Math.floor(delta % 60);

        return {
            days, hours, minutes, seconds
        }
    
    }

    const formatLocaleString = (date) => date.toLocaleDateString(undefined, { 
        weekday: undefined, year: 'numeric', month: 'long', day: 'numeric' 
    })

</script>

<style>
    .time-banner{
        position: relative;
        margin: 2rem 0 1rem -40px;
        left: 20px;
        padding: 11px 35px;
    }
    .time-banner.horizontal{
        margin: 0;
        left: unset;
        padding: 0;
        align-self: flex-end;
    }
    .hasNotStarted{
        background: var(--color-primary-inactive);
    }
    .hasStarted{
        background: var(--color-secondary);
    }
    .message{
        line-height: 1.2;
        margin-left: 12px;
    }
    .message.horizontal{
        line-height: unset;
        color: var(--text-primary-color-dim);
    }
    .message > span{
        margin: 0;
        text-align: center;
    }
</style>

<div class="flex-row time-banner flex-center-center" 
    class:hasStarted={hasStarted && !horizontal} 
    class:hasNotStarted={!hasStarted && !horizontal}
    class:horizontal={horizontal} >
    {#if !hasStarted}
        <Clock color={horizontal ? "var(--text-primary-color-dim)" : undefined}/>
            <div class="message" class:flex-col={!horizontal} class:horizontal={horizontal}>
                <span>Starts accruing interest in</span>
                {#if deltaTime.days === 0}
                    <span>{deltaTime.hours} Hours {deltaTime.minutes} Minutes {deltaTime.seconds} Seconds</span>
                {:else}
                    <span>{deltaTime.days} Days {deltaTime.hours} Hours {deltaTime.minutes} Minutes</span>
                {/if}
            </div>
    {/if}

    {#if hasStarted && !hasEnded}
        <Warning color={horizontal ? "var(--text-primary-color-dim)" : undefined}/>
        <div class="message" class:flex-col={!horizontal} class:horizontal={horizontal}>
            <span>Stops accruing interest on </span>
            <span>{formatLocaleString(endTime)}</span>
        </div>
        
    {/if}

    {#if hasStarted && hasEnded}
        <Stop color={horizontal ? "var(--text-primary-color-dim)" : undefined}/>
        <div class="message" class:text-small={!horizontal} class:text-center={!horizontal} class:horizontal={horizontal}>
            <span>No longer accruing interest as of {formatLocaleString(endTime)}</span>
        </div>
    {/if}
</div>
