document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting if validation fails

    const getElement = (name) => document.querySelector(`[name="${name}"]`);
    const getValue = (name) => getElement(name) ? getElement(name).value.trim() : "";

    // Required Fields Validation
    const requiredFields = ["first_name", "surname", "email", "password", "confirmPassword"];
    for (let field of requiredFields) {
        if (!getValue(field)) {
            showAlert(`${field} cannot be empty!`);
            return; // Stop execution if any field is empty
        }
    }

    // ID Number Validation
    if (!/^\d+$/.test(getValue("idNumber"))) {
        showAlert("ID Number must contain only numbers!");
        return;
    }

    // Email Validation
    if (!/\S+@\S+\.\S+/.test(getValue("email"))) {
        showAlert("Invalid email format!");
        return;
    }

    // Password Match Validation
    if (getValue("password") !== getValue("confirmPassword")) {
        showAlert("Passwords do not match!");
        return;
    }

    // Proceed with form submission if validation passes
    fetch("/register", {
        method: "POST",
        body: new FormData(this),
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            showAlert(data.message);
        } else {
            window.location.href = "/login";  // Redirect on success
        }
    })
    .catch(error => console.error("Error:", error));

    // Function to show an alert without "OK" button
    function showAlert(message) {
        let alertDiv = document.createElement("div");
        alertDiv.textContent = message;
        alertDiv.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: red;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            z-index: 1000;
        `;
        document.body.appendChild(alertDiv);

        // Remove alert after 3 seconds
        setTimeout(() => alertDiv.remove(), 3000);
    }
});
