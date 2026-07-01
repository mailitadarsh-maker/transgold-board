<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

$file = __DIR__.'/spread.json';
$data = json_decode(file_get_contents('php://input'), true);
if (!$data) { echo json_encode(['ok'=>false,'error'=>'no data']); exit; }

// Merge with existing file instead of overwriting it wholesale.
// index.html's admin panel only posts {master, override}; admin.html
// posts {master, override, usd}. A blind overwrite from either one
// wipes out whatever key the other panel wasn't sending — that was
// the bug (AED/USD spread "disappearing" a few seconds after saving).
$existing = [];
if (file_exists($file)) {
    $existing = json_decode(file_get_contents($file), true) ?: [];
}
$merged = array_merge($existing, $data);

file_put_contents($file, json_encode($merged, JSON_PRETTY_PRINT));
echo json_encode(['ok'=>true, 'saved'=>$merged]);
