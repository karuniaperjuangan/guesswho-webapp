export default function base64ToFile(base64String: string, fileName: string): File {
    // Extract the base64 data part
    const arr = base64String.split(',');
    const mime = arr[0].match(/:(.*?);/)?.[1] || '';
    const bstr = atob(arr[1]); // decode base64
    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    // Convert the binary string to a byte array
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }

    // Create the file
    return new File([u8arr], fileName, { type: mime });
}