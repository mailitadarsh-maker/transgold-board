<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-store');

$pricesFile = __DIR__ . '/../prices.json';
$data = file_exists($pricesFile) ? file_get_contents($pricesFile) : null;

if ($data) {
    $json = json_decode($data, true);

    $spreadFile = __DIR__ . '/../spread.json';
    if (file_exists($spreadFile)) {
        $spread = json_decode(file_get_contents($spreadFile), true);
        $master = $spread['master'] ?? $spread;
        $json['spread'] = [
            'goldBid'   => $master['goldBid']   ?? 0,
            'goldAsk'   => $master['goldAsk']   ?? 0,
            'silverBid' => $master['silverBid'] ?? 0,
            'silverAsk' => $master['silverAsk'] ?? 0,
        ];
    } else {
        $json['spread'] = ['goldBid'=>0,'goldAsk'=>0,'silverBid'=>0,'silverAsk'=>0];
    }

    echo json_encode($json);
} else {
    echo json_encode(['ok' => false, 'error' => $err]);
}
