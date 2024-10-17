<script lang="ts">
    import { media, status, result } from "../store";
    import FileUpload from "../lib/components/FileUpload.svelte";
    import MediaPreview from "../lib/components/MediaPreview.svelte";
    import ResultTable from "../lib/components/ResultTable.svelte";

    const URL = "http://0.0.0.0:8000";
    async function uploadFile() {
        if (!$media) {
            alert("Please select a file first!");
            status.set("No media file selected!");
            return;
        }

        status.set("Uploading and processing...");
        result.set([]);

        const endpoint = $media
            ? $media.type.startsWith("image/")
                ? URL + "/face/image"
                : URL + "/face/video"
            : "";
        const formData = new FormData();
        if ($media) {
            formData.append("file", $media);
        } else {
            throw new Error("No media file selected");
        }

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData,
            });
            const { task_id } = await response.json();
            pollStatus(task_id);
        } catch (error) {
            status.set("Error uploading file!");
            console.error(error);
        }
    }

    async function pollStatus(taskId: String) {
        try {
            const res = await fetch(URL + `/task/status/${taskId}`);
            const data = await res.json();

            if (data.status === "completed") {
                status.set("Processing completed!");
                console.log(data);
                //Check if data.result is an array
                if (Array.isArray(data.result)) {
                    result.set(data.result);
                } else {
                    result.set(data.result.faces_data);
                }
            } else {
                status.set(data.status);
                setTimeout(() => pollStatus(taskId), 2000);
            }
        } catch (error) {
            status.set("Error checking task status!");
            console.error(error);
        }
    }
</script>

<div class=" w-full text-center">
    <h1>Face Detection Client</h1>

    <div class="grid grid-cols-2 gap-4 w-full justify-around px-8">
        <div class=" w-full">
            <div>
                
                {#if $media}
                <div class=" max-h-[512px] aspect-video bg-neutral">
                    <MediaPreview />
                </div>

                    <p class=" text-center">Selected file: {$media.name}</p>
                {:else}
                    <div class=" bg-neutral aspect-video w-full text-white p-2 my-5 flex flex-col justify-center">
                        <p class=" text-center my-auto">No media file selected!</p>
                    </div>
                {/if}
            </div>
            
            <div class=" flex w-full justify-around">
                <div class="w-1/4">
                <FileUpload />
                </div>
                {#if $media}
                    <button on:click={uploadFile} class=" btn btn-primary w-1/4"
                        >Process File</button
                    >
                {:else}
                    <div />
                {/if}
            </div>
        </div>
        <div class=" w-full"><ResultTable /></div>
    </div>

    <p class=" text-center w-full">{$status}</p>
    
</div>
