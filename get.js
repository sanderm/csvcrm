var page = require('webpage').create(),
  system = require('system'), address;

address = system.args[1];
page.scrollPosition= { top: 4000, left: 0}  
page.open(address, function(status) {
  if (status !== 'success') {
    console.log('** Error loading url.');
  } else {
    console.log(page.plaintext);
    //console.log(page.content);
  }
  phantom.exit();
});
