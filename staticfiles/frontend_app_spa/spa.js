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

// Load alumni list
async function loadAlumni() {
  alumniList.innerHTML = "<p>Mengambil data alumni...</p>";
  try {
    const res = await fetch("/api/alumni/", {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    if (!res.ok) throw new Error("Gagal mengambil data alumni.");
    const alumni = await res.json();
    let html = alumni.map((alum) => renderAlumniCard(alum)).join("");
    if (isAdmin) {
      html = `<div class='d-flex justify-content-end mb-2'>
        <button class='btn btn-success' onclick='showAlumniForm()'>Tambah Alumni</button>
      </div>` + html;
    }
    alumniList.innerHTML = html;
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

// Inisialisasi
showLogin();
