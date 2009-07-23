<?
$items = array('rune', 'ideas', 'programming', 'mastering', 'projects');
?>
<div id="menu">
	<ul>
		<?foreach($items as $item):?>
			<li<?=strpos(uri(), $item) === 0 ? ' class="active"' : ''?>>
				<a href="<?=$item?>"><?=to_title($item)?></a>
			</li>
		<?endforeach?>
	</ul>
</div>
