<?
$items = array('rune', 'ideas', 'programming', 'mastering', 'projects', 'admin');
?>
<div id="menu">
	<ul>
		<?foreach($items as $item):?>
			<li<?=strpos(cfg::$uri, $item) === 1 ? ' class="active"' : ''?>>
				<a href="<?=$item?>"><?=to_title($item)?></a>
			</li>
		<?endforeach?>
	</ul>

	<?=clear()?>
</div>
