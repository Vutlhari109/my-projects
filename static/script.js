document.getElementById('registerForm').addEventListener('submit', function() {
    const getElement = (name) => document.querySelector(`[name="${name}"]`);
    const getValue = (name) => getElement(name) ? getElement(name).value.trim() : "";

    // Required Fields Validation
    const requiredFields = ["first_name", "surname", "email", "password", "confirmPassword"];
    for (let field of requiredFields) {
        if (!getValue(field)) {
            window.alert(`${field} cannot be empty!`);
        }
    }

    // ID Number Validation
    if (!/^\d+$/.test(getValue("idNumber"))) {
        window.alert("ID Number must contain only numbers!");
    }

    // Email Validation
    if (!/\S+@\S+\.\S+/.test(getValue("email"))) {
        window.alert("Invalid email format!");
    }

    // Password Match Validation
    if (getValue("password") !== getValue("confirmPassword")) {
        window.alert("Passwords do not match!");
    }

    // ✅ JS validation is for user feedback, but the form still submits to Flask
});
