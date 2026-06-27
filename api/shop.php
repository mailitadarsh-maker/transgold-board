<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

$shopFile = __DIR__ . '/../shop.json';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  // Save shop details (from admin panel)
  $data = json_decode(file_get_contents('php://input'), true);
  if ($data) {
    file_put_contents($shopFile, json_encode($data, JSON_PRETTY_PRINT));
    echo json_encode(['success' => true]);
  } else {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid data']);
  }
} else {
  // Return shop details
  if (file_exists($shopFile)) {
    echo file_get_contents($shopFile);
  } else {
    echo json_encode([
      'name' => 'Transgold Markets',
      'tagline' => 'Your Trusted Gold & Silver Trading Partner in UAE',
      'whatsapp' => '+971500000000',
      'phone' => '+97140000000',
      'email' => 'info@transgoldmarkets.com',
      'address' => 'Gold Souk, Deira, Dubai, UAE',
      'mapsUrl' => 'https://maps.google.com/?q=Gold+Souk+Deira+Dubai',
      'hours' => [
        ['day' => 'Monday – Saturday', 'time' => '9:00 AM – 9:00 PM'],
        ['day' => 'Sunday', 'time' => '10:00 AM – 6:00 PM']
      ]
    ]);
  }
}
