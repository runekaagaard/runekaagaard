<?php
class cfg {
	public static $files_in_site;
	public static $cache = true;
	public function __construct() {
		$files_in_site = cache_fetch('files_in_site');
		if (!$files_in_site) {
			$files_in_site = files_in_site();
			cache_store('files_in_site', $files_in_site);
		}
		self::$files_in_site = $files_in_site;
	}
}