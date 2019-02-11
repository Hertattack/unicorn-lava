var demoColorPicker = new iro.ColorPicker("#color-picker-container");
var autoUpdate = true;

demoColorPicker.on("input:end", function onInputStart() {
    if(autoUpdate === true){
        setColorFromPicker();
    }
});

function setAutoUpdate(checkBox){
    autoUpdate = checkBox.checked === true;
}

function setColorFromPicker(){
    var rgb = demoColorPicker.color.rgb;
    setColor(rgb.r,rgb.g, rgb.b, true);
}

function setColor(red, green, blue, addButton){
    const Http = new XMLHttpRequest();
    const url=`api/setColor?red=${red}&green=${green}&blue=${blue}`;

    Http.open("GET", url);
    Http.send();
    
    Http.onreadystatechange=(e)=>{
        console.log(Http.responseText)
    }

    if(addButton===true){
        var colorOutput = document.querySelector("#selectedColors");
        colorOutput.innerHTML = `<a class="waves-effect waves-light btn" style="margin:4px; background-color: rgb(${red},${green},${blue});" onClick="setColor(${red},${green},${blue})">&nbsp;&nbsp;</a>${colorOutput.innerHTML}`;
    }
}