const state = { userId: localStorage.getItem("notes-user-id"), page: 1, pageSize: 10, total: 0 };
const $ = (id) => document.getElementById(id);

function showMessage(text, error = false) {
  $("message").textContent = text;
  $("message").style.color = error ? "#bd4f36" : "#6c776f";
}

async function request(url, options = {}) {
  const response = await fetch(url, { headers: { "Content-Type": "application/json" }, ...options });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || error.detail || `Ошибка ${response.status}`);
  }
  return response.status === 204 ? null : response.json();
}

function renderUser() {
  $("user-state").textContent = state.userId
    ? `Активный ID: ${state.userId}`
    : "Пользователь не выбран";
}

async function loadNotes() {
  const filter = $("filter").value;
  const params = new URLSearchParams({ skip: String((state.page - 1) * state.pageSize), limit: String(state.pageSize) });
  if (filter !== "") params.set("status_filter", filter);
  try {
    const data = await request(`/notes?${params}`);
    state.total = data.total;
    const totalPages = Math.max(1, Math.ceil(state.total / state.pageSize));
    if (state.page > totalPages) {
      state.page = totalPages;
      return loadNotes();
    }
    $("count").textContent = data.total;
    $("page-info").textContent = `Страница ${state.page} из ${totalPages}`;
    $("previous-page").disabled = state.page === 1;
    $("next-page").disabled = state.page === totalPages;
    $("notes").innerHTML = data.items.length ? data.items.map((note) => `
      <article class="note ${note.status ? "done" : ""}">
        <div class="note-title">${escapeHtml(note.title)}</div>
        <div class="note-actions">
          <button data-toggle="${note.id}" aria-label="Изменить статус">${note.status ? "Вернуть" : "Готово"}</button>
          <button class="delete" data-delete="${note.id}" aria-label="Удалить заметку">Удалить</button>
        </div>
      </article>`).join("") : '<div class="empty">Пока нет заметок. Добавьте первую выше.</div>';
  } catch (error) { showMessage(error.message, true); }
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character]));
}

$("user-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const user = await request("/users", { method: "POST", body: JSON.stringify({ email: $("email").value, phone: $("phone").value }) });
    state.userId = user.id;
    localStorage.setItem("notes-user-id", user.id);
    renderUser();
    showMessage("Пользователь создан");
  } catch (error) { showMessage(error.message, true); }
});

$("note-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.userId) { showMessage("Сначала создайте пользователя", true); return; }
  try {
    await request("/notes", { method: "POST", body: JSON.stringify({ title: $("title").value, user_id: state.userId }) });
    $("title").value = "";
    showMessage("Заметка добавлена");
    await loadNotes();
  } catch (error) { showMessage(error.message, true); }
});

$("filter").addEventListener("change", loadNotes);
$("previous-page").addEventListener("click", () => {
  if (state.page > 1) {
    state.page -= 1;
    loadNotes();
  }
});
$("next-page").addEventListener("click", () => {
  if (state.page < Math.ceil(state.total / state.pageSize)) {
    state.page += 1;
    loadNotes();
  }
});
$("notes").addEventListener("click", async (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  try {
    if (button.dataset.toggle) {
      await request(`/notes/${button.dataset.toggle}`, { method: "PATCH", body: JSON.stringify({ status: !button.closest(".note").classList.contains("done") }) });
    } else if (button.dataset.delete) {
      await request(`/notes/${button.dataset.delete}`, { method: "DELETE" });
    }
    await loadNotes();
  } catch (error) { showMessage(error.message, true); }
});

renderUser();
loadNotes();