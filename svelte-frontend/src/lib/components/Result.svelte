<script lang="ts">
    import type { Face } from "$lib/models/face";

    import { result, activeFace } from "../../store";
    import ModalCharacter from "./ModalCharacter.svelte";
    import ResultCards from "./result/ResultCards.svelte";
    import ResultTable from "./result/ResultTable.svelte";

</script>
{#if $activeFace}
<ModalCharacter activeFace={$activeFace} />
{/if}
<div role="tablist" class="tabs tabs-lifted">
    <input type="radio" name="result_tabs" role="tab" class="tab w-full" aria-label="Detected Celebs" checked/>
    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6 !col-span-2">
    <ResultCards/>
    </div>
  
    <input
      type="radio"
      name="result_tabs"
      role="tab"
      class="tab w-full"
      aria-label="Celebs Information"
       />
    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6 !col-span-2">
        <ResultTable/>
    </div>

  </div>
  
