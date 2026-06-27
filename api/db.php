<?php
define('DB_HOST', '127.0.0.1');
define('DB_NAME', 'u561967956_Transgold');
define('DB_USER', 'u561967956_Transgold');
define('DB_PASS', 'Trans@Gold@007');

function getDB() {
  static $pdo = null;
  if ($pdo === null) {
    try {
      $pdo = new PDO(
        'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4',
        DB_USER,
        DB_PASS,
        [
          PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
          PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
          PDO::ATTR_EMULATE_PREPARES   => false,
        ]
      );
    } catch (PDOException $e) {
      http_response_code(500);
      die(json_encode(['error' => 'Database connection failed']));
    }
  }
  return $pdo;
}

function cors() {
  header('Content-Type: application/json');
  header('Access-Control-Allow-Origin: *');
  header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
  header('Access-Control-Allow-Headers: Content-Type, Authorization');
  if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(200); exit; }
}

function authHeader() {
  $headers = getallheaders();
  $auth = $headers['Authorization'] ?? $headers['authorization'] ?? '';
  if (str_starts_with($auth, 'Bearer ')) {
    return substr($auth, 7);
  }
  return null;
}

function verifyToken($token) {
  $db = getDB();
  $stmt = $db->prepare('SELECT * FROM customers WHERE auth_token = ? AND token_expires > NOW()');
  $stmt->execute([$token]);
  return $stmt->fetch();
}
