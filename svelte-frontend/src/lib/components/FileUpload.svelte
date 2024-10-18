<script lang="ts">
    
    import { media,result } from '../../store';
 
    let file: HTMLInputElement | null = null;

    function handleUpload() {
        const input = document.getElementById("file-input");
        input?.click();
    }

    function handleFileChange(event: Event) {
        const input = event.target as HTMLInputElement;
        if (!input.files || input.files.length === 0) {
            alert("Please select a file first!");
            return;
        }
        media.set(input.files[0]);
        result.set([]);
    }
</script>

<div class="upload-container">
    <input id="file-input" on:change={handleFileChange} class=" hidden" type="file" bind:this={file} accept="image/*,video/*" />
    <button on:click={handleUpload} class=" btn btn-primary w-full">Upload</button>
</div>

