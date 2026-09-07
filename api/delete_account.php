<?php
require_once __DIR__ . '/db.php';
cors();

if ($_SERVER['REQUEST_METHOD'] !== 'POST' && $_SERVER['REQUEST_METHOD'] !== 'DELETE') {
  http_response_code(405);
  echo json_encode(['error' => 'Method not allowed']);
  exit;
}

$token = authHeader();
if (!$token) {
  http_response_code(401);
  echo json_encode(['error' => 'Missing authorization token']);
  exit;
}

$customer = verifyToken($token);
if (!$customer) {
  http_response_code(401);
  echo json_encode(['error' => 'Invalid or expired session']);
  exit;
}

$db = getDB();
$customerId = $customer['id'];

try {
  $db->beginTransaction();
  $stmt = $db->prepare('DELETE FROM orders WHERE customer_id = ?');
  $stmt->execute([$customerId]);
  $stmt = $db->prepare('DELETE FROM customers WHERE id = ?');
  $stmt->execute([$customerId]);
  $db->commit();
  echo json_encode(['success' => true, 'message' => 'Account and all associated data have been permanently deleted']);
} catch (Exception $e) {
  $db->rollBack();
  http_response_code(500);
  echo json_encode(['error' => 'Failed to delete account. Please try again.']);
}
