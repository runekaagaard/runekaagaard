<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
		<base href="<?=cfg::$base_url?>" />
		<title><?=$title?></title>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<style type="text/css" media="all">
			@import url("/css/reset.css");
			@import url("/css/base.css");
			@import url("/css/rune.css");
		</style>

	</head>
	<body>
		<div class="logo">
			 <div class="txt">
				<h1><a href="http://www.techfounder.net/">rune - </a>
					<span>blog on music, ideas, code and moonlight</span>
				</h1>
				
			</div>
		</div>

		<?=parse('tpl/menu.php')?>
		
    <div id="content">
      <h1 class="first"><?=$title?></h1>
      <?=$content?>
    </div>

	<?=parse('tpl/w3c.php')?>
	
	</body>
</html>