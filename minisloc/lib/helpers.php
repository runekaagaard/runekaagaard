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
	return str_replace(array(cfg::$site_path, '.php'), '', $path);
}

function yaml($content) {
	return syck_load($content);
}

function to_title($string) {
	return ucwords(str_replace(array('-', '.php'), array(' ', ''), basename($string)));
}

function files_in_site($dir = null, &$files = array()) {
	if (!$dir) $dir = cfg::$site_path;
	$files_in_dir = glob($dir . '*');
	$dirs_in_dir = glob($dir . '*', GLOB_ONLYDIR);
	foreach ($files_in_dir as $path) {
		$url = url_from_path($path);
		$last_url_part = basename($url);
		if (in_array($path, $dirs_in_dir)) {
			$files[$last_url_part] = files_in_site($path . '/', $files[$url]);
		} else {
			$file = read_file($path);
			$settings = array(
				'basename' => basename($path),
				'path' => $path,
				'title' => to_title($path),
				'url' => $url,
				'teaser' => text::truncate($file['content']),
				'content' => $file['content'],
				'created' => 0,
			);
			$settings = array_merge($settings, $file['settings']);
			if ($settings['created'] instanceof DateTime) {
				$settings['created'] = $settings['created']->format('U');
			}
			$files[$last_url_part] = $settings;
		}
	}
	uasort($files, 'files_sort');
	return $files;
}

function files_sort($a, $b) {
	if (!isset($a['created']) || !isset($b['created'])) return 0;
	if ($a['created'] == $b['created']) return 0;
	return ($a['created'] > $b['created']) ? -1 : 1;
}

function cache_fetch($key) {
	if (!cfg::$cache) return false;
	return apc_fetch($key);
}

function cache_store($key, $var) {
	if (!cfg::$cache) return false;
	return apc_store($key, $var);
}

function clear() {
	return '<div class="clear"></div>';
}