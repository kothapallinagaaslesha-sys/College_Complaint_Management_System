// ================================
// College Complaint Management System
// script.js
// ================================

document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // Complaint Form Validation
    // -----------------------------
    const complaintForm = document.getElementById("complaintForm");

    if (complaintForm) {
        complaintForm.addEventListener("submit", function (e) {

            const title = document.getElementById("title").value.trim();
            const category = document.getElementById("category").value;
            const description = document.getElementById("description").value.trim();

            if (title === "" || category === "" || description === "") {
                e.preventDefault();
                alert("Please fill all complaint details.");
                return;
            }

            if (description.length < 20) {
                e.preventDefault();
                alert("Complaint description must contain at least 20 characters.");
                return;
            }

            alert("Complaint submitted successfully!");
        });
    }

    // -----------------------------
    // Register Form Validation
    // -----------------------------
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {

            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirmPassword").value;

            if (name === "" || email === "" || password === "" || confirmPassword === "") {
                e.preventDefault();
                alert("Please fill all fields.");
                return;
            }

            if (password.length < 6) {
                e.preventDefault();
                alert("Password should be at least 6 characters.");
                return;
            }

            if (password !== confirmPassword) {
                e.preventDefault();
                alert("Passwords do not match.");
            }
        });
    }

    // -----------------------------
    // Login Form Validation
    // -----------------------------
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            if (email === "" || password === "") {
                e.preventDefault();
                alert("Enter Email and Password.");
            }
        });
    }

    // -----------------------------
    // Password Show / Hide
    // -----------------------------
    const togglePassword = document.getElementById("togglePassword");

    if (togglePassword) {
        togglePassword.addEventListener("click", function () {

            const passwordInput = document.getElementById("password");

            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                this.textContent = "Hide";
            } else {
                passwordInput.type = "password";
                this.textContent = "Show";
            }
        });
    }

    // -----------------------------
    // Description Character Counter
    // -----------------------------
    const description = document.getElementById("description");
    const counter = document.getElementById("charCount");

    if (description && counter) {

        counter.textContent = "0 / 500";

        description.addEventListener("input", function () {
            counter.textContent = `${this.value.length} / 500`;
        });
    }

    // -----------------------------
    // Auto Close Success Alert
    // -----------------------------
    const successAlert = document.querySelector(".success-alert");

    if (successAlert) {
        setTimeout(() => {
            successAlert.style.display = "none";
        }, 3000);
    }

});