<?php
//help me
error_reporting(E_ALL | E_STRICT);

//globals
define('RUNE_PATH', realpath(dirname(__FILE__)) . '/');
define('RUNE_SITE_PATH', RUNE_PATH . 'site/');
define('RUNE_URI', 'http://runekaagaard.com/');

//add include path
set_include_path(RUNE_PATH . PATH_SEPARATOR . get_include_path());

//requires
$lib_files = glob('lib/*.php');
foreach ($lib_files as $lib_file) require $lib_file;

//config
new cfg;

//cache
if (cfg::$cache) apc_clear_cache();

//dispatch
$d = dispatcher::get_instance();
$d->dispatch();