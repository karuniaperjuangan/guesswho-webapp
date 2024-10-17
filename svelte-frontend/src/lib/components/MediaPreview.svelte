<script>
    import { media } from '../../store';
    let previewUrl = '';

    $: if ($media) {
        previewUrl = URL.createObjectURL($media);
    }
</script>

<div class="media-preview h-full my-5 mx-auto">
    {#if previewUrl}
    {#if $media}
        {#if $media.type.startsWith("image/")}
            <img src={previewUrl} alt="Uploaded" class="h-full mx-auto" />
        {:else if $media.type.startsWith("video/")}
            <video src={previewUrl} controls class="h-full mx-auto">
                <track kind="captions" src="captions.vtt" srclang="en" label="English">
            </video>
        {/if}
    {/if}
    {/if}
</div>

<style>

</style>
