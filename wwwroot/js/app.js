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
        if(Http.readyState === 4 && Http.status === 200){ 
            setLastColor(red,green,blue);
        }    
    }
    if(addButton){
        addColorButton(red,green,blue);
    }
}

function addColorButton(red,green,blue){
    var colorOutput = document.querySelector("#selectedColors");
    colorOutput.innerHTML = `<a class="waves-effect waves-light btn" style="margin:4px; background-color: rgb(${red},${green},${blue});" onClick="setColor(${red},${green},${blue})" onContextMenu="deleteColor(${red},${green},${blue})">&nbsp;&nbsp;</a>${colorOutput.innerHTML}`;
}

function setLastColor(red,green,blue){
    var colorOutput = document.querySelector("#last-used-color");
    colorOutput.innerHTML = `<a class="waves-effect waves-light btn" style="margin:4px; background-color: rgb(${red},${green},${blue});" href="#">&nbsp;&nbsp;</a>`;
}

function loadPreviousColors(){
    const Http = new XMLHttpRequest();
    const url=`api/getUsedColors`;

    Http.open("GET", url);
    Http.send();
    
    Http.onreadystatechange=(e)=>{
        if(Http.readyState === 4 && Http.status === 200){
            var colors = JSON.parse(Http.responseText);
            if(colors.length > 0){
                setLastColor(colors[0][0],colors[0][1],colors[0][2]);
            }
            colors.reverse().forEach(
                color => {
                    addColorButton(color[0],color[1],color[2]);
                }
            )
        }
    }
}

function deleteColor(red, green, blue){
    alert('Delete?');
}