<?php
header('Content-Type: application/json');

$cacheFile = __DIR__ . '/../live_price_cache.json';
$ttl = 2; // seconds — tune this down if GoldVaultApp allows tighter polling

if (file_exists($cacheFile) && (time() - filemtime($cacheFile)) < $ttl) {
    readfile($cacheFile);
    exit;
}

$apiKey = getenv('GOLDVAULT_API_KEY'); // set this in Hostinger env, not hardcoded
$ch = curl_init('https://api.goldvaultapp.example/latest'); // <-- swap in real GoldVaultApp URL
curl_setopt($ch, CURLOPT_HTTPHEADER, ["X-API-Key: $apiKey"]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 3);
$raw = curl_exec($ch);
curl_close($ch);

if ($raw === false) {
    // fall back to last good cache rather than erroring the board
    if (file_exists($cacheFile)) { readfile($cacheFile); exit; }
    echo json_encode(['ok' => false]); exit;
}

$data = json_decode($raw, true);
$mid = ($data['bid'] + $data['ask']) / 2;

// merge spread.json + daily_hilo.json same way prices.php already does
$spread = json_decode(@file_get_contents(__DIR__ . '/../spread.json'), true) ?: [];
$hilo   = json_decode(@file_get_contents(__DIR__ . '/../daily_hilo.json'), true) ?: [];

$out = [
    'gold' => $mid,
    'silver' => $data['silver_mid'] ?? null,
    'spread' => $spread,
    'hilo' => $hilo,
    'ts' => time(),
];

file_put_contents($cacheFile, json_encode($out));
echo json_encode($out);
