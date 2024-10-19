<script lang="ts">
    import type { Face } from "$lib/models/face";

    export let activeFace: Face;
</script>
<dialog id="modal-character" class="modal">
    <div class="modal-box">
        <h2 class="text-center w-full text-2xl font-bold">{activeFace?.name}</h2>
        <div class=" flex rounded-lg w-full overflow-hidden my-4 ">
            <div class="w-full">
            <img
            src={activeFace?.b64_face}
            alt={`Original Image of ${activeFace?.name}`}
            class="w-full object-cover aspect-square"
            />
            </div>
            <div class="w-full"><img
              src={activeFace?.img_url}
              alt={`Face of ${activeFace?.name}`}
              class="w-full object-cover aspect-square"
              /></div>
            
        </div>
        <p class=" w-full text-justify">{activeFace?.description}</p>
        <div class="card-actions justify-end">
          <a href={activeFace?.detail_url} target="_blank" class=" link link-primary">More Information</a>
        </div>
      <div class="modal-action">
        <form method="dialog">
          <!-- if there is a button in form, it will close the modal -->
          <button class="btn">Close</button>
        </form>
      </div>
    </div>
  </dialog>