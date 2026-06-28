<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-store');

$goldUrl   = 'https://portal.arakkalmarkets.com/getprice/GOLD';
$silverUrl = 'https://portal.arakkalmarkets.com/getprice/SILVER';

$proxyBase = 'https://priceboard.transgoldmarkets.com/api/proxy.php?url=';

$goldRaw   = @file_get_contents($proxyBase . urlencode($goldUrl));
$silverRaw = @file_get_contents($proxyBase . urlencode($silverUrl));

$goldData   = json_decode($goldRaw, true);
$silverData = json_decode($silverRaw, true);

$gold   = $goldData['price']   ?? $goldData['Price']   ?? $goldData['value'] ?? null;
$silver = $silverData['price'] ?? $silverData['Price'] ?? $silverData['value'] ?? null;

if ($gold && $silver) {
    $json = json_encode(['gold' => floatval($gold), 'silver' => floatval($silver), 'ok' => true, 'ts' => time()]);
    file_put_contents(__DIR__ . '/prices.json', $json);
    echo "Updated: gold=$gold silver=$silver";
} else {
    echo "Failed — goldRaw: $goldRaw | silverRaw: $silverRaw";
}
