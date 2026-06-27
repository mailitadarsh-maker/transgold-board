<?php
require_once __DIR__ . '/db.php';
cors();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  http_response_code(405);
  echo json_encode(['error' => 'Method not allowed']);
  exit;
}

$data = json_decode(file_get_contents('php://input'), true);

$name  = trim($data['name']  ?? '');
$email = trim($data['email'] ?? '');
$phone = trim($data['phone'] ?? '');
$pass  = $data['password']   ?? '';

// Validate
if (!$name || !$email || !$pass) {
  http_response_code(400);
  echo json_encode(['error' => 'Name, email and password are required']);
  exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
  http_response_code(400);
  echo json_encode(['error' => 'Invalid email address']);
  exit;
}

if (strlen($pass) < 6) {
  http_response_code(400);
  echo json_encode(['error' => 'Password must be at least 6 characters']);
  exit;
}

$db = getDB();

// Check existing
$stmt = $db->prepare('SELECT id FROM customers WHERE email = ?');
$stmt->execute([$email]);
if ($stmt->fetch()) {
  http_response_code(409);
  echo json_encode(['error' => 'Email already registered']);
  exit;
}

// Create account
$hash        = password_hash($pass, PASSWORD_DEFAULT);
$verifyToken = bin2hex(random_bytes(32));

$stmt = $db->prepare('
  INSERT INTO customers (name, email, phone, password_hash, verify_token)
  VALUES (?, ?, ?, ?, ?)
');
$stmt->execute([$name, $email, $phone, $hash, $verifyToken]);
$customerId = $db->lastInsertId();

// Send verification email via Hostinger mail
$verifyUrl = "https://priceboard.transgoldmarkets.com/api/verify.php?token=$verifyToken";

$subject = "Verify your Transgold Markets account";
$message = "
Hi $name,

Welcome to Transgold Markets!

Please verify your email by clicking the link below:
$verifyUrl

This link expires in 24 hours.

Best regards,
Transgold Markets Team
";

$headers = "From: noreply@transgoldmarkets.com\r\nContent-Type: text/plain";
mail($email, $subject, $message, $headers);

echo json_encode([
  'success' => true,
  'message' => 'Registration successful. Please check your email to verify your account.',
  'customer_id' => $customerId
]);
