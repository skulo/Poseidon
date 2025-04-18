let currentPage = 1;
let maxPage = 1;
const pageSize = 5;

function updatePaginationControls() {
  document.getElementById("page-indicator-bottom").innerText = currentPage;
  document.getElementById("page-indicator-top").innerText = currentPage;

  const disableElement = (element, condition) => {
    element.style.opacity = condition ? "0.5" : "1";
    element.style.pointerEvents = condition ? "none" : "auto";
  };

  disableElement(document.getElementById("prevPageTop"), currentPage <= 1);
  disableElement(
    document.getElementById("nextPageTop"),
    currentPage >= maxPage
  );
  disableElement(document.getElementById("prevPageBottom"), currentPage <= 1);
  disableElement(
    document.getElementById("nextPageBottom"),
    currentPage >= maxPage
  );
}

function nextPage() {
  currentPage++;
  getQuizResults(currentPage);
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    getQuizResults(currentPage);
  }
}

async function getQuizResults(page = 1) {
  const url = `/quiz-all/?page=${page}&page_size=${pageSize}`;
  const response = await fetch(url, {
    method: "GET",
  });

  if (!response.ok) {
    alert("Nem sikerült betölteni a kvízeket.");
    return;
  }

  const quizResults = await response.json();

  maxPage = quizResults.max_page;

  currentPage = page;

  showQuizResult(quizResults.quizzes);
  updatePaginationControls();
}

function showQuizResult(results) {
  const quizzesList = document.getElementById("quizzes-list");
  quizzesList.innerHTML = "";

  results.forEach(async (result) => {
    const card = document.createElement("div");
    card.className = "document-card";

    card.innerHTML = `
      <div class="document-date">${new Date(
        result.created_at
      ).toLocaleDateString()}</div>
      <div class="documents-category">${result.category}</div>
      <div class="document-title">${result.document_name}</div>
      <div class="document-description">${result.total_questions} Kérdés</div>
    `;

    const responsez = await getUserData();
    if (responsez.ok) {
      const user_data = responsez.data;
      const userId = user_data.id;
      const role = user_data.role;

      if (role === "admin" || result.created_by === userId) {
        const deleteButton = document.createElement("button");
        deleteButton.innerText = "Törlés";
        deleteButton.className = "delete-btn";

        deleteButton.onclick = async (e) => {
          const checkQuiz = await fetch(`/api/quiz/${result.quiz_id}`, {
            method: "GET",
          });

          if (!checkQuiz.ok) {
            showAlert("warning", "A kvíz nem elérhető. Frissítsd az oldalt.");
            return;
          }

          const confirmed = confirm(
            "Biztosan törölni szeretnéd a kvízt? A kvízhez tartozó eredmények is törlésre kerülnek."
          );
          if (!confirmed) {
            return;
          }

          e.stopPropagation();
          try {
            const response = await fetch(`/deletequiz/${result.quiz_id}`, {
              method: "DELETE",
              credentials: "include",
            });

            if (response.ok) {
              showAlert("success", "Sikeres törlés!");
              getQuizResults(currentPage);
            } else {
              const errorResponse = await response.json();
              showAlert(
                "danger",
                errorResponse.detail || "Hiba a törlés során."
              );
            }
          } catch (error) {
            showAlert("danger", "Hálózati hiba történt.");
          }
        };

        card.appendChild(deleteButton);
      }
    }

    card.addEventListener("click", async (event) => {
      if (!event.target.classList.contains("delete-btn")) {
        const checkQuiz = await fetch(`/api/quiz/${result.quiz_id}`, {
          method: "GET",
        });

        if (!checkQuiz.ok) {
          showAlert("warning", "A kvíz nem elérhető. Frissítsd az oldalt.");
          return;
        }

        window.location.href = `/quiz/quiz.html?quiz_id=${result.quiz_id}`;
      }
    });

    quizzesList.appendChild(card);
  });
}

window.addEventListener("load", () => {
  getQuizResults();
});

document.addEventListener("DOMContentLoaded", function () {
  const pageNumber = document.getElementById("page-indicator-top");

  function updatePaginationControls(page, maxPage) {
    pageNumber.textContent = page;

    document.getElementById("page-indicator-top").innerText = page;
    document.getElementById("page-indicator-bottom").innerText = page;

    document.getElementById("prevPageTop").disabled = page <= 1;
    document.getElementById("prevPageBottom").disabled = page <= 1;
  }

  document.getElementById("prevPageTop").addEventListener("click", function () {
    if (currentPage > 1) {
      currentPage--;
      getQuizResults(currentPage);
    }
  });

  document.getElementById("nextPageTop").addEventListener("click", function () {
    currentPage++;
    getQuizResults(currentPage);
  });

  document
    .getElementById("prevPageBottom")
    .addEventListener("click", function () {
      if (currentPage > 1) {
        currentPage--;
        getQuizResults(currentPage);
      }
    });

  document
    .getElementById("nextPageBottom")
    .addEventListener("click", function () {
      currentPage++;
      getQuizResults(currentPage);
    });

  updatePaginationControls(1, 10);
});
