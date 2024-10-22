<script lang="ts">
  import { goto } from "$app/navigation";

  import { PUBLIC_BASE_API_URL } from "$env/static/public";
  import { toast } from "@zerodevx/svelte-toast";
  let username = "";
  let password = "";

  async function register() {
    const response = await fetch(PUBLIC_BASE_API_URL + "/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, password: password }),
    });
    if (response.ok) {
      toast.push('Registration successful!', { classes: ['bg-success'] })
      goto("/auth/login");
    } else {
      //alert("Registration failed." + (await response.json()).detail);
      toast.push((await response.json()).detail, { classes: ['bg-error'] })
    }
  }
</script>

<div class=" my-auto h-full flex flex-col flex-1 justify-center items-center">
  <h2 class="text-xl font-bold mb-4 mx-auto text-center">Register</h2>
  <form
    on:submit|preventDefault={register}
    class="max-w-md mx-auto p-6 bg-gray-100 rounded-lg shadow-md"
  >
    <div class="mb-4">
      <label for="username" class="block text-sm font-medium text-gray-700"
        >Username</label
      >
      <input
        bind:value={username}
        id="username"
        type="text"
        placeholder="Username"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>
    <div class="mb-4">
      <label for="password" class="block text-sm font-medium text-gray-700"
        >Password</label
      >
      <input
        bind:value={password}
        id="password"
        type="password"
        placeholder="Password"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
    </div>
    <div class="flex justify-end text-sm font-medium">
      <p>Already have an account?</p>
      <a href="/auth/login" class=" link-primary mx-2">Login here.</a>
    </div>
    <button
      type="submit"
      class="w-full flex justify-center my-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >Register</button
    >
  </form>
</div>
