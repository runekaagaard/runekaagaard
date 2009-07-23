<?php
function parse($file, array $data=array()) {
	extract($data);
	ob_start();
	require $file;
	return ob_get_clean();
}

function redirect($location) {
	header("Location: $location");
	exit;
}

function read_file($path) {
	ob_start();
	$settings = require $path;
	if (!is_array($settings)) $settings = array();
	return array(
		'content' => ob_get_clean(),
		'settings' => $settings,
	);
}

function url_from_path($path) {
	return str_replace(array(RUNE_SITE_PATH, '.php'), '', $path);
}

function yaml($content) {
	return syck_load($content);
}

function to_title($string) {
	return ucwords(str_replace(array('-', '.php'), array(' ', ''), basename($string)));
}

function uri() {
	static $d = null;
	if (!$d) $d = dispatcher::get_instance();
	return $d->uri;
}

function files_in_site($dir = RUNE_SITE_PATH, &$files = array()) {
	$files_in_dir = glob($dir . '*');
	$dirs_in_dir = glob($dir . '*', GLOB_ONLYDIR);
	foreach ($files_in_dir as $path) {
		$url = url_from_path($path);
		if (in_array($path, $dirs_in_dir)) {
			$files[$url] = files_in_site($path . '/', $files[$url]);
		} else {
			$file = read_file($path);
			$settings = array(
				'basename' => basename($path),
				'path' => $path,
				'title' => to_title($path),
				'url' => $url,
				'teaser' => text::truncate($file['content']),
				'content' => $file['content'],
			);
			$settings = array_merge($settings, $file['settings']);
			$files[$url] = $settings;
		}
	}
	uasort($files, 'files_sort');
	return $files;
}

function files_sort($a, $b) {
	if (empty($a['created']) || empty($b['created'])) return 0;
	$a = $a['created']->format('U');
	$b = $b['created']->format('U');
	if ($a == $b) return 0;
	return ($a > $b) ? -1 : 1;
}

function cache_fetch($key) {
	if (!cfg::$cache) return false;
	return apc_fetch($key);
}

function cache_store($key, $var) {
	if (!cfg::$cache) return false;
	return apc_store($key, $var);
}