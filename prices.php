<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-store');

$localFile = __DIR__ . '/prices.json';
$spreadFile = __DIR__ . '/spread.json';

$json = json_decode(file_get_contents($localFile), true);

if (file_exists($spreadFile)) {
    $spread = json_decode(file_get_contents($spreadFile), true);
    $json['spread'] = [
        'goldBid'   => $spread['goldBid']   ?? 0,
        'goldAsk'   => $spread['goldAsk']   ?? 0,
        'silverBid' => $spread['silverBid'] ?? 0,
        'silverAsk' => $spread['silverAsk'] ?? 0,
    ];
    $json['usdSpread'] = [
        'goldBuy'    => $spread['usd']['goldBuy']    ?? 0,
        'goldSell'   => $spread['usd']['goldSell']   ?? 0,
        'silverBuy'  => $spread['usd']['silverBuy']  ?? 0,
        'silverSell' => $spread['usd']['silverSell'] ?? 0,
    ];
} else {
    $json['spread'] = ['goldBid'=>0,'goldAsk'=>0,'silverBid'=>0,'silverAsk'=>0];
    $json['usdSpread'] = ['goldBuy'=>0,'goldSell'=>0,'silverBuy'=>0,'silverSell'=>0];
}

echo json_encode($json);
