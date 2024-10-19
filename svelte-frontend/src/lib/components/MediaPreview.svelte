<script lang="ts">
    import type { Face } from '$lib/models/face';
    import { media, result, activeFace } from '../../store';
    import ModalCharacter from './ModalCharacter.svelte';
    let previewUrl = '';

    $: if ($media) {
        previewUrl = URL.createObjectURL($media);
    }

    
    $: isShowingTooltip = false;
    
    async function onMouseEnteringBoundingBox (event: MouseEvent, face: Face) {
        console.log(event);
        isShowingTooltip = true;
        const tooltip = document.getElementById('hover-tooltip');
        activeFace.set(face);
        if (tooltip) {
            tooltip.style.top = Math.min(window.innerHeight - 400, event.clientY) + 'px';
            tooltip.style.left = Math.min(window.innerWidth - 400, event.clientX) + 'px';
        }
    }
    async function onMouseLeavingBoundingBox (event: MouseEvent) {
        console.log(event);
        isShowingTooltip = false;
    }
    async function showModal(face:Face) {
        const modal = document.getElementById('modal-character');
        activeFace.set(face);
        if (modal) {
            (modal as HTMLDialogElement).showModal();
        }
    }
</script>
<div class=" mx-auto max-h-[384px] h-fit aspect-video bg-neutral overflow-hidden">
<div class="media-preview h-fit w-fit mx-auto">
    {#if previewUrl}
    {#if $media}
        {#if $media.type.startsWith("image/")}
        {#if $activeFace}
        <ModalCharacter activeFace={$activeFace} />
        {/if}
        <!--
        <div id="hover-tooltip" class="fixed card aspect-square card-compact bg-base-100 w-96 shadow-xl z-10 rounded-lg {isShowingTooltip? 'block' : 'hidden'}">
                <figure>
                    <img
                      src={activeFace?.img_url}
                      alt={`Face of ${activeFace?.name}`}
                      class="w-full object-cover rounded-t-lg aspect-video"
                      />
                  </figure>
                  <div class="card-body">
                    <h2 class="card-title">{activeFace?.name}</h2>
                    <p>{activeFace?.description}</p>
                    <div class="card-actions justify-end">
                      <a href={activeFace?.detail_url} target="_blank" class=" text-primary-content">More Information</a>
                    </div>
                  </div>
            </div> 
        -->    
        <div class="bounding-box h-fit w-fit relative">
            {#each $result as face}
                <div class="bounding-box__box absolute border-2 border-primary" style="top: {face.bbox.y_min * 100}%; left: {face.bbox.x_min * 100}%; width: {(face.bbox.x_max - face.bbox.x_min) * 100}%; height: {(face.bbox.y_max - face.bbox.y_min) * 100}%;">
                    <div class="h-full w-full hover:bg-slate-200 hover:opacity-25 hover:cursor-pointer transition-all" role="presentation" 
                    on:click={(element) => showModal(face)}></div>
                </div>
            {/each}
            <img src={previewUrl} alt="Uploaded" class="h-full max-h-[384px] mx-auto"/>
        </div>
        
        {:else if $media.type.startsWith("video/")}
            <video src={previewUrl} controls class="w-full mx-auto">
                <track kind="captions" src="captions.vtt" srclang="en" label="English">
            </video>
        {/if}
    {/if}
    {/if}
</div>
</div>
<style>

</style>
