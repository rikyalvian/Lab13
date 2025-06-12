let accessToken = "";
let isAdmin = false;
let currentUser = null;

const loginForm = document.getElementById("login-form");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const loginError = document.getElementById("login-error");

const loginSection = document.getElementById("login-section");
const dataSection = document.getElementById("data-section");
const alumniList = document.getElementById("alumni-list");
const logoutBtn = document.getElementById("logout-btn");

const registerBtn = document.getElementById("register-btn");
const registerSection = document.getElementById("register-section");
const registerForm = document.getElementById("register-form");
const registerError = document.getElementById("register-error");
const registerSuccess = document.getElementById("register-success");

// Login
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  loginError.textContent = "";
  try {
    const res = await fetch("/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: usernameInput.value,
        password: passwordInput.value,
      }),
    });
    if (res.ok) {
      const data = await res.json();
      accessToken = data.access;
      // Ambil info user dari JWT (payload)
      const payload = JSON.parse(atob(data.access.split('.')[1]));
      console.log('JWT payload:', payload); // DEBUG: tampilkan payload JWT
      isAdmin = payload.is_admin || false;
      currentUser = { username: payload.username, is_admin: isAdmin };
      showData();
    } else {
      loginError.textContent = "Login gagal. Coba periksa username dan password.";
    }
  } catch (err) {
    loginError.textContent = "Terjadi kesalahan saat login.";
  }
});

// Logout
logoutBtn.addEventListener("click", () => {
  accessToken = "";
  isAdmin = false;
  currentUser = null;
  showLogin();
});

function showLogin() {
  loginSection.style.display = "block";
  dataSection.style.display = "none";
  registerSection.style.display = "none";
  alumniList.innerHTML = "";
}
function showData() {
  loginSection.style.display = "none";
  dataSection.style.display = "block";
  registerSection.style.display = "none";
  loadAlumni();
}

// State filter
let filterMajor = "";
let filterGraduationYear = "";
let searchKeyword = "";
let sortBy = "";

// Load alumni list with filter/search/sort
async function loadAlumni() {
  alumniList.innerHTML = "<p>Mengambil data alumni...</p>";
  try {
    let url = "/api/alumni/?";
    if (filterMajor) url += `major=${encodeURIComponent(filterMajor)}&`;
    if (filterGraduationYear) url += `graduation_year=${encodeURIComponent(filterGraduationYear)}&`;
    if (searchKeyword) url += `search=${encodeURIComponent(searchKeyword)}&`;
    if (sortBy) url += `ordering=${encodeURIComponent(sortBy)}&`;
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (!res.ok) throw new Error("Gagal mengambil data alumni.");
    const alumni = await res.json();
    let results = alumni.results || alumni;
    let html = results.map((alum) => renderAlumniCard(alum)).join("");
    if (isAdmin) {
      html = `<div class='d-flex justify-content-end mb-2'>
        <button class='btn btn-success' onclick='showAlumniForm()'>Tambah Alumni</button>
      </div>` + html;
    }
    alumniList.innerHTML = `<div class='row g-4'>${html}</div>`;
    // Pagination
    alumniList.innerHTML += renderPagination(alumni);
    // Pagination events
    if (alumni.previous) document.getElementById('prev-page').onclick = (e) => { e.preventDefault(); loadAlumniPage(alumni.previous); };
    if (alumni.next) document.getElementById('next-page').onclick = (e) => { e.preventDefault(); loadAlumniPage(alumni.next); };
    // Numbered page events
    document.querySelectorAll('.pagination .page-link[data-page]').forEach(link => {
      link.onclick = (e) => {
        e.preventDefault();
        let page = link.getAttribute('data-page');
        loadAlumniPage(`/api/alumni/?page=${page}`);
      };
    });
  } catch (err) {
    alumniList.innerHTML = "<p class='text-danger'>Gagal memuat data alumni.</p>";
  }
}

async function loadAlumniPage(url) {
  alumniList.innerHTML = "<p>Mengambil data alumni...</p>";
  try {
    const res = await fetch(url, { headers: { Authorization: `Bearer ${accessToken}` } });
    if (!res.ok) throw new Error("Gagal mengambil data alumni.");
    const alumni = await res.json();
    let results = alumni.results || alumni;
    let html = results.map((alum) => renderAlumniCard(alum)).join("");
    if (isAdmin) {
      html = `<div class='d-flex justify-content-end mb-2'>
        <button class='btn btn-success' onclick='showAlumniForm()'>Tambah Alumni</button>
      </div>` + html;
    }
    alumniList.innerHTML = `<div class='row g-4'>${html}</div>`;
    alumniList.innerHTML += renderPagination(alumni);
    // Pagination events
    if (alumni.previous) document.getElementById('prev-page').onclick = (e) => { e.preventDefault(); loadAlumniPage(alumni.previous); };
    if (alumni.next) document.getElementById('next-page').onclick = (e) => { e.preventDefault(); loadAlumniPage(alumni.next); };
    document.querySelectorAll('.pagination .page-link[data-page]').forEach(link => {
      link.onclick = (e) => {
        e.preventDefault();
        let page = link.getAttribute('data-page');
        loadAlumniPage(`/api/alumni/?page=${page}`);
      };
    });
  } catch (err) {
    alumniList.innerHTML = "<p class='text-danger'>Gagal memuat data alumni.</p>";
  }
}

