const tasks = [...document.querySelectorAll('[data-task]')];
const saved = JSON.parse(localStorage.getItem('studyflow-tasks') || '{}');

tasks.forEach((task) => {
  task.checked = Boolean(saved[task.dataset.task]);
  task.addEventListener('change', updateProgress);
});

function updateProgress() {
  const state = Object.fromEntries(tasks.map((task) => [task.dataset.task, task.checked]));
  localStorage.setItem('studyflow-tasks', JSON.stringify(state));

  const done = tasks.filter((task) => task.checked).length;
  const percent = Math.round((done / tasks.length) * 100);
  document.querySelector('#doneCount').textContent = String(done).padStart(2, '0');
  document.querySelector('#ringPercent').textContent = `${percent}%`;
  document.querySelector('.focus-ring').style.setProperty('--progress', `${percent}%`);
  document.querySelector('#totalProgress').style.width = `${percent}%`;
  document.querySelector('#progressLabel').textContent = `${done}/${tasks.length} nhiệm vụ hoàn thành`;
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.14 });

document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
updateProgress();
