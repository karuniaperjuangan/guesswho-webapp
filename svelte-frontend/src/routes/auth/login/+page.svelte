<script lang="ts">
  import { PUBLIC_BASE_API_URL } from "$env/static/public";
  import { accessToken } from "$lib/store";
  import { goto } from "$app/navigation";
  let username = "";
  let password = "";

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    const response = await fetch(`${PUBLIC_BASE_API_URL}/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        grant_type: "password",
        username: username,
        password: password,
      }),
    });
    const data = await response.json();
    if (data.access_token) {
      accessToken.set(data.access_token);
      localStorage.setItem("access_token", data.access_token);
      await goto("/");
    }
  }
</script>

<div class=" my-auto h-full flex flex-col flex-1 justify-center items-center">
  <h2 class="text-xl font-bold mb-4 mx-auto text-center">Login</h2>
  <form
    on:submit|preventDefault={handleSubmit}
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
      <p>Do not have an account?</p>
      <a href="/auth/register" class=" link-primary mx-2">Register here.</a>
    </div>
    <button
      type="submit"
      class="w-full flex justify-center my-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >Login</button
    >
  </form>
</div>
