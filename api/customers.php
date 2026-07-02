<?php
require_once __DIR__ . '/db.php';
cors();

if ($_SERVER['REQUEST_METHOD'] !== 'PUT') {
  http_response_code(405);
  echo json_encode(['error' => 'Method not allowed']);
  exit;
}

$data = json_decode(file_get_contents('php://input'), true);
if (($data['admin_password'] ?? '') !== 'admin2024') {
  http_response_code(403);
  echo json_encode(['error' => 'Forbidden']);
  exit;
}

$db = getDB();
$customerId = $data['customer_id'] ?? null;

if ($customerId) {
  // -- SINGLE CUSTOMER: profile + full order history --
  $stmt = $db->prepare('SELECT id, name, email, phone, is_verified, created_at FROM customers WHERE id = ?');
  $stmt->execute([$customerId]);
  $customer = $stmt->fetch();

  if (!$customer) {
    http_response_code(404);
    echo json_encode(['error' => 'Customer not found']);
    exit;
  }

  $stmt = $db->prepare('
    SELECT id, metal, purity, weight, unit, price_aed, spot_usd, type, status, notes, admin_notes, created_at, updated_at
    FROM orders
    WHERE customer_id = ?
    ORDER BY created_at DESC
  ');
  $stmt->execute([$customerId]);
  $orders = $stmt->fetchAll();

  echo json_encode([
    'success'  => true,
    'customer' => $customer,
    'orders'   => $orders,
  ]);
  exit;
}

// -- ALL CUSTOMERS: list with order-count / total AED summary --
$stmt = $db->query('
  SELECT
    c.id, c.name, c.email, c.phone, c.is_verified, c.created_at,
    COUNT(o.id) AS order_count,
    COALESCE(SUM(CASE WHEN o.status = "completed" THEN o.price_aed ELSE 0 END), 0) AS total_aed,
    MAX(o.created_at) AS last_order_at
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id
  GROUP BY c.id
  ORDER BY c.created_at DESC
');
echo json_encode(['success' => true, 'customers' => $stmt->fetchAll()]);