// Render alumni card
function renderAlumniCard(alum) {
  let btns = "";
  if (isAdmin) {
    btns = `
      <div class='mt-2'>
        <button class='btn btn-warning btn-sm me-2' onclick='editAlumni(${alum.id})'>Edit</button>
        <button class='btn btn-danger btn-sm' onclick='deleteAlumni(${alum.id})'>Delete</button>
      </div>
    `;
  }
  return `
    <div class="card mb-2">
      <div class="card-body">
        <h5>${alum.name}</h5>
        <p>Tahun Lulus: ${alum.graduation_year}</p>
        <p>Jurusan: ${alum.major || "-"}</p>
        ${btns}
      </div>
    </div>
  `;
}

// Pagination rendering
function renderPagination(alumni) {
  if (!(alumni.count && (alumni.next || alumni.previous))) return '';
  let currentPage = 1;
  let totalPages = 1;
  let nextUrl = alumni.next;
  let prevUrl = alumni.previous;
  // Extract page info from next/prev URLs if available
  const getPageNum = (url) => {
    if (!url) return null;
    const match = url.match(/[?&]page=(\d+)/);
    return match ? parseInt(match[1]) : null;
  };
  if (alumni.next) currentPage = getPageNum(alumni.next) - 1;
  else if (alumni.previous) currentPage = getPageNum(alumni.previous) + 1;
  if (alumni.count && alumni.results) {
    totalPages = Math.ceil(alumni.count / alumni.results.length);
  }
  let pagHtml = '<nav><ul class="pagination justify-content-center flex-wrap pagination-lg">';
  if (prevUrl) pagHtml += `<li class='page-item'><a class='page-link' href='#' id='prev-page'>Sebelumnya</a></li>`;
  // Numbered pages
  for (let i = 1; i <= totalPages; i++) {
    pagHtml += `<li class='page-item${i === currentPage ? ' active' : ''}'><a class='page-link' href='#' data-page='${i}'>${i}</a></li>`;
  }
  if (nextUrl) pagHtml += `<li class='page-item'><a class='page-link' href='#' id='next-page'>Berikutnya</a></li>`;
  pagHtml += '</ul></nav>';
  return pagHtml;
}

// Show alumni form (admin only)
window.showAlumniForm = function() {
  alumniList.innerHTML = `
    <div class='card p-3'>
      <h5>Tambah Alumni</h5>
      <form id='alumni-form'>
        <input class='form-control mb-2' name='name' placeholder='Nama' required />
        <input class='form-control mb-2' name='email' placeholder='Email' type='email' required />
        <input class='form-control mb-2' name='graduation_year' placeholder='Tahun Lulus' type='number' required />
        <input class='form-control mb-2' name='major' placeholder='Jurusan' />
        <input class='form-control mb-2' name='job_position' placeholder='Pekerjaan' />
        <input class='form-control mb-2' name='company' placeholder='Perusahaan' />
        <input class='form-control mb-2' name='phone_number' placeholder='No. HP' />
        <input class='form-control mb-2' name='linkedin' placeholder='LinkedIn' type='url' />
        <div class='form-check mb-2'>
          <input class='form-check-input' type='checkbox' name='status_kerja' id='status_kerja'>
          <label class='form-check-label' for='status_kerja'>Sudah Bekerja</label>
        </div>
        <button class='btn btn-success' type='submit'>Simpan</button>
        <button class='btn btn-secondary ms-2' type='button' onclick='loadAlumni()'>Batal</button>
      </form>
      <div id='alumni-form-error' class='text-danger mt-2'></div>
    </div>
  `;
  document.getElementById('alumni-form').onsubmit = async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = {
      name: form.name.value,
      email: form.email.value,
      graduation_year: form.graduation_year.value,
      major: form.major.value,
      job_position: form.job_position.value,
      company: form.company.value,
      phone_number: form.phone_number.value,
      linkedin: form.linkedin.value,
      status_kerja: form.status_kerja.checked
    };
    try {
      const res = await fetch('/api/alumni/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`
        },
        body: JSON.stringify(data)
      });
      if (res.ok) {
        loadAlumni();
      } else {
        document.getElementById('alumni-form-error').textContent = 'Gagal menambah alumni.';
      }
    } catch {
      document.getElementById('alumni-form-error').textContent = 'Gagal menambah alumni.';
    }
  };
};

