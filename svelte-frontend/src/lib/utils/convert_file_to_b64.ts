export default async function fileToBase64(file: File): Promise<string> {
    // If it's an image file, convert directly
    if (file.type.startsWith("image/")) {
      return await readFileAsBase64(file);
    } 
    // If it's a video file, capture a frame
    else if (file.type.startsWith("video/")) {
      return await captureVideoFrameAsBase64(file);
    } 
    else {
      throw new Error("Unsupported file type");
    }
  }
  
  // Helper function to read image files as Base64
  async function readFileAsBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string); // Contains "data:image/jpeg;base64,..."
      reader.onerror = () => reject(new Error("Error reading file"));
      reader.readAsDataURL(file);
    });
  }
  
  // Helper function to capture a frame from a video file and convert it to Base64
  async function captureVideoFrameAsBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const video = document.createElement("video");
      const canvas = document.createElement("canvas");
  
      video.preload = "metadata";
      video.src = URL.createObjectURL(file);
  
      video.onloadeddata = () => {
        video.currentTime = 0;
        video.onseeked = () => {
          const context = canvas.getContext("2d");
          if (!context) {
            reject(new Error("Canvas context not available"));
            return;
          }
  
          // Set canvas size to the video frame size
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
  
          // Draw the video frame on the canvas
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
          // Convert the canvas to a Base64 image (JPEG format)
          const base64String = canvas.toDataURL("image/jpeg");
          resolve(base64String); // "data:image/jpeg;base64,..."
        };
      };
  
      video.onerror = () => reject(new Error("Error loading video"));
    });
  }