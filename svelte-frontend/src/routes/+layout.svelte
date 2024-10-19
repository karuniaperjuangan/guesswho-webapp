<script>
  import "tailwindcss/tailwind.css";
</script>

<div class="navbar bg-base-100">
  <div class="flex-none">
    <label class="btn btn-square btn-ghost drawer-button" for="guesswho-drawer">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        class="inline-block h-5 w-5 stroke-current">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16"></path>
      </svg>
    </label>
  </div>
  <div class="flex-1">
    <a class="btn btn-ghost text-xl" href="/#">GuessWho?</a>
  </div>
  <div class="flex-none">
    <div class="dropdown dropdown-end">
    <div role="button" tabindex=0  class="btn btn-ghost btn-circle avatar mx-4">
      <div class="w-10 rounded-full">
        <img
          alt="Tailwind CSS Navbar component"
          src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
      </div>
    </div>
    <ul
    class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
    <li><a href="/#">Logout</a></li>
    </div>
  </div>
</div>

<div class="drawer">
  <input id="guesswho-drawer" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content">
    <!-- Page content here -->
    <slot />
  </div>
  <div class="drawer-side">
    <label for="guesswho-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
    <ul class="menu bg-base-200 text-base-content min-h-full w-80 p-4">
      <!-- Sidebar content here -->
      <li><a>Sidebar Item 1</a></li>
      <li><a>Sidebar Item 2</a></li>
    </ul>
  </div>
</div>


