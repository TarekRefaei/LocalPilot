export function renderChat(container: HTMLElement) {
  const progress = document.createElement('progress');
  progress.max = 100;
  container.appendChild(progress);

  const input = document.createElement("input");
  const output = document.createElement("div");

  input.placeholder = "Ask about your project...";

  container.appendChild(output);
  container.appendChild(input);

  input.addEventListener("keydown", async (e: KeyboardEvent) => {
    if (e.key !== "Enter") return;
    const target = e.target as HTMLInputElement;
    const message = target.value;
    target.value = "";

    output.innerHTML += `<div><b>You:</b> ${message}</div>`;

    // ChatService injected later
  });
}
