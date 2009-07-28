<?php
function remove_text(&$cfg) {
	foreach ($cfg as $key => &$val) {
		if (is_array($val) && empty($val['path'])) remove_text($val);
		else unset($val['content'], $val['teaser']);
	}
}
$cfg = get_class_vars('cfg');
remove_text($cfg['files_in_site']);
?>
<p>
	<pre>
	<?=htmlentities(print_r($cfg, true))?>
	</pre>
</p>