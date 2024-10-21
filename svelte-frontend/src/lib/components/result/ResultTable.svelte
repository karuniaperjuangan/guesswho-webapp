<script lang="ts">
import type { Face } from "$lib/models/face";

import { result } from "../../../store";

// Variables for pagination
let currentPage = 1;
let pageSize = 5; // Number of items per page
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
        return true;
    }
    return face.name.toLowerCase().includes(searchKeyword.toLowerCase());
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

<div class="result-table mt-5 w-full">
    <input
        type="text"
        class="input input-bordered w-full mb-4"
        placeholder="Search by name"
        bind:value={searchKeyword}/>
    {#if result && $result.length > 0}
    <table class="table w-full border-collapse">
        <thead>
            <tr class="*:px-4 *:py-2 *:border-b-gray-300 *:text-left *:bg-gray-200">
                <th>Original Image</th>
                <th>Face Image</th>
                <th>Name</th>
                <!--
                <th>Description</th>
                -->
                <th>Details</th>
            </tr>
        </thead>
        <tbody>
            {#each paginatedResults as face}
            <tr class="table-row hover:bg-slate-200 transition-all min-h-24 *:px-4 *:py-2 *:border-b-gray-300 *:text-left">
                <td><img src={face.b64_face} alt="Original" class="w-full mx-auto max-w-24 aspect-square object-cover" /></td>
                <td><img src={face.img_url} alt="Face" class="w-full mx-auto max-w-24 aspect-square object-cover" /></td>
                <td>{face.name}</td>
                <!--
                <td>{face.description}</td>
                -->
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
                  name="table-page"
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

