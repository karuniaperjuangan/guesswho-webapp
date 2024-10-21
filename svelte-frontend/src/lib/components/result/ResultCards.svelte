<script lang="ts">
    import type { Face } from "$lib/models/face";
    import { result, activeFace } from "../../store";

    async function showModal(face:Face) {
        const modal = document.getElementById('modal-character');
        activeFace.set(face);
        if (modal) {
            (modal as HTMLDialogElement).showModal();
        }
    }

    // Variables for pagination
let currentPage = 1;
let pageSize = 6; // Number of items per page
let totalPages = 1;

// Function to change page
function changePage(newPage: number) {
    if (newPage > 0 && newPage <= totalPages) {
        currentPage = newPage;
    }
}

let searchKeyword = "";

$: filteredResults = $result.filter((face: Face) => {
    if (searchKeyword === "") {
        return !face.name.toLowerCase().includes("unknown")
    }
    return face.name.toLowerCase().includes(searchKeyword.toLowerCase()) && !face.name.toLowerCase().includes("unknown")
});

// Get paginated results
$: paginatedResults = filteredResults.slice((currentPage - 1) * pageSize, currentPage * pageSize);
$: if (paginatedResults) {
    totalPages = Math.ceil(filteredResults.length / pageSize);
}

// Reset currentPage to 1 when result changes
$: if ($result && $result.length > 0) {
    currentPage = 1;
}
</script>

<input
type="text"
class="input input-bordered w-full mb-4"
placeholder="Search by name"
bind:value={searchKeyword}/>

{#if result && $result.length > 0}
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
{#each paginatedResults as face}
<!--Gradient from transparent to black as overlay-->
<button class="relative w-40 m-4 aspect-square transition-all hover:scale-110" on:click={() => showModal(face)}>
    <div class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black rounded-md"></div>
    <img src={face.img_url} alt="Face" class=" w-full aspect-square object-cover rounded-md" />
    <h2 class="absolute bottom-0 left-0 right-0  text-white text-center p-2 rounded-b-md">{face.name}</h2>
</button>
{/each}


</div>
{:else}
<p>No results available.</p>
{/if}    

<!-- Pagination Controls -->
    <div class="flex justify-between items-center mt-4 mx-auto">
        <div class="join mx-auto">
            {#each Array.from({ length: totalPages }, (_, i) => i + 1) as page}
            <div class="join">
                <input
                  class="join-item btn btn-square"
                  type="radio"
                  name="cards-page"
                  on:click={() => changePage(page)}
                  aria-label={`${page}`}
                  checked={currentPage === page}/>
              </div>
            {/each}  
          </div>
    </div>