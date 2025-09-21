// Redirect Signup button (from index.html)
const signupBtn = document.querySelector('.signup-btn');

if (signupBtn) {
  signupBtn.addEventListener('click', () => {
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;

    firebase.auth().createUserWithEmailAndPassword(email, password)
      .then((userCredential) => {
        alert("Account created successfully!");
        window.location.href = "index.html"; // Redirect to login
      })
      .catch((error) => {
        alert(error.message);
      });
  });
}


// Signup form validation (from signup.html)
const signupForm = document.querySelector('.signup-box');
if (signupForm) {
  const inputs = signupForm.querySelectorAll('input');
  const createBtn = signupForm.querySelector('.signup-btn');

  createBtn.addEventListener('click', () => {
    const name = inputs[0].value.trim();
    const email = inputs[1].value.trim();
    const pass = inputs[2].value;
    const confirm = inputs[3].value;

    if (!name || !email || !pass || !confirm) {
      alert('Please fill all fields');
      return;
    }

    if (pass !== confirm) {
      alert('Passwords do not match');
      return;
    }

    alert('Account created successfully!');
    // Redirect to dashboard or next page here
  });
}
const createBtn = document.querySelector('.signup-btn');

if (createBtn) {
  createBtn.addEventListener('click', () => {
    const inputs = document.querySelectorAll('.signup-box input');
    const artisanType = document.querySelector('.signup-box select');

    const name = inputs[0].value.trim();
    const email = inputs[1].value.trim();
    const password = inputs[2].value;
    const confirmPassword = inputs[3].value;
    const artisan = artisanType.value;

    if (!name || !email || !password || !confirmPassword || artisan === "Select Artisan Type") {
      alert("Please fill all fields correctly.");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    alert("Account created successfully!");
    // You can redirect to dashboard here
    // window.location.href = 'dashboard.html';
  });
}
const loginBtn = document.getElementById('login-button');

if (loginBtn) {
  loginBtn.addEventListener('click', () => {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;

    // Get Firebase Auth instance
    const auth = firebase.auth();

    auth.signInWithEmailAndPassword(email, password)
      .then((userCredential) => {
        alert("Login successful!");
        window.location.href = "dashboard.html";
      })
      .catch((error) => {
        alert("Login failed: " + error.message);
      });
  });
}


