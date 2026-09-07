<?php
date_default_timezone_set('Asia/Dubai');
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-store');

$goldVaultKey = '7e8YKZCZ2kK2_FXAFKefifcHggibYk5tQ6SAAb7vXsM';
$cacheFile  = __DIR__ . '/../live_price_cache.json';
$pricesFile = __DIR__ . '/../prices.json';
$hiloFile   = __DIR__ . '/../daily_hilo.json';
$spreadFile = __DIR__ . '/../spread.json';
$ttl = 2; // seconds — floor to avoid hammering GoldVaultApp under concurrent load

if (file_exists($cacheFile) && (time() - filemtime($cacheFile)) < $ttl) {
    readfile($cacheFile);
    exit;
}

function fetchGoldVaultPrice($symbol, $apiKey) {
    $url = 'https://metalprice.goldvaultapp.com/getprice/' . $symbol;
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['X-API-Key: ' . $apiKey]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 3);
    $raw = curl_exec($ch);
    curl_close($ch);
    if ($raw === false || $raw === '') return null;
    $data = json_decode($raw, true);
    if (!is_array($data) || !isset($data['bid']) || !isset($data['ask'])) return null;
    return $data;
}

$goldData   = fetchGoldVaultPrice('XAUUSD', $goldVaultKey);
$silverData = fetchGoldVaultPrice('XAGUSD', $goldVaultKey);

if (!$goldData || !$silverData) {
    // fetch failed — serve last known good cache/prices.json rather than error the board
    if (file_exists($cacheFile)) { readfile($cacheFile); exit; }
    if (file_exists($pricesFile)) { readfile($pricesFile); exit; }
    echo json_encode(['ok' => false]);
    exit;
}

$gold   = round(($goldData['bid'] + $goldData['ask']) / 2, 2);
$silver = round(($silverData['bid'] + $silverData['ask']) / 2, 2);

$json = ['gold' => $gold, 'silver' => $silver, 'ok' => true, 'ts' => time()];
file_put_contents($pricesFile, json_encode($json));

// same locked hi/lo update pattern as cron_prices.php — keeps intra-minute
// spikes from being lost between cron ticks
$today = date('Y-m-d');
$fh = fopen($hiloFile, 'c+');
$hilo = null;
if ($fh && flock($fh, LOCK_EX)) {
    $raw = stream_get_contents($fh);
    $hilo = json_decode($raw, true);
    if (!is_array($hilo) || ($hilo['date'] ?? '') !== $today) {
        $hilo = ['date' => $today, 'goldLow' => $gold, 'goldHigh' => $gold, 'silverLow' => $silver, 'silverHigh' => $silver];
    } else {
        $hilo['goldLow']    = min($hilo['goldLow'], $gold);
        $hilo['goldHigh']   = max($hilo['goldHigh'], $gold);
        $hilo['silverLow']  = min($hilo['silverLow'], $silver);
        $hilo['silverHigh'] = max($hilo['silverHigh'], $silver);
    }
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($hilo));
    fflush($fh);
    flock($fh, LOCK_UN);
    fclose($fh);
}

$json['goldLow']    = $hilo['goldLow']    ?? $gold;
$json['goldHigh']   = $hilo['goldHigh']   ?? $gold;
$json['silverLow']  = $hilo['silverLow']  ?? $silver;
$json['silverHigh'] = $hilo['silverHigh'] ?? $silver;

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

file_put_contents($cacheFile, json_encode($json));
echo json_encode($json);
