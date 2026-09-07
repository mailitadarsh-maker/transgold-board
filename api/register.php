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
$verifyUrl = "https://priceboard.transgoldmarkets.com/api/auth.php?token=$verifyToken";

$subject = "Verify your Feelani account";
$safeName = htmlspecialchars($name);
$message = <<<HTML
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background-color:#0a0a0a; font-family: Arial, Helvetica, sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#0a0a0a; padding:40px 0;">
    <tr>
      <td align="center">
        <table role="presentation" width="480" cellpadding="0" cellspacing="0" style="background-color:#141414; border:1px solid #1e1e1e; border-radius:14px; overflow:hidden;">
          <tr>
            <td align="center" style="padding:36px 32px 8px 32px;">
              <div style="font-size:26px; font-weight:800; letter-spacing:4px; color:#D4AF37; font-family: Georgia, serif;">FEELANI</div>
              <div style="font-size:11px; letter-spacing:2px; color:#777; margin-top:6px;">LIVE GOLD &amp; SILVER PRICES</div>
            </td>
          </tr>
          <tr>
            <td style="padding:24px 32px 8px 32px; border-top:1px solid #1e1e1e;">
              <p style="color:#fff; font-size:16px; margin:16px 0 0 0;">Hi {$safeName},</p>
              <p style="color:#ccc; font-size:14px; line-height:1.6; margin:12px 0;">Welcome to Feelani! Please confirm your email address to activate your account.</p>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:20px 32px 8px 32px;">
              <a href="{$verifyUrl}" style="display:inline-block; background-color:#D4AF37; color:#000; text-decoration:none; font-weight:700; font-size:14px; letter-spacing:1px; padding:14px 32px; border-radius:10px;">VERIFY EMAIL</a>
            </td>
          </tr>
          <tr>
            <td style="padding:16px 32px 32px 32px;">
              <p style="color:#666; font-size:12px; line-height:1.5; margin:0;">This link expires in 24 hours. If you did not create a Feelani account, you can safely ignore this email.</p>
            </td>
          </tr>
          <tr>
            <td style="padding:16px 32px; border-top:1px solid #1e1e1e;">
              <p style="color:#555; font-size:11px; margin:0; text-align:center;">Feelani &middot; Best regards, the Feelani Team</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
HTML;

$headers = "From: Feelani <noreply@transgoldmarkets.com>\r\nMIME-Version: 1.0\r\nContent-Type: text/html; charset=UTF-8";
mail($email, $subject, $message, $headers);

echo json_encode([
  'success' => true,
  'message' => 'Registration successful. Please check your email to verify your account.',
  'customer_id' => $customerId
]);
