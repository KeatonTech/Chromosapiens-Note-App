chrome.app.runtime.onLaunched.addListener(function() {
  chrome.app.window.create('window.html', {
    bounds: {
      width: 100,
      height: 100,
    },
    minWidth: 800,
    minHeight: 600
  });

  document.body.webkitRequestFullscreen();
});