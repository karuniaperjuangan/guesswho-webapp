<script lang="ts">
  import { media, status, result, accessToken } from "$lib/store";
  let history_name = "";

  async function showModal() {
    const modal = document.getElementById("modal-saveform");
    if (modal) {
      (modal as HTMLDialogElement).showModal();
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
      <button class=" btn btn-primary">Save Result</button>
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
