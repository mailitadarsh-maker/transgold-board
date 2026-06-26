<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');
$data = json_decode(file_get_contents('php://input'), true);
if (!$data) { echo json_encode(['ok'=>false,'error'=>'no data']); exit; }
file_put_contents(__DIR__.'/spread.json', json_encode($data, JSON_PRETTY_PRINT));
echo json_encode(['ok'=>true]);
