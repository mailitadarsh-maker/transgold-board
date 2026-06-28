<?php
require_once __DIR__ . '/api/db.php';
cors();
$db = getDB();
$db->exec("ALTER TABLE orders MODIFY COLUMN status ENUM('pending','confirmed','processing','completed','cancelled','approved') DEFAULT 'pending'");
echo json_encode(['success' => true, 'message' => 'Status enum updated']);
