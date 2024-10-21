export async function getVideoFrame(media: File) {
    // Create a new video element and set its source
    const video = document.createElement('video');
    video.src = URL.createObjectURL(media);
    video.load();

    // Wait for the video to load
    await new Promise(resolve => video.addEventListener('loadeddata', resolve));

    // Create a canvas element
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the first frame of the video onto the canvas
    canvas.getContext('2d')?.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas content to a data URL
    const frameDataUrl = canvas.toDataURL('image/png');

    // Clean up
    URL.revokeObjectURL(video.src);

    return frameDataUrl;
}

/*Usage example 
// Usage example:
const videoFileInput = document.querySelector('input[type="file"]');
videoFileInput?.addEventListener('change', async (event) => {
    const fileInput = event.currentTarget as HTMLInputElement;
    const file = fileInput.files?.[0];
    if (file) {
        const frameDataURL = await getVideoFrame(file);
        // Now you can use the frameDataUrl to display the first frame
        const imgElement = document.createElement('img');
        imgElement.src = frameDataURL;
        document.body.appendChild(imgElement);
    }
});
*/