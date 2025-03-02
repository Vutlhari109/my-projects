<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user_id = $_POST['user_id']; // Get user ID from session or form
    $institutions = isset($_POST['institutions']) ? $_POST['institutions'] : [];

    if (!empty($institutions)) {
        $selected_institutions = implode(",", $institutions); // Convert array to comma-separated string
    } else {
        $selected_institutions = "";
    }

    // Database Connection (Replace with your credentials)
    $conn = new mysqli("localhost", "root", "", "varsity_applicants");

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Update user record with selected institutions
    $stmt = $conn->prepare("UPDATE users SET selected_institutions = ? WHERE id = ?");
    $stmt->bind_param("si", $selected_institutions, $user_id);

    if ($stmt->execute()) {
        echo "Institutions updated successfully!";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();
}
?>
<?php
// Database connection
$conn = new mysqli("localhost", "root", "", "varsity_applicants");

// Fetch user institutions
$user_id = 1; // Replace with dynamic user ID
$result = $conn->query("SELECT selected_institutions FROM users WHERE id = $user_id");

$row = $result->fetch_assoc();
$institutions = explode(",", $row['selected_institutions']); // Convert back to array

echo "Selected Institutions: " . implode(", ", $institutions);
?>

