const form = document.querySelector("#demo-form");
const input = document.querySelector("#url");
const status = document.querySelector("#status");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const value = input.value.trim();

  if (!value) {
    status.textContent = "Give me a signal first. Paste a video URL.";
    return;
  }

  status.textContent =
    "Signal received. The public interface is alive; multimodal analysis gets wired in next.";
});
