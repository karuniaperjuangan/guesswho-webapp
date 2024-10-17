<script lang="ts">
    import type { Face } from "$lib/models/face";

    import { result } from "../../store";


</script>

<div class="result-table">
    {#if result && $result.length > 0}
        <table class=" table">
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
                {#each $result as face}
                    <tr class="table-row hover:bg-slate-200 transition-all min-h-36">
                        <td><img src={face.b64_face} alt="Original" class="w-full max-w-36"/></td>
                        <td><img src={face.img_url} alt="Face" class="w-full max-w-36" /></td>
                        <td>{face.name}</td>
                        <td>{face.description}</td>
                        <td><a href={face.detail_url} target="_blank">More Information</a></td>
                {/each}
            </tbody>
        </table>
    {:else}
        <p>No results available.</p>
    {/if}
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
