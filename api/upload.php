<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

define('UPLOAD_DIR',  __DIR__ . '/../media/');
define('UPLOAD_URL',  '/media/');
define('MAX_SLOTS',   3);
define('MAX_SIZE_MB', 50);
define('SLOTS_FILE',  __DIR__ . '/../media/slots.json');

$ALLOWED_TYPES = [
  'image/jpeg','image/jpg','image/png','image/gif','image/webp',
  'video/mp4','video/webm','video/ogg','video/quicktime'
];

if (!is_dir(UPLOAD_DIR)) mkdir(UPLOAD_DIR, 0755, true);

$action = $_POST['action'] ?? $_GET['action'] ?? 'upload';

switch ($action) {
  case 'list':
    echo json_encode(['success'=>true,'slots'=>loadSlots()]);
    exit;

  case 'remove':
    $slot = (int)($_POST['slot'] ?? -1);
    if ($slot < 0 || $slot >= MAX_SLOTS) { echo json_encode(['success'=>false,'error'=>'Invalid slot']); exit; }
    $slots = loadSlots();
    if ($slots[$slot]) { $fp = UPLOAD_DIR.$slots[$slot]['filename']; if(file_exists($fp)) unlink($fp); $slots[$slot]=null; }
    saveSlots($slots);
    echo json_encode(['success'=>true,'slots'=>$slots]);
    exit;

  case 'clear':
    $slots = loadSlots();
    foreach($slots as $s) { if($s){ $fp=UPLOAD_DIR.$s['filename']; if(file_exists($fp)) unlink($fp); } }
    $slots=[null,null,null];
    saveSlots($slots);
    echo json_encode(['success'=>true,'slots'=>$slots]);
    exit;

  default:
    if ($_SERVER['REQUEST_METHOD']!=='POST') { http_response_code(405); echo json_encode(['success'=>false,'error'=>'POST required']); exit; }
    $slot=(int)($_POST['slot']??-1);
    if ($slot<0||$slot>=MAX_SLOTS) { echo json_encode(['success'=>false,'error'=>'slot must be 0-2']); exit; }
    if (empty($_FILES['file'])) { echo json_encode(['success'=>false,'error'=>'No file received']); exit; }
    $file=$_FILES['file'];
    if ($file['error']!==UPLOAD_ERR_OK) { echo json_encode(['success'=>false,'error'=>'Upload error: '.$file['error']]); exit; }
    if ($file['size']>MAX_SIZE_MB*1024*1024) { echo json_encode(['success'=>false,'error'=>'File exceeds '.MAX_SIZE_MB.' MB']); exit; }
    $finfo=new finfo(FILEINFO_MIME_TYPE);
    $mime=$finfo->file($file['tmp_name']);
    if (!in_array($mime,$ALLOWED_TYPES)) { echo json_encode(['success'=>false,'error'=>'Type not allowed: '.$mime]); exit; }
    $extMap=['image/jpeg'=>'jpg','image/jpg'=>'jpg','image/png'=>'png','image/gif'=>'gif','image/webp'=>'webp','video/mp4'=>'mp4','video/webm'=>'webm','video/ogg'=>'ogv','video/quicktime'=>'mov'];
    $ext=$extMap[$mime]??'bin';
    $slots=loadSlots();
    if ($slots[$slot]) { $old=UPLOAD_DIR.$slots[$slot]['filename']; if(file_exists($old)) unlink($old); }
    $filename='slot'.$slot.'_'.time().'.'.$ext;
    $dest=UPLOAD_DIR.$filename;
    if (!move_uploaded_file($file['tmp_name'],$dest)) { echo json_encode(['success'=>false,'error'=>'Failed to save file']); exit; }
    $slots[$slot]=['filename'=>$filename,'url'=>UPLOAD_URL.$filename,'type'=>str_starts_with($mime,'video/')?'video':'image','name'=>basename($file['name'])];
    saveSlots($slots);
    echo json_encode(['success'=>true,'slot'=>$slots[$slot],'slots'=>$slots]);
    exit;
}

function loadSlots(): array {
  if (!file_exists(SLOTS_FILE)) return [null,null,null];
  $data=json_decode(file_get_contents(SLOTS_FILE),true);
  return array_slice(array_pad((array)$data,3,null),0,3);
}
function saveSlots(array $slots): void {
  file_put_contents(SLOTS_FILE,json_encode($slots,JSON_PRETTY_PRINT));
}
