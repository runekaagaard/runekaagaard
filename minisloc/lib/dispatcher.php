<?php
class frontcontroller {
	public $uri = 'rune';
	private $content_file = 'site/rune.php';
	private static $instance;

	private function  __construct() {}
	private function __clone() {}

	public static function get_instance() {
		if (!isset(self::$instance)) {
			$c = __CLASS__;
			self::$instance = new $c;
		}
		return self::$instance;
	}

	public function dispatch() {
		if (!empty($_GET['uri'])) $this->parse_request();
		echo $this->render_page();
		return;
		$config = array(
		   'indent'         => true,
		   'indent-spaces' => 4,
		   'output-xhtml'   => true,
		   'wrap'           => 200
		);
		$tidy = new tidy;
		$tidy->parseString($html, $config, 'utf8');
		echo $tidy;
	}

	private function parse_request() {
		$uri = trim(cfg::$uri, '/');
		if (is_dir("site/$uri")) {
			$this->content_file = "site/$uri/index.php";
		} else {
			$this->content_file = "site/$uri.php";
		}
		if (!file_exists($this->content_file)) redirect('404');
	}

	private function render_page() {
		return parse('tpl/page.php', array(
			'title' => to_title($this->uri),
			'content' => parse($this->content_file),
		));
	}
}