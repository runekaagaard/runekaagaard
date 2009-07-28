<?php
//help me
error_reporting(E_ALL | E_STRICT);

//requires
$lib_files = glob('lib/*.php');
foreach ($lib_files as $lib_file) require $lib_file;

//config
cfg::set_variables();

//cache
if (cfg::$cache) apc_clear_cache();

//dispatch
frontcontroller::get_instance()->dispatch();