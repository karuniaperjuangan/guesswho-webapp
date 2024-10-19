<script lang="ts">
    import type { Face } from "$lib/models/face";

    import { result, activeFace } from "../../store";
    import ModalCharacter from "./ModalCharacter.svelte";

    // Variables for pagination
    let currentPage = 1;
    let pageSize = 5; // Number of items per page
    let totalPages = 1;

    $: if (result) {
        totalPages = Math.ceil($result.length / pageSize);
    }

    // Function to change page
    function changePage(newPage: number) {
        if (newPage > 0 && newPage <= totalPages) {
            currentPage = newPage;
        }
    }
    async function showModal(face:Face) {
        const modal = document.getElementById('modal-character');
        activeFace.set(face);
        if (modal) {
            (modal as HTMLDialogElement).showModal();
        }
    }

    // Get paginated results
    $: paginatedResults = $result.slice((currentPage - 1) * pageSize, currentPage * pageSize);
</script>
{#if $activeFace}
<ModalCharacter activeFace={$activeFace} />
{/if}
<div role="tablist" class="tabs tabs-lifted">
    <input type="radio" name="my_tabs_2" role="tab" class="tab w-full" aria-label="Detected Celebs" checked/>
    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6 !col-span-2">
        {#if result && $result.length > 0}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {#each $result as face}
        {#if !face.name.toLowerCase().includes("unknown")}
        <!--Gradient from transparent to black as overlay-->
        <button class="relative w-40 m-4 aspect-square transition-all hover:scale-110" on:click={() => showModal(face)}>
            <div class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black rounded-md"></div>
            <img src={face.img_url} alt="Face" class=" w-full aspect-square object-cover rounded-md" />
            <h2 class="absolute bottom-0 left-0 right-0  text-white text-center p-2 rounded-b-md">{face.name}</h2>
    </button>
        
        {/if}
        {/each}
        </div>
    {:else}
        <p>No results available.</p>
    {/if}
    </div>
  
    <input
      type="radio"
      name="my_tabs_2"
      role="tab"
      class="tab w-full"
      aria-label="Celebs Information"
       />
    <div role="tabpanel" class="tab-content bg-base-100 border-base-300 rounded-box p-6 !col-span-2">
        <div class="result-table w-full">
            {#if result && $result.length > 0}
            <table class="table">
                <thead>
                    <tr>
                        <th>Original Image</th>
                        <th>Face Image</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {#each paginatedResults as face}
                    <tr class="table-row hover:bg-slate-200 transition-all min-h-36">
                        <td><img src={face.b64_face} alt="Original" class="w-full max-w-36" /></td>
                        <td><img src={face.img_url} alt="Face" class="w-full max-w-36" /></td>
                        <td>{face.name}</td>
                        <td>{face.description}</td>
                        <td><a href={face.detail_url} target="_blank" class="link link-primary">More Information</a></td>
                    </tr>
                    {/each}
                </tbody>
            </table>

            <!-- Pagination Controls -->
            <div class="flex justify-between items-center mt-4 mx-auto">
                <div class="join mx-auto">
                    {#each Array.from({ length: totalPages }, (_, i) => i + 1) as page}
                    <div class="join">
                        <input
                          class="join-item btn btn-square"
                          type="radio"
                          name="options"
                          on:click={() => changePage(page)}
                          aria-label={`${page}`}
                          checked={currentPage === page}/>
                      </div>
                    {/each}  
                  </div>
            </div>
            {:else}
                <p>No results available.</p>
            {/if}
        </div>
    </div>

  </div>
  


<style>
    .result-table {
        margin-top: 20px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 10px;
        border: 1px solid #ddd;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
</style>
