<?
foreach($pages as $page):
extract($page);
if ($basename == 'index.php') continue;
?>
	<h2><?=$title?></h2>
	<?=$teaser?>
	<a href="<?=$url?>">Read More</a>
<?endforeach?>