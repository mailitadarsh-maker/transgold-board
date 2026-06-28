<?php
// Fetch live price from Arakkal via existing proxy
$arakkalUrls = [
    'https://portal.arakkalmarkets.com/api/v1/rates',
    'https://portal.arakkalmarkets.com/rates',
    'https://portal.arakkalmarkets.com/api/rates',
];

$gold = null;
$silver = null;

foreach ($arakkalUrls as $url) {
    $proxyUrl = 'https://priceboard.transgoldmarkets.com/api/proxy.php?url=' . urlencode($url);
    $raw = @file_get_contents($proxyUrl);
    if ($raw) {
        $data = json_decode($raw, true);
        if (isset($data['XAU']) || isset($data['gold'])) {
            $gold = $data['XAU'] ?? $data['gold'];
            $silver = $data['XAG'] ?? $data['silver'];
            break;
        }
    }
}

if ($gold) {
    $json = json_encode(['gold' => $gold, 'silver' => $silver, 'ok' => true, 'ts' => time()]);
    file_put_contents(__DIR__ . '/prices.json', $json);
    echo "Updated: gold=$gold silver=$silver";
} else {
    echo "Failed to fetch live price";
}
