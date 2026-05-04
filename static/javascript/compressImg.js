// Listens for image inputs
// Compresses and swaps img
document.addEventListener("DOMContentLoaded", () => {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach((input) => {
        input.addEventListener("change", async (e) => {
            const file = e.target.files[0]

            if (!file || !file.type.startsWith('image/')) return 

            const compressedFile = await compressImage(file, 0.7);
            const dataTransfer = new DataTransfer();

            dataTransfer.items.add(compressedFile);
            input.files = dataTransfer.files;
        })
    })

})

function compressImage(file, quality = 0.7) {
  return new Promise((resolve) => {
    const reader = new FileReader();

    reader.onload = (event) => {
      const img = new Image();

      img.onload = () => {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");

        // optional: resize if huge
        const maxWidth = 1600;
        const scale = Math.min(1, maxWidth / img.width);

        canvas.width = img.width * scale;
        canvas.height = img.height * scale;

        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        const baseName = file.name.replace(/\.[^/.]+$/, "");
        const newName = `${baseName}.jpg`;

        canvas.toBlob(
          (blob) => {
            const compressedFile = new File(
              [blob],
              newName,
              {
                type: "image/jpeg",
                lastModified: Date.now(),
              }
            );

            resolve(compressedFile);
          },
          "image/jpeg",
          quality
        );
      };

      img.src = event.target.result;
    };

    reader.readAsDataURL(file);
  });
}