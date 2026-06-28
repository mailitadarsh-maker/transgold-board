<?php
$proxyBase = 'https://priceboard.transgoldmarkets.com/api/proxy.php?url=';

$goldRaw   = @file_get_contents($proxyBase . urlencode('https://portal.arakkalmarkets.com/getprice/GOLD'));
$silverRaw = @file_get_contents($proxyBase . urlencode('https://portal.arakkalmarkets.com/getprice/SILVER'));

// Strip HTML debug output and extract JSON
preg_match('/"Bid"[^0-9]*([0-9.]+)/', $goldRaw, $gm);
preg_match('/"Bid"[^0-9]*([0-9.]+)/', $silverRaw, $sm);

$gold   = isset($gm[1]) ? floatval($gm[1]) : null;
$silver = isset($sm[1]) ? floatval($sm[1]) : null;

if ($gold && $silver) {
    $json = json_encode(['gold' => $gold, 'silver' => $silver, 'ok' => true, 'ts' => time()]);
    file_put_contents(__DIR__ . '/prices.json', $json);
    echo "Updated: gold=$gold silver=$silver";
} else {
    echo "Failed — gold=$gold silver=$silver";
}
