<?php
class cfg {
	public static $path;
	public static $site_path;
	public static $uri;
	public static $files_in_site;
	public static $cache = false;
	public static $base_url = 'http://runekaagaard.com/';
	
	public static function set_variables() {
		self::$path = realpath(dirname(__FILE__) . '/../') . '/';
		self::$site_path = self::$path . 'site/';
		self::$uri = $_SERVER['REQUEST_URI'] . '/';
		//files in site
		$files_in_site = cache_fetch('files_in_site');
		if (!$files_in_site) {
			$files_in_site = files_in_site();
			cache_store('files_in_site', $files_in_site);
		}
		self::$files_in_site = $files_in_site;
		#var_dump($files_in_site);
	}
}