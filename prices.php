<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-store');

$url = 'https://raw.githubusercontent.com/mailitadarsh-maker/transgold-board/main/prices.json';

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
$data = curl_exec($ch);
$err  = curl_error($ch);
curl_close($ch);

if ($data && !$err) {
    $json = json_decode($data, true);

    // Read spread.json saved by admin dashboard
    $spreadFile = __DIR__ . '/spread.json';
    if (file_exists($spreadFile)) {
        $spread = json_decode(file_get_contents($spreadFile), true);
        $json['spread'] = [
            'goldBid'   => $spread['goldBid']   ?? 0,
            'goldAsk'   => $spread['goldAsk']   ?? 0,
            'silverBid' => $spread['silverBid'] ?? 0,
            'silverAsk' => $spread['silverAsk'] ?? 0,
        ];
    } else {
        $json['spread'] = ['goldBid'=>0,'goldAsk'=>0,'silverBid'=>0,'silverAsk'=>0];
    }

    echo json_encode($json);
} else {
    echo json_encode(['ok' => false, 'error' => $err]);
}
