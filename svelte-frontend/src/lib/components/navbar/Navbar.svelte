<script>
    import { accessToken } from "$lib/store";
    import { goto } from "$app/navigation";

    async function onLogout() {
        localStorage.removeItem("access_token");
        accessToken.set(null);
        await goto("/auth/login");
    }
    async function onLogin() {
        await goto("/auth/login");
    }
</script>

<div class="navbar bg-base-100">
    <div class="flex-none">
        <label
            class="btn btn-square btn-ghost drawer-button"
            for="guesswho-drawer"
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                class="inline-block h-5 w-5 stroke-current"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 6h16M4 12h16M4 18h16"
                ></path>
            </svg>
        </label>
    </div>
    <div class="flex-1">

        <a class="btn btn-ghost" href="/#">
            <p class=" text-base-content text-xl">GuessWho?</p>
        </a>
    </div>
    <div class="flex-none">
        <div class="dropdown dropdown-end">
            <div
                role="button"
                tabindex="0"
                class="btn btn-ghost btn-circle avatar mx-4"
            >
                <div class="w-10 rounded-full">
                    <img
                        alt="Tailwind CSS Navbar component"
                        src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
                    />
                </div>
            </div>
            <ul
                class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
            >
                {#if $accessToken}
                    <li><button on:click={onLogout}>Logout</button></li>
                {:else}
                    <li><button on:click={onLogin}>Login</button></li>
                {/if}
            </ul>
        </div>
    </div>
</div>
