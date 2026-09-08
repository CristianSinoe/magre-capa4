const form = document.getElementById("generation-form");
const statusEl = document.getElementById("status");
const resultPanel = document.getElementById("result-panel");
const parametersOutput = document.getElementById("parameters-output");
const metadataOutput = document.getElementById("metadata-output");
const audioPlayer = document.getElementById("audio-player");
const downloadLink = document.getElementById("download-link");
const submitButton = document.getElementById("submit-button");

function parseOptionalInteger(value) {
  if (!value || value.trim() === "") {
    return null;
  }
  return Number.parseInt(value, 10);
}

function buildPayload(formData) {
  return {
    session_name: formData.get("session_name") || null,
    duration_seconds: Number.parseInt(formData.get("duration_seconds"), 10),
    seed: parseOptionalInteger(formData.get("seed")),
    current_state: {
      arousal: Number.parseFloat(formData.get("current_arousal")),
      valence: Number.parseFloat(formData.get("current_valence")),
      stress: Number.parseFloat(formData.get("current_stress")),
      engagement: Number.parseFloat(formData.get("current_engagement")),
    },
    target_state: {
      arousal: Number.parseFloat(formData.get("target_arousal")),
      valence: Number.parseFloat(formData.get("target_valence")),
      stress: Number.parseFloat(formData.get("target_stress")),
      engagement: Number.parseFloat(formData.get("target_engagement")),
    },
  };
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusEl.textContent = "Generando intervención musical...";
  submitButton.disabled = true;

  try {
    const payload = buildPayload(new FormData(form));
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "No fue posible generar el audio.");
    }

    parametersOutput.textContent = JSON.stringify(data.metadata.safe_parameters, null, 2);
    metadataOutput.textContent = JSON.stringify(data.metadata, null, 2);
    audioPlayer.src = data.audio_url;
    downloadLink.href = data.audio_url;
    resultPanel.classList.remove("hidden");
    statusEl.textContent = `Sesión ${data.session_id} generada correctamente.`;
  } catch (error) {
    statusEl.textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
});
