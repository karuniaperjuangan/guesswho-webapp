<script lang="ts">
  import { media, status, result, accessToken } from "$lib/store";
  import {PUBLIC_BASE_API_URL} from "$env/static/public"
  import convert_file_to_b64 from "$lib/utils/convert_file_to_b64"
  import { toast } from "@zerodevx/svelte-toast";
  let history_name = "";

  async function showModal() {
    const modal = document.getElementById("modal-saveform");
    if (modal) {
      (modal as HTMLDialogElement).showModal();
    }
  }
  async function closeModal() {
    const modal = document.getElementById("modal-saveform");
     if (modal) {
       (modal as HTMLDialogElement).close();
     }
  }

  async function onSaveResult(){
    if($media){
    // if the $media is a video, set all attribute of item.bbox to 0 where item is the members of $result
    let submittedResult = $result;
    if ($media.type.startsWith("video/")) {
      submittedResult.forEach((item) => {
        item.bbox.x_min = 0;
        item.bbox.y_min = 0;
        item.bbox.x_max = 0;
        item.bbox.y_max = 0;
      });
    }

    const response = await fetch(PUBLIC_BASE_API_URL + "/user/history", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${$accessToken}`
        },
        body: JSON.stringify({
          "history_name":history_name,
          "b64_media": await convert_file_to_b64($media),
          "recognition_result":{
            "result":submittedResult
          }
        })
      });
      if(response.ok){
        const data = await response.json();
        console.log(data);
        await closeModal();
        location.reload();
      }else{
        console.error("Error saving result"+ (await response.json()).detail);
        toast.push('Errror saving result', { classes: ['bg-error']});
      }
    }  
  }
</script>

<dialog id="modal-saveform" class="modal">
  <div class="modal-box">
    <form>
      <h3 class="font-bold text-lg">Save Form</h3>
      <p>Are you sure you want to save the result?</p>
      <input
        bind:value={history_name}
        id="history_name"
        type="text"
        placeholder="Result name to save (must be unique)"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </form>
    <div class="modal-action">
      <button class=" btn btn-primary"
      on:click={onSaveResult}
      >Save Result</button>
      <form method="dialog">
        <!-- if there is a button in form, it will close the modal -->
        <button class="btn">Close</button>
      </form>
    </div>
  </div>
</dialog>

{#if $accessToken}
  <button
    on:click={showModal}
    class={`btn btn-primary w-full my-4 ${!$result || $result.length <= 0 ? "cursor-not-allowed disabled" : ""}`}
    disabled={!$result || $result.length <= 0}>Save Results</button
  >
{/if}
