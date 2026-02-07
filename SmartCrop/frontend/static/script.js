const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultBox = document.getElementById("result");
const statusText = document.getElementById("statusText");
const confidenceText = document.getElementById("confidenceText");

// -----------------------------
// IMAGE PREVIEW
// -----------------------------
imageInput.addEventListener("change", () => {
  preview.innerHTML = "";

  const file = imageInput.files[0];
  if (!file) return;

  const img = document.createElement("img");
  img.src = URL.createObjectURL(file);
  preview.appendChild(img);
});

// -----------------------------
// ANALYZE BUTTON (REAL BACKEND)
// -----------------------------
analyzeBtn.addEventListener("click", async () => {
  const file = imageInput.files[0];

  if (!file) {
    alert("Please upload a leaf image");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  // UI feedback
  analyzeBtn.innerText = "Analyzing...";
  analyzeBtn.disabled = true;
  resultBox.classList.add("hidden");

  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();
    showResult(data.status, data.confidence);

  } catch (error) {
    console.error(error);
    alert("Could not connect to backend");
  }

  analyzeBtn.innerText = "Analyze Leaf";
  analyzeBtn.disabled = false;
});

// -----------------------------
// DISPLAY RESULT
// -----------------------------
function showResult(status, confidence) {
  resultBox.className = `result ${status}`;
  resultBox.classList.remove("hidden");

  statusText.innerText = status;
  confidenceText.innerText = `Confidence: ${confidence}%`;
}
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");

  if (!form) return;

  form.addEventListener("submit", () => {
    const btn = document.getElementById("analyzeBtn");
    btn.innerText = "Analyzing...";
    btn.disabled = true;
  });
});
