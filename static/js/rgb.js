var bodyheight
var hex

// Instantiates iro.js
var colorPicker = new iro.ColorPicker('#picker');

// Sets parameters upon full page load
$(document).ready(function() {
    setBodyHeight();
    setBodyColor();
});

// Sets color picker to value from flask server
function setInitialHexValue(initalHexValue) {
    colorPicker.color.hexString = initalHexValue;
    $("body").css("background-color",initalHexValue)
}

// Listener for colorpicker - body background-color is called when color-picker color is changed
colorPicker.on('color:change', function(color) {
    setBodyColor();
    submitColor();
});

// Sets body background color
function setBodyColor() {
    hex = colorPicker.color.hexString;
    $("body").css("background-color",hex)
}

// Fills space between header and footer
function setBodyHeight() {
    bodyheight = ($(window).height() - ( $(".custom-nav").outerHeight(true) + $(".footer-box").outerHeight(true) ));
    $(".main-box").css("min-height",bodyheight)
}

// Changes parameters when viewport changes size
$(window).resize(function(){
    setBodyHeight();
})

// Displays current color value in hex
function colorValueInHex() {
    hex = colorPicker.color.hexString;
    console.log(hex);
}

// Submits colour to flask server
function submitColor() {
    $.post("/", {hexValue: hex});
}