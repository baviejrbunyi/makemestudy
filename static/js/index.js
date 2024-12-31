document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-input");
    const filePlaceholder = document.getElementById("file-placeholder");
    const errorMessage = document.getElementById("error-message");
    const uploadImage = document.getElementById("upload-image");
    const studyPlanForm = document.getElementById("study-plan-form");

    // Handle file drop
    filePlaceholder.addEventListener("dragover", (event) => {
        event.preventDefault();
        filePlaceholder.classList.add("drag-over");
    });

    filePlaceholder.addEventListener("dragleave", () => {
        filePlaceholder.classList.remove("drag-over");
    });

    filePlaceholder.addEventListener("drop", (event) => {
        event.preventDefault();
        filePlaceholder.classList.remove("drag-over");
        handleFileUpload(event.dataTransfer.files[0]);
    });

    // Handle file input click
    uploadImage.addEventListener("click", () => {
        fileInput.click();
    });

    // Handle file input change (file picker)
    fileInput.addEventListener("change", (event) => {
        handleFileUpload(event.target.files[0]);
    });

    // Function to handle file upload
    function handleFileUpload(file) {
        const validTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
        if (validTypes.includes(file.type)) {
            const fileName = file.name;
            filePlaceholder.innerHTML = `<span>${fileName}</span><button type="button" id="remove-file" class="remove-file">X</button>`;
            document.getElementById("remove-file").addEventListener("click", () => {
                fileInput.value = "";
                filePlaceholder.innerHTML = '<div class="file-placeholder-child"></div><div class="upload-image"><div class="choose-a-file">Choose a file or Drag it here</div><img class="upload-image-child" alt="" src="../assets/Group 3.svg"></div>';
            });
            errorMessage.style.display = "none";
        } else {
            errorMessage.style.display = "block";
            setTimeout(() => {
                errorMessage.style.display = "none";
            }, 2000);
        }
    }

    // Handle form submission (validate)
    studyPlanForm.addEventListener("submit", (event) => {
        if (!fileInput.files[0]) {
            alert("Please upload a file.");
            event.preventDefault();
        }
    });
});
