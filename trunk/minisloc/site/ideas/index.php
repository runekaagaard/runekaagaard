<p>I have a lot of ideas!!! Here is a list:</p>
<?
echo parse('tpl/page_list.php', array('pages' => cfg::$files_in_site['ideas']));

return yaml('
tags: [about, Rune, Kaagaard, cv, details]
created: 2009-07-23
');