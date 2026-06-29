<?php
$proxyBase = 'https://priceboard.transgoldmarkets.com/api/proxy.php?url=';
$goldRaw   = @file_get_contents($proxyBase . urlencode('https://portal.arakkalmarkets.com/getprice/GOLD'));
$silverRaw = @file_get_contents($proxyBase . urlencode('https://portal.arakkalmarkets.com/getprice/SILVER'));

preg_match_all('/<span class=sf-dump-num>([0-9.]+)<\/span>/', $goldRaw, $gm);
preg_match_all('/<span class=sf-dump-num>([0-9.]+)<\/span>/', $silverRaw, $sm);

$gold   = isset($gm[1][1]) ? floatval($gm[1][1]) : null;
$silver = isset($sm[1][1]) ? floatval($sm[1][1]) : null;

if ($gold && $silver) {
    $json = json_encode(['gold' => $gold, 'silver' => $silver, 'ok' => true, 'ts' => time()]);
    $path = __DIR__ . '/prices.json';
    file_put_contents($path, $json);
    echo "Updated: gold=$gold silver=$silver";
} else {
    echo "Failed — gold=$gold silver=$silver";
}
