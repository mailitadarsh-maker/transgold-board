<?php
header('Content-Type: text/html; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-cache, no-store, must-revalidate');

$allowed_host = 'portal.arakkalmarkets.com';
$url = $_GET['url'] ?? '';

if (!$url) { http_response_code(400); echo 'Missing url'; exit; }

$parsed = parse_url($url);
if (!$parsed || ($parsed['host'] ?? '') !== $allowed_host) {
    http_response_code(403); echo 'Host not allowed'; exit;
}

$ctx = stream_context_create(['http' => ['timeout' => 5, 'ignore_errors' => true, 'user_agent' => 'TransgoldMarkets/1.0']]);
$response = @file_get_contents($url, false, $ctx);

if ($response === false) { http_response_code(502); echo 'Fetch failed'; exit; }
echo $response;
