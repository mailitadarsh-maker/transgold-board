<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-store');

$localFile = __DIR__ . '/prices.json';
$spreadFile = __DIR__ . '/spread.json';
$hiloFile = __DIR__ . '/daily_hilo.json';

$json = json_decode(file_get_contents($localFile), true);

if (file_exists($hiloFile)) {
    $hilo = json_decode(file_get_contents($hiloFile), true);
    $json['goldLow']    = $hilo['goldLow']    ?? $json['gold'];
    $json['goldHigh']   = $hilo['goldHigh']   ?? $json['gold'];
    $json['silverLow']  = $hilo['silverLow']  ?? $json['silver'];
    $json['silverHigh'] = $hilo['silverHigh'] ?? $json['silver'];
}

if (file_exists($spreadFile)) {
    $spread = json_decode(file_get_contents($spreadFile), true);
    $json['spread'] = [
        'goldBid'   => $spread['master']['goldBid']   ?? 0,
        'goldAsk'   => $spread['master']['goldAsk']   ?? 0,
        'silverBid' => $spread['master']['silverBid'] ?? 0,
        'silverAsk' => $spread['master']['silverAsk'] ?? 0,
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
