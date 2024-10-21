<script lang="ts">
    import { media, status, result } from "../store";
    import FileUpload from "../lib/components/FileUpload.svelte";
    import MediaPreview from "../lib/components/MediaPreview.svelte";
    import Result from "../lib/components/Result.svelte";
    import type { Face } from "$lib/models/face";

    const URL = "http://0.0.0.0:8000";
    async function uploadFile() {
        if (!$media) {
            alert("Please select a file first!");
            status.set("No media file selected!");
            return;
        }

        status.set("Uploading file...");
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
                // deduplicate the result based on name
                const uniqueResult = Array.from(new Set($result.map((a) => a.name))).map((name) => {
                    return $result.find((a) => a.name === name);
                });
                result.set(uniqueResult.filter((face) => face !== undefined) as Face[]);
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

<div class=" w-full text-center px-8 mx-auto">
    <h1
    class="text-2xl font-bold mb-6"
    >Guess Who? : Identify Your Favorite Celebs</h1>

    <p class=" text-justify mx-auto w-fit py-4">
        Upload a photo or video of your favorite celebs and let our AI models <span class="font-bold">guess who</span> they are! <br />
        Our AI models can identify 12,000+ famous faces from <span class="font-bold">MyDramaList</span> and <span class="font-bold">Kpopping</span> image databases. <br/>
        To save the results, please sign in with your account.
    </p>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class=" w-full">
            <div class="relative">
                {#if !($status.includes("completed") || $status === "")}
                     <p class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-20 text-white">
                {$status}
                </p>
                {/if}
                {#if $media}      
                    <MediaPreview />
                {:else}
                    <div class=" mx-auto bg-neutral max-h-[384px] aspect-video text-white p-2 mb-5 flex flex-col justify-center">
                        <p class=" text-center my-auto">No media file selected!</p>
                    </div>
                {/if}
            </div>
            
            <div class=" flex w-full justify-around max-w-4xl mx-auto py-8">
                <div class="w-1/4">
                <FileUpload />
                </div>
                    <button on:click={uploadFile} class={` btn btn-primary w-1/4 ${!$media ? "cursor-not-allowed disabled" : ""}`} disabled={!$media}>Process File</button>
            </div>
        </div>

        <div class="w-full"><Result /></div>
    </div>    
</div>
