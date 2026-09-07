<?php
require_once __DIR__ . '/db.php';
cors();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  http_response_code(405);
  echo json_encode(['error' => 'Method not allowed']);
  exit;
}

$data     = json_decode(file_get_contents('php://input'), true);
$token    = trim($data['token'] ?? '');
$password = $data['password'] ?? '';

if (!$token || !$password) {
  http_response_code(400);
  echo json_encode(['error' => 'Token and new password are required']);
  exit;
}

if (strlen($password) < 6) {
  http_response_code(400);
  echo json_encode(['error' => 'Password must be at least 6 characters']);
  exit;
}

$db = getDB();
$stmt = $db->prepare('SELECT id FROM customers WHERE reset_token = ? AND reset_token_expires > NOW()');
$stmt->execute([$token]);
$customer = $stmt->fetch();

if (!$customer) {
  http_response_code(400);
  echo json_encode(['error' => 'This reset link is invalid or has expired. Please request a new one.']);
  exit;
}

$hash = password_hash($password, PASSWORD_DEFAULT);

$db->prepare('UPDATE customers SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL, auth_token = NULL, token_expires = NULL WHERE id = ?')
   ->execute([$hash, $customer['id']]);

echo json_encode([
  'success' => true,
  'message' => 'Your password has been reset. You can now log in with your new password.',
]);
