<?php
require_once __DIR__ . '/db.php';
cors();

// ── VERIFY EMAIL ──────────────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['token'])) {
  $token = $_GET['token'];
  $db = getDB();

  $stmt = $db->prepare('SELECT id FROM customers WHERE verify_token = ? AND is_verified = 0');
  $stmt->execute([$token]);
  $customer = $stmt->fetch();

  if (!$customer) {
    echo "<h2>Invalid or already used verification link.</h2>";
    exit;
  }

  $db->prepare('UPDATE customers SET is_verified = 1, verify_token = NULL WHERE id = ?')
     ->execute([$customer['id']]);

  echo "
  <html>
  <head><title>Verified — Transgold Markets</title>
  <style>
    body { font-family: Arial; background: #0a0a0a; color: #fff; display:flex; align-items:center; justify-content:center; height:100vh; margin:0; }
    .box { text-align:center; padding:40px; border:1px solid #C9A84C; border-radius:16px; }
    h2 { color: #C9A84C; }
    p { color: #aaa; }
  </style>
  </head>
  <body>
    <div class='box'>
      <h2>✓ Email Verified!</h2>
      <p>Your Transgold Markets account is now active.</p>
      <p>You can now log in on the app.</p>
    </div>
  </body>
  </html>
  ";
  exit;
}

// ── LOGIN ─────────────────────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $data  = json_decode(file_get_contents('php://input'), true);
  $email = trim($data['email']    ?? '');
  $pass  = $data['password']      ?? '';

  if (!$email || !$pass) {
    http_response_code(400);
    echo json_encode(['error' => 'Email and password required']);
    exit;
  }

  $db   = getDB();
  $stmt = $db->prepare('SELECT * FROM customers WHERE email = ?');
  $stmt->execute([$email]);
  $customer = $stmt->fetch();

  if (!$customer || !password_verify($pass, $customer['password_hash'])) {
    http_response_code(401);
    echo json_encode(['error' => 'Invalid email or password']);
    exit;
  }

  if (!$customer['is_verified']) {
    http_response_code(403);
    echo json_encode(['error' => 'Please verify your email before logging in']);
    exit;
  }

  // Generate token
  $token   = bin2hex(random_bytes(32));
  $expires = date('Y-m-d H:i:s', strtotime('+30 days'));

  $db->prepare('UPDATE customers SET auth_token = ?, token_expires = ? WHERE id = ?')
     ->execute([$token, $expires, $customer['id']]);

  echo json_encode([
    'success'  => true,
    'token'    => $token,
    'customer' => [
      'id'    => $customer['id'],
      'name'  => $customer['name'],
      'email' => $customer['email'],
      'phone' => $customer['phone'],
    ]
  ]);
  exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
