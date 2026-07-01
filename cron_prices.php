<?php
date_default_timezone_set('Asia/Dubai');

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

    // Daily high/low tracking (Asia/Dubai trading day). Resets automatically
    // whenever the stored date differs from today; otherwise widens the
    // running min/max. File-locked so overlapping cron runs can't clobber
    // each other's updates.
    $hiloPath = __DIR__ . '/daily_hilo.json';
    $today = date('Y-m-d');
    $fh = fopen($hiloPath, 'c+');
    if ($fh && flock($fh, LOCK_EX)) {
        $raw = stream_get_contents($fh);
        $hilo = json_decode($raw, true);
        if (!is_array($hilo) || ($hilo['date'] ?? '') !== $today) {
            // New trading day (or file missing/corrupt) — start fresh from current price
            $hilo = [
                'date'       => $today,
                'goldLow'    => $gold,
                'goldHigh'   => $gold,
                'silverLow'  => $silver,
                'silverHigh' => $silver,
            ];
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

    echo "Updated: gold=$gold silver=$silver";
} else {
    echo "Failed — gold=$gold silver=$silver";
}
