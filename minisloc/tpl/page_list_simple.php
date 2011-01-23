<ul>
<?
foreach($pages as $page):
extract($page);
if ($basename == 'index.php') continue;
?>
	<li><a href="<?=$url?>"><?=$title?></a>
<?endforeach?>
</ul>