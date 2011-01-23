<?php
echo parse('tpl/page_list_simple.php', array(
	'pages' => cfg::$files_in_site['admin'],
));