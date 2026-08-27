const dropZone = document.getElementById("drop-zone");
const imageInput = document.getElementById("image-input");
const browseButton = document.getElementById("browse-button");

const previewContainer =
    document.getElementById("preview-container");

const previewImage =
    document.getElementById("preview-image");

const removeButton =
    document.getElementById("remove-button");

const analyzeButton =
    document.getElementById("analyze-button");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const errorBox =
    document.getElementById("error-box");


let selectedFile = null;


// ============================================================
// BROWSE
// ============================================================

browseButton.addEventListener(
    "click",
    function (event) {

        event.stopPropagation();

        imageInput.click();

    }
);


// ============================================================
// DROP ZONE CLICK
// ============================================================

dropZone.addEventListener(
    "click",
    function () {

        imageInput.click();

    }
);


// ============================================================
// FILE SELECT
// ============================================================

imageInput.addEventListener(
    "change",
    function () {

        if (this.files.length > 0) {

            handleFile(
                this.files[0]
            );

        }

    }
);


// ============================================================
// DRAG EVENTS
// ============================================================

dropZone.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();

        dropZone.classList.add(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "dragleave",
    function () {

        dropZone.classList.remove(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();

        dropZone.classList.remove(
            "dragover"
        );

        const files =
            event.dataTransfer.files;

        if (files.length > 0) {

            handleFile(files[0]);

        }

    }
);


// ============================================================
// HANDLE FILE
// ============================================================

function handleFile(file) {

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ];

    if (!allowedTypes.includes(file.type)) {

        showError(
            "Please upload a JPG, JPEG, PNG, or WEBP image."
        );

        return;

    }


    selectedFile = file;


    const reader =
        new FileReader();


    reader.onload = function (event) {

        previewImage.src =
            event.target.result;

        dropZone.classList.add(
            "hidden"
        );

        previewContainer.classList.remove(
            "hidden"
        );

        result.classList.add(
            "hidden"
        );

        errorBox.classList.add(
            "hidden"
        );

    };


    reader.readAsDataURL(file);

}


// ============================================================
// REMOVE IMAGE
// ============================================================

removeButton.addEventListener(
    "click",
    function () {

        selectedFile = null;

        imageInput.value = "";

        previewImage.src = "";

        previewContainer.classList.add(
            "hidden"
        );

        dropZone.classList.remove(
            "hidden"
        );

        result.classList.add(
            "hidden"
        );

        errorBox.classList.add(
            "hidden"
        );

    }
);


// ============================================================
// ANALYZE
// ============================================================

analyzeButton.addEventListener(
    "click",
    async function () {

        if (!selectedFile) {

            showError(
                "Please select an image first."
            );

            return;

        }


        const formData =
            new FormData();

        formData.append(
            "image",
            selectedFile
        );


        loading.classList.remove(
            "hidden"
        );

        result.classList.add(
            "hidden"
        );

        errorBox.classList.add(
            "hidden"
        );


        try {

            const response =
                await fetch(
                    "/api/predict",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Prediction failed."
                );

            }


            displayResult(data);


        } catch (error) {

            showError(
                error.message
            );

        } finally {

            loading.classList.add(
                "hidden"
            );

        }

    }
);


// ============================================================
// DISPLAY RESULT
// ============================================================

function displayResult(data) {

    const country =
        data.country || {};

    const confidence =
        Number(
            data.confidence_percent || 0
        );


    document.getElementById(
        "country-name"
    ).textContent =
        country.country_name ||
        "Unknown";


    document.getElementById(
        "official-name"
    ).textContent =
        country.official_name ||
        "";


    document.getElementById(
        "confidence"
    ).textContent =
        confidence.toFixed(2) + "%";


    setTimeout(
        function () {

            document.getElementById(
                "confidence-bar"
            ).style.width =
                Math.min(
                    confidence,
                    100
                ) + "%";

        },
        100
    );


    document.getElementById(
        "capital"
    ).textContent =
        country.capital ||
        "N/A";


    document.getElementById(
        "continent"
    ).textContent =
        country.continent ||
        "N/A";


    document.getElementById(
        "region"
    ).textContent =
        country.region ||
        "N/A";


    document.getElementById(
        "currency"
    ).textContent =
        country.currency ||
        "N/A";


    document.getElementById(
        "languages"
    ).textContent =
        country.languages ||
        "N/A";


    document.getElementById(
        "independence"
    ).textContent =
        country.independence_date ||
        "N/A";


    document.getElementById(
        "flag-description"
    ).textContent =
        country.flag_description ||
        "No description available.";


    document.getElementById(
        "history"
    ).textContent =
        country.short_history ||
        "No history available.";


    document.getElementById(
        "interesting-fact"
    ).textContent =
        country.interesting_fact ||
        "No interesting fact available.";


    const neighbors =
        country.neighbors || "";


    document.getElementById(
        "neighbors"
    ).textContent =
        neighbors ||
        "No neighboring countries available.";


    // ========================================================
    // TOP 5
    // ========================================================

    const topContainer =
        document.getElementById(
            "top-predictions"
        );


    topContainer.innerHTML = "";


    const predictions =
        data.top_predictions || [];


    predictions.forEach(
        function (item, index) {

            const name =
                item.country_name ||
                "Unknown";


            const score =
                Number(
                    item.confidence_percent || 0
                );


            const div =
                document.createElement(
                    "div"
                );


            div.className =
                "top-item";


            div.innerHTML = `

                <div class="top-row">

                    <span class="top-name">
                        ${index + 1}. ${escapeHtml(name)}
                    </span>

                    <span class="top-score">
                        ${score.toFixed(2)}%
                    </span>

                </div>

                <div class="top-track">

                    <div
                        class="top-fill"
                        style="width:${Math.min(score, 100)}%"
                    >
                    </div>

                </div>

            `;


            topContainer.appendChild(
                div
            );

        }
    );


    result.classList.remove(
        "hidden"
    );


    result.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


// ============================================================
// ERROR
// ============================================================

function showError(message) {

    errorBox.textContent =
        "⚠️ " + message;

    errorBox.classList.remove(
        "hidden"
    );

}


// ============================================================
// BASIC HTML ESCAPE
// ============================================================

function escapeHtml(value) {

    return String(value)

        .replaceAll("&", "&amp;")

        .replaceAll("<", "&lt;")

        .replaceAll(">", "&gt;")

        .replaceAll('"', "&quot;")

        .replaceAll("'", "&#039;");

}