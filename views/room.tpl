<!doctype html>
<html>
  <head>
    <title>约电影</title>

	<link type="text/css" href="css/ui-lightness/jquery-ui-1.8.13.custom.css" rel="stylesheet" />
	<link type="text/css" href="css/main.css" rel="stylesheet" />

    <script src="http://lib.sinaapp.com/js/jquery/1.7.2/jquery.min.js"></script>
	<script type="text/javascript" src="js/room.js"></script>

  </head>
  <body>
    <p>房间号: {{rid}} </p>
    <p>房间人数: {{nmember}} </p>
    <p> Connecting... </p>
	<div class="centered">
	  <div id="mainContainer" class="centered">
		<div id="controlContainer" class="ui-widget">
		  <div id="controlTable" class="ui-widget-content">
			<ul id="controlButtons">
			  <li id="buttonPlay" class="button48  ui-corner-all paused" title="Play"></li>
			  <li id="buttonStop" class="button48  ui-corner-all" title="Stop"></li>
			  <li id="buttonFull" class="button48  ui-corner-all" title="Full Screen"></li>
            </ul>

			<div id="seekContainer">
			  <div id="seekSlider"></div>
			  <div id="currentTime" class="dynamic">00:00:00</div>
			  <div id="totalTime" class="dynamic">00:00:00</div>
			</div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
