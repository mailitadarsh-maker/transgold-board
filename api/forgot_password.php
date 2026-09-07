<?php
require_once __DIR__ . '/db.php';
cors();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  http_response_code(405);
  echo json_encode(['error' => 'Method not allowed']);
  exit;
}

$data  = json_decode(file_get_contents('php://input'), true);
$email = trim($data['email'] ?? '');

if (!$email || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  http_response_code(400);
  echo json_encode(['error' => 'A valid email is required']);
  exit;
}

$db = getDB();
$stmt = $db->prepare('SELECT id, name FROM customers WHERE email = ?');
$stmt->execute([$email]);
$customer = $stmt->fetch();

// Always return the same success response, whether or not the email exists.
// This prevents user enumeration (an attacker probing which emails are registered).
$genericResponse = [
  'success' => true,
  'message' => 'If an account exists for that email, a password reset link has been sent.',
];

if (!$customer) {
  echo json_encode($genericResponse);
  exit;
}

$resetToken   = bin2hex(random_bytes(32));
$resetExpires = date('Y-m-d H:i:s', strtotime('+1 hour'));

$db->prepare('UPDATE customers SET reset_token = ?, reset_token_expires = ? WHERE id = ?')
   ->execute([$resetToken, $resetExpires, $customer['id']]);

$resetUrl = "https://priceboard.transgoldmarkets.com/api/reset-password.html?token=$resetToken";

$subject = "Reset your Transgold Markets password";
$message = "
Hi {$customer['name']},

We received a request to reset your Transgold Markets password.

Click the link below to set a new password:
$resetUrl

This link expires in 1 hour. If you did not request this, you can safely ignore this email.

Best regards,
Transgold Markets Team
";

$headers = "From: noreply@transgoldmarkets.com\r\nContent-Type: text/plain";
mail($email, $subject, $message, $headers);

echo json_encode($genericResponse);
