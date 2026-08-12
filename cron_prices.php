<?php
date_default_timezone_set('Asia/Dubai');

// --- GoldVaultApp price source ---
$goldVaultKey = '7e8YKZCZ2kK2_FXAFKefifcHggibYk5tQ6SAAb7vXsM';

function fetchGoldVaultPrice($symbol, $apiKey) {
    $url = 'https://metalprice.goldvaultapp.com/getprice/' . $symbol;
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['X-API-Key: ' . $apiKey]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 8);
    $raw = curl_exec($ch);
    $err = curl_error($ch);
    curl_close($ch);

    if ($raw === false || $raw === '') {
        return null;
    }
    $data = json_decode($raw, true);
    if (!is_array($data) || !isset($data['bid']) || !isset($data['ask'])) {
        return null;
    }
    return $data; // ['symbol'=>.., 'bid'=>.., 'ask'=>.., 'time'=>..]
}

$goldData   = fetchGoldVaultPrice('XAUUSD', $goldVaultKey);
$silverData = fetchGoldVaultPrice('XAGUSD', $goldVaultKey);

// Mid price keeps prices.json's existing shape (single number per metal),
// same convention the old arakkalmarkets feed used.
$gold   = $goldData   ? round(($goldData['bid'] + $goldData['ask']) / 2, 2)   : null;
$silver = $silverData ? round(($silverData['bid'] + $silverData['ask']) / 2, 2) : null;

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
