<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-store');

$localFile = dirname(__DIR__) . '/prices.json';
$spreadFile = dirname(__DIR__) . '/spread.json';

$json = json_decode(file_get_contents($localFile), true);

if (file_exists($spreadFile)) {
    $spread = json_decode(file_get_contents($spreadFile), true);
    $json['spread'] = [
        'goldBid'   => $spread['master']['goldBid']   ?? 0,
        'goldAsk'   => $spread['master']['goldAsk']   ?? 0,
        'silverBid' => $spread['master']['silverBid'] ?? 0,
        'silverAsk' => $spread['master']['silverAsk'] ?? 0,
    ];
} else {
    $json['spread'] = ['goldBid'=>0,'goldAsk'=>0,'silverBid'=>0,'silverAsk'=>0];
}

echo json_encode($json);
