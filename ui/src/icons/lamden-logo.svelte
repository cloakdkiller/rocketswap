<script>
    export let width = "24px";
    export let margin = "0 5px";
    export let reverseColors = false;

    $: height = width
</script>

<svg xmlns="http://www.w3.org/2000/svg" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xml:space="preserve" {width} {height}
    viewBox="0 0 3571 3571" 
    version="1.1" 
    style={`margin: ${margin}; 
    shape-rendering:geometricPrecision; 
    text-rendering:geometricPrecision; 
    fill-rule:evenodd; 
    clip-rule:evenodd`}
>
    <path fill={reverseColors ? "var(--lamden-logo-color)" : "var(--lamden-logo-border-color)"} d="M965 2607l-720 -720 -101 -101 101 -102 720 -719 719 -720 102 -101 101 101 720 720 719 719 102 102 -102 101 -719 720 -720 719 -101 102 -102 -102 -719 -719zm821 964c36,0 69,-13 93,-36l15 -13 814 -814 813 -814 15 -14c22,-26 35,-58 35,-94 0,-36 -13,-69 -35,-94l-15 -14 -813 -814 -814 -814 -15 -14c-24,-22 -57,-36 -93,-36 -37,0 -70,14 -94,36l-15 14 -814 814 -813 814 -14 14c-23,25 -36,58 -36,94 0,36 13,68 36,94l14 14 813 814 814 814 15 13c24,23 57,36 94,36z"/>
    <path fill={reverseColors ? "var(--lamden-logo-border-color)" : "var(--lamden-logo-color)"} d="M1786 144l821 822 822 822 -822 822 -821 822 -822 -822 -822 -822 822 -822 822 -822zm0 823l410 410 411 411 -411 410 -410 411 -411 -411 -410 -410 410 -411 411 -410z"/>
    <path fill={reverseColors ? "var(--lamden-logo-color)" : "var(--lamden-logo-border-color)"} d="M1375 2198l411 411 410 -411 411 -410 -411 -411 -410 -410 -411 410 -410 411 410 410zm100 -100l311 311 310 -311 311 -310 -311 -311 -310 -310 -311 310 -311 311 311 310z"/>
</svg>
