const form = document.querySelector("#convert-form");
const input = document.querySelector("#file-input");
const dropZone = document.querySelector("#drop-zone");
const fileList = document.querySelector("#file-list");
const emptyState = document.querySelector("#empty-state");
const statusLine = document.querySelector("#status");
const convertButton = document.querySelector("#convert-button");
const clearButton = document.querySelector("#clear-button");
const fileCount = document.querySelector("#file-count");

let selectedFiles = [];
let detectionAbort = null;

const setStatus = (message) => {
  statusLine.textContent = message;
};

const setFiles = (files) => {
  selectedFiles = Array.from(files);
  renderFiles(selectedFiles.map((file) => ({ name: file.name })));
  detectFiles();
};

const renderFiles = (files) => {
  fileList.innerHTML = "";
  emptyState.hidden = files.length > 0;
  convertButton.disabled = files.length === 0;
  clearButton.disabled = files.length === 0;
  fileCount.textContent = `${files.length} selected`;

  files.forEach((file) => {
    const row = document.createElement("li");
    row.className = "file-row";

    const name = document.createElement("span");
    name.className = "name";
    name.textContent = file.name;
    row.append(name);

    const meta = document.createElement("span");
    meta.className = "meta";
    [file.extension, file.mimetype, file.charset].filter(Boolean).forEach((value) => {
      const chip = document.createElement("span");
      chip.className = "chip";
      chip.textContent = value;
      meta.append(chip);
    });
    if (!meta.children.length) {
      const chip = document.createElement("span");
      chip.className = "chip";
      chip.textContent = "detecting";
      meta.append(chip);
    }
    row.append(meta);
    fileList.append(row);
  });
};

const buildFormData = () => {
  const data = new FormData();
  selectedFiles.forEach((file) => data.append("files", file));
  return data;
};

const detectFiles = async () => {
  if (detectionAbort) {
    detectionAbort.abort();
  }
  if (!selectedFiles.length) {
    setStatus("");
    return;
  }

  detectionAbort = new AbortController();
  setStatus("Detecting formats...");
  try {
    const response = await fetch("/api/detect", {
      method: "POST",
      body: buildFormData(),
      signal: detectionAbort.signal,
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Format detection failed.");
    }
    renderFiles(payload.files);
    setStatus(`${payload.files.length} file${payload.files.length === 1 ? "" : "s"} ready.`);
  } catch (error) {
    if (error.name !== "AbortError") {
      setStatus(error.message);
    }
  }
};

const downloadBlob = async (response) => {
  const disposition = response.headers.get("content-disposition") || "";
  const match = disposition.match(/filename="?([^"]+)"?/i);
  const filename = match ? match[1] : "markitdown-output.md";
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
};

input.addEventListener("change", () => setFiles(input.files));

["dragenter", "dragover"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.add("is-dragging");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.remove("is-dragging");
  });
});

dropZone.addEventListener("drop", (event) => {
  setFiles(event.dataTransfer.files);
});

clearButton.addEventListener("click", () => {
  input.value = "";
  selectedFiles = [];
  renderFiles([]);
  setStatus("");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!selectedFiles.length) {
    return;
  }

  convertButton.disabled = true;
  setStatus("Converting locally...");

  const data = buildFormData();
  const formValues = new FormData(form);
  data.append("mode", formValues.get("mode"));
  data.append("collection_name", formValues.get("collection_name"));

  try {
    const response = await fetch("/api/convert", {
      method: "POST",
      body: data,
    });
    if (!response.ok) {
      const payload = await response.json();
      throw new Error(payload.error || "Conversion failed.");
    }
    await downloadBlob(response);
    setStatus("Conversion complete. Your PageMint output is ready.");
  } catch (error) {
    setStatus(error.message);
  } finally {
    convertButton.disabled = selectedFiles.length === 0;
  }
});