// Edit alumni (admin only)
window.editAlumni = function(id) {
  // Ambil data alumni lalu tampilkan form edit
  fetch(`/api/alumni/${id}/`, {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
    .then(res => res.json())
    .then(alum => {
      alumniList.innerHTML = `
        <div class='card p-3'>
          <h5>Edit Alumni</h5>
          <form id='alumni-edit-form'>
            <input class='form-control mb-2' name='name' value='${alum.name || ''}' placeholder='Nama' required />
            <input class='form-control mb-2' name='email' value='${alum.email || ''}' placeholder='Email' type='email' required />
            <input class='form-control mb-2' name='graduation_year' value='${alum.graduation_year || ''}' placeholder='Tahun Lulus' type='number' required />
            <input class='form-control mb-2' name='major' value='${alum.major || ''}' placeholder='Jurusan' />
            <input class='form-control mb-2' name='job_position' value='${alum.job_position || ''}' placeholder='Pekerjaan' />
            <input class='form-control mb-2' name='company' value='${alum.company || ''}' placeholder='Perusahaan' />
            <input class='form-control mb-2' name='phone_number' value='${alum.phone_number || ''}' placeholder='No. HP' />
            <input class='form-control mb-2' name='linkedin' value='${alum.linkedin || ''}' placeholder='LinkedIn' type='url' />
            <div class='form-check mb-2'>
              <input class='form-check-input' type='checkbox' name='status_kerja' id='edit_status_kerja' ${alum.status_kerja ? 'checked' : ''}>
              <label class='form-check-label' for='edit_status_kerja'>Sudah Bekerja</label>
            </div>
            <button class='btn btn-warning' type='submit'>Update</button>
            <button class='btn btn-secondary ms-2' type='button' onclick='loadAlumni()'>Batal</button>
          </form>
          <div id='alumni-edit-error' class='text-danger mt-2'></div>
        </div>
      `;
      document.getElementById('alumni-edit-form').onsubmit = async function(e) {
        e.preventDefault();
        const form = e.target;
        const data = {
          name: form.name.value,
          email: form.email.value,
          graduation_year: form.graduation_year.value,
          major: form.major.value,
          job_position: form.job_position.value,
          company: form.company.value,
          phone_number: form.phone_number.value,
          linkedin: form.linkedin.value,
          status_kerja: form.status_kerja.checked
        };
        try {
          const res = await fetch(`/api/alumni/${id}/`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${accessToken}`
            },
            body: JSON.stringify(data)
          });
          if (res.ok) {
            loadAlumni();
          } else {
            // Show backend error message if available
            let msg = 'Gagal update alumni.';
            try {
              const err = await res.json();
              msg += ' ' + JSON.stringify(err);
            } catch {}
            document.getElementById('alumni-edit-error').textContent = msg;
          }
        } catch {
          document.getElementById('alumni-edit-error').textContent = 'Gagal update alumni.';
        }
      };
    });
};

// Delete alumni (admin only)
window.deleteAlumni = function(id) {
  if (!confirm('Yakin ingin menghapus alumni ini?')) return;
  fetch(`/api/alumni/${id}/`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${accessToken}` }
  })
    .then(res => {
      if (res.ok) loadAlumni();
      else alert('Gagal menghapus alumni.');
    });
};

// Register
function showRegister() {
  loginSection.style.display = "none";
  dataSection.style.display = "none";
  registerSection.style.display = "block";
}

if (registerBtn) {
  registerBtn.addEventListener('click', showRegister);
}
if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    registerError.textContent = "";
    registerSuccess.textContent = "";
    const data = {
      username: document.getElementById('reg-username').value,
      password: document.getElementById('reg-password').value,
      name: document.getElementById('reg-name').value,
      email: document.getElementById('reg-email').value,
      graduation_year: parseInt(document.getElementById('reg-graduation_year').value),
      major: document.getElementById('reg-major').value,
      job_position: document.getElementById('reg-job_position').value,
      company: document.getElementById('reg-company').value,
      phone_number: document.getElementById('reg-phone_number').value,
      linkedin: document.getElementById('reg-linkedin').value,
      status_kerja: document.getElementById('reg-status_kerja').checked ? true : false
    };
    try {
      const res = await fetch('/auth/api/register-user-alumni/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (res.ok) {
        registerSuccess.textContent = 'Registrasi berhasil! Silakan login.';
        setTimeout(showLogin, 1500);
      } else {
        const errData = await res.json();
        registerError.textContent = 'Registrasi gagal: ' + JSON.stringify(errData);
      }
    } catch (err) {
      registerError.textContent = 'Registrasi gagal: ' + err;
    }
  });
}

// Filter/search/sort form event
const filterForm = document.getElementById('alumni-filter-form');
if (filterForm) {
  filterForm.onsubmit = function(e) {
    e.preventDefault();
    filterMajor = document.getElementById('filter-major').value;
    filterGraduationYear = document.getElementById('filter-graduation-year').value;
    searchKeyword = document.getElementById('search-keyword').value;
    sortBy = document.getElementById('sort-by').value;
    loadAlumni();
  };
  document.getElementById('reset-filter').onclick = function() {
    filterMajor = "";
    filterGraduationYear = "";
    searchKeyword = "";
    sortBy = "";
    document.getElementById('filter-major').value = "";
    document.getElementById('filter-graduation-year').value = "";
    document.getElementById('search-keyword').value = "";
    document.getElementById('sort-by').value = "";
    loadAlumni();
  };
}

// Inisialisasi
showLogin();
