<?php
require_once __DIR__ . '/db.php';
cors();

$token    = authHeader();
$customer = $token ? verifyToken($token) : null;

// ── GET ORDERS ────────────────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
  if (!$customer) { http_response_code(401); echo json_encode(['error' => 'Unauthorized']); exit; }

  $db   = getDB();
  $stmt = $db->prepare('SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC');
  $stmt->execute([$customer['id']]);
  $orders = $stmt->fetchAll();

  echo json_encode(['success' => true, 'orders' => $orders]);
  exit;
}

// ── PLACE ORDER ───────────────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  if (!$customer) { http_response_code(401); echo json_encode(['error' => 'Unauthorized']); exit; }

  $data = json_decode(file_get_contents('php://input'), true);

  $metal     = $data['metal']     ?? '';
  $purity    = $data['purity']    ?? '';
  $weight    = $data['weight']    ?? 0;
  $unit      = $data['unit']      ?? '';
  $price_aed = $data['price_aed'] ?? 0;
  $spot_usd  = $data['spot_usd']  ?? 0;
  $type      = $data['type']      ?? 'buy';
  $notes     = $data['notes']     ?? '';

  if (!$metal || !$purity || !$weight || !$price_aed) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required fields']);
    exit;
  }

  $db   = getDB();
  $stmt = $db->prepare('
    INSERT INTO orders (customer_id, metal, purity, weight, unit, price_aed, spot_usd, type, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  ');
  $stmt->execute([
    $customer['id'], $metal, $purity, $weight,
    $unit, $price_aed, $spot_usd, $type, $notes
  ]);
  $orderId = $db->lastInsertId();

  // Send WhatsApp to admin via CallMeBot
  $adminPhone   = '+971500000000'; // ← Replace with admin WhatsApp
  $adminApiKey  = 'YOUR_CALLMEBOT_API_KEY'; // ← Replace after setup
  $orderType    = strtoupper($type);
  $msg = urlencode("🔔 NEW ORDER #$orderId\n$orderType $weight$unit $purity $metal\nAED " . number_format($price_aed, 2) . "\nCustomer: {$customer['name']} ({$customer['phone']})");
  
  @file_get_contents("https://api.callmebot.com/whatsapp.php?phone=$adminPhone&text=$msg&apikey=$adminApiKey");

  echo json_encode([
    'success'  => true,
    'order_id' => $orderId,
    'message'  => 'Order placed successfully. We will contact you shortly.'
  ]);
  exit;
}

// ── ADMIN: GET ALL ORDERS ─────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'PUT') {
  // Admin password check
  $data = json_decode(file_get_contents('php://input'), true);
  if (($data['admin_password'] ?? '') !== 'admin2024') {
    http_response_code(403);
    echo json_encode(['error' => 'Forbidden']);
    exit;
  }

  $db     = getDB();
  $status = $data['status'] ?? null;
  $id     = $data['order_id'] ?? null;

  if ($id && $status) {
    // Update order status
    $db->prepare('UPDATE orders SET status = ?, admin_notes = ? WHERE id = ?')
       ->execute([$status, $data['admin_notes'] ?? '', $id]);
    echo json_encode(['success' => true]);
  } else {
    // Get all orders
    $stmt = $db->query('
      SELECT o.*, c.name as customer_name, c.phone as customer_phone, c.email as customer_email
      FROM orders o
      JOIN customers c ON o.customer_id = c.id
      ORDER BY o.created_at DESC
    ');
    echo json_encode(['success' => true, 'orders' => $stmt->fetchAll()]);
  }
  exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
