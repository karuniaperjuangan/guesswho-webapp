<script lang="ts">
    import type { Face } from '$lib/models/face';
    import { media, result } from '../../store';
    let previewUrl = '';

    $: if ($media) {
        previewUrl = URL.createObjectURL($media);
    }

    
    $: isShowingTooltip = false;
    let activeFace: Face | null = null;
    async function onMouseEnteringBoundingBox (event: MouseEvent, face: Face) {
        console.log(event);
        isShowingTooltip = true;
        const tooltip = document.getElementById('hover-tooltip');
        activeFace = face;
        if (tooltip) {
            tooltip.style.top = `${event.clientY}px`;
            tooltip.style.left = `${event.clientX}px`;
        }
    }
    async function onMouseLeavingBoundingBox (event: MouseEvent) {
        console.log(event);
        isShowingTooltip = false;
    }
</script>

<div class="media-preview h-fit w-fit mx-auto">
    {#if previewUrl}
    {#if $media}
        {#if $media.type.startsWith("image/")}
        <div class="bounding-box h-fit aspect-video w-fit relative">
            <div id="hover-tooltip" class="fixed card card-compact bg-base-100 w-96 shadow-xl z-10 rounded-lg {isShowingTooltip? 'block' : 'hidden'}">
                <figure>
                    <img
                      src={activeFace?.img_url}
                      alt={`Face of ${activeFace?.name}`}/>
                  </figure>
                  <div class="card-body">
                    <h2 class="card-title">{activeFace?.name}</h2>
                    <p>{activeFace?.description}</p>
                    <div class="card-actions justify-end">
                      <a href={activeFace?.detail_url} target="_blank" class=" text-primary-content">More Information</a>
                    </div>
                  </div>
            </div>
            {#each $result as face}
                <div class="bounding-box__box absolute border-2 border-primary" style="top: {face.bbox.y_min * 100}%; left: {face.bbox.x_min * 100}%; width: {(face.bbox.x_max - face.bbox.x_min) * 100}%; height: {(face.bbox.y_max - face.bbox.y_min) * 100}%;">
                    <div class="h-full w-full" role="presentation" on:mouseenter={(event) => onMouseEnteringBoundingBox(event, face)} on:mouseleave={onMouseLeavingBoundingBox}></div>
                </div>
            {/each}
            <img src={previewUrl} alt="Uploaded" class="w-full aspect-video mx-auto object-contain" />
        </div>
        {:else if $media.type.startsWith("video/")}
            <video src={previewUrl} controls class="w-full mx-auto">
                <track kind="captions" src="captions.vtt" srclang="en" label="English">
            </video>
        {/if}
    {/if}
    {/if}
</div>

<style>

</style>
