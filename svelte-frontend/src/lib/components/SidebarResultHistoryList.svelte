<script lang="ts">
    import Navbar from "$lib/components/navbar/Navbar.svelte";
    import "tailwindcss/tailwind.css";

    import { accessToken, result, media } from "$lib/store";
    import { onMount } from "svelte";
    import { PUBLIC_BASE_API_URL } from "$env/static/public";

    import convert_b64_to_file from "$lib/utils/convert_b64_to_file";

    import IconButton from "@smui/icon-button";
    let ResultHistory: any[] = [];

    async function fetchResultHistory() {
        const response = await fetch(
            `${PUBLIC_BASE_API_URL}/user/list_history`,
            {
                headers: {
                    Authorization: `Bearer ${$accessToken}`,
                },
            },
        );
        if (response.ok) {
            const resp = await response.json();
            ResultHistory = resp;
            console.log(resp);
        } else {
            console.error("Failed to fetch result history");
        }
    }

    onMount(async () => {
        $accessToken = localStorage.getItem("access_token");
        // try to access /user in api with bearer access token
        if ($accessToken) {
            try {
                const response = await fetch(`${PUBLIC_BASE_API_URL}/user`, {
                    headers: {
                        Authorization: `Bearer ${$accessToken}`,
                    },
                });
                if (response.ok) {
                    console.log("User is authenticated");
                    // Fetch result history after user authentication
                    await fetchResultHistory();
                } else {
                    console.log("User is not authenticated");
                    localStorage.removeItem("access_token");
                    $accessToken = null;
                }
            } catch (error) {
                console.error("Error accessing /user", error);
                localStorage.removeItem("access_token");
                $accessToken = null;
            }
        }
    });

    async function onClickResultHistory(history_name: string) {
        try {
            const response = await fetch(
                `${PUBLIC_BASE_API_URL}/user/history?history_name=${history_name}`,
                {
                    headers: {
                        Authorization: `Bearer ${$accessToken}`,
                    },
                },
            );
            if (response.ok) {
                const resultData = await response.json();
                console.log(resultData);
                // Handle the result data as needed
                if (resultData.b64_media) {
                    media.set(
                        convert_b64_to_file(resultData.b64_media, "image.jpg"),
                    );
                }

                result.set(resultData.recognition_result.result);
                // toggle guesswho-drawer checkbox
                const drawer = document.getElementById(
                    "guesswho-drawer",
                ) as HTMLInputElement;
                if (drawer) {
                    drawer.checked = false;
                } else {
                    console.error(
                        'Element with id "guesswho-drawer" not found',
                    );
                }
            } else {
                console.error("Failed to fetch result data");
            }
        } catch (error) {
            console.error("Error fetching result data", error);
        }
    }
    async function onDeleteResultHistory(history_name: string) {}
</script>

{#if $accessToken}
    {#each ResultHistory as item (item.history_name)}
        <li class="flex">
            <button
                on:click={() => onClickResultHistory(item.history_name)}
                class="btn btn-ghost w-full text-left flex-1"
                >{item.history_name}</button
            >
            <!--Delete Button as a square button with symbol-->
            <IconButton
                class="material-icons text-white bg-red-400 hover:bg-red-600 focus:bg-red-800 w-12 rounded-md  aspect-square"
                on:click={() => onDeleteResultHistory(item.history_name)}
                >delete</IconButton
            >
        </li>
    {/each}
{:else}
    <li>
        <p>
            The history of results can only be used by registered users. Please
            login or register to access this menu.
        </p>
    </li>
{/if}
