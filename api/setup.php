<?php
require_once __DIR__ . '/db.php';
cors();

$db = getDB();

$tables = [
'customers' => "
CREATE TABLE IF NOT EXISTS customers (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(100) NOT NULL,
  email         VARCHAR(150) NOT NULL UNIQUE,
  phone         VARCHAR(20),
  password_hash VARCHAR(255) NOT NULL,
  is_verified   TINYINT(1) DEFAULT 0,
  verify_token  VARCHAR(64),
  auth_token    VARCHAR(64),
  token_expires DATETIME,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
",

'orders' => "
CREATE TABLE IF NOT EXISTS orders (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  customer_id   INT NOT NULL,
  metal         ENUM('gold','silver') NOT NULL,
  purity        VARCHAR(10) NOT NULL,
  weight        DECIMAL(10,3) NOT NULL,
  unit          VARCHAR(10) NOT NULL,
  price_aed     DECIMAL(12,2) NOT NULL,
  spot_usd      DECIMAL(10,4) NOT NULL,
  type          ENUM('buy','sell') NOT NULL,
  status        ENUM('pending','confirmed','processing','completed','cancelled') DEFAULT 'pending',
  notes         TEXT,
  admin_notes   TEXT,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
",

'notifications' => "
CREATE TABLE IF NOT EXISTS notifications (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  order_id    INT,
  type        VARCHAR(50),
  message     TEXT,
  sent        TINYINT(1) DEFAULT 0,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"
];

$results = [];
foreach ($tables as $name => $sql) {
  try {
    $db->exec($sql);
    $results[$name] = 'created';
  } catch (PDOException $e) {
    $results[$name] = 'error: ' . $e->getMessage();
  }
}

echo json_encode(['success' => true, 'tables' => $results]);
