<script lang="ts">
  import Navbar from "$lib/components/navbar/Navbar.svelte";
  import SidebarResultHistoryList from "$lib/components/SidebarResultHistoryList.svelte";
  import "tailwindcss/tailwind.css";
  import { accessToken, result, media } from "$lib/store";
  import { onMount } from "svelte";
  import { PUBLIC_BASE_API_URL } from "$env/static/public";

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
</script>

<div class=" flex flex-col h-full min-h-screen">
  <Navbar />

  <div class="drawer h-full flex-1">
    <input id="guesswho-drawer" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content">
      <!-- Page content here -->
      <slot />
    </div>
    <div class="drawer-side">
      <label
        for="guesswho-drawer"
        aria-label="close sidebar"
        class="drawer-overlay"
      ></label>
      <ul class="bg-base-200 text-base-content min-h-full w-80 p-4">
        <div class="flex items-center justify-center w-full">
          <img
            src="/Logo.png"
            alt="Placeholder"
            class="h-8 aspect-square object-cover"
          />
          <a class="btn btn-ghost text-xl" href="/#">GuessWho?</a>
        </div>

        <SidebarResultHistoryList></SidebarResultHistoryList>
      </ul>
    </div>
  </div>
</div>
