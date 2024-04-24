function loadable(){
    data()
}

function takePhoto(){ 
    let btn = document.getElementById("takePhotoBtn");
    btn.classList.remove("buttonComplete");
    btn.classList.remove("buttonOff");
    btn.classList.remove("buttonFail");
    btn.classList.add("buttonWait");
    btn.innerHTML = "Wait";

    fetch('/manual/photo')

    .then(response => response.json())
    .then(data=>{
        btn.classList.remove("buttonWait");

        if(data.status != 200){
            btn.classList.add("buttonFail");
            btn.innerHTML = "Failed";
            console.log("Manual photo error - " + data.error + " | " + data.status);
            setTimeout(() => {
                resetBtn(btn, 'Take photo')
              }, 1000); 
        }else{
            loadImages();
            btn.classList.add("buttonComplete");
            btn.innerHTML = "Complete";
            setTimeout(() => {
                resetBtn(btn, 'Take photo')
              }, 1000);
        }
    });
}

function start(){
    let startBtn = document.getElementById("startBtn");
    startBtn.classList.remove("buttonComplete");
    startBtn.classList.remove("buttonOff");
    startBtn.classList.remove("buttonFail");
    startBtn.classList.add("buttonWait");
    startBtn.innerHTML = "Wait";

    fetch('/start')

    .then(response => response.json())
    .then(data=>{
    
        if(data.status != 200){
            startBtn.classList.remove("buttonComplete");
            startBtn.classList.remove("buttonWait");
            startBtn.classList.remove("buttonOff");
            startBtn.classList.add("buttonFail");
            startBtn.innerHTML = "Failed";
            console.log("Start error - " + data.data + " | " + data.status);
            setTimeout(() => {
                resetBtn(startBtn, 'Start')
              }, 1000); 
        }else{
            startBtn.classList.remove("buttonOff");
            startBtn.classList.remove("buttonWait");
            startBtn.classList.remove("buttonFail");
            startBtn.classList.add("buttonComplete");
            startBtn.innerHTML = "Running";
            setTimeout(() => {
                resetBtn(startBtn, 'Start')
              }, 1000); 
        }
    })
}

function end(){
    let endBtn = document.getElementById("endBtn");
    endBtn.classList.remove("buttonOff");
    endBtn.classList.remove("buttonComplete");
    endBtn.classList.remove("buttonFail");
    endBtn.classList.add("buttonWait");
    endBtn.innerHTML = "Wait";
    fetch('/end')

    .then(response => response.json())
    .then(data=>{
    
        if(data.status != 200){
            endBtn.classList.remove("buttonOff");
            endBtn.classList.remove("buttonComplete");
            endBtn.classList.remove("buttonWait");
            endBtn.classList.add("buttonFail");
            endBtn.innerHTML = "Failed";
            console.log("End error - " + data.data + " | " + data.status);
            setTimeout(() => {
                resetBtn(startBtn, 'Stop')
              }, 1000);              
        }else{
            endBtn.classList.remove("buttonFail");
            endBtn.classList.remove("buttonOff");
            endBtn.classList.remove("buttonWait");
            endBtn.classList.add("buttonComplete");
            endBtn.innerHTML = "Stopped";
            setTimeout(() => {
                resetBtn(startBtn, 'Stop')
              }, 1000); 
        }
    })
}

function resetBtn(btn, text){
    btn.innerHTML = text;
    btn.classList.remove("buttonFail");
    btn.classList.remove("buttonComplete");
    btn.classList.remove("buttonWait");
    btn.classList.add("buttonOff");
}

function showHiResImage(file){
    filename = "../static/data/photos/HR/" + file
    var hiresDiv = document.createElement('div');
    hiresDiv.style.position = 'fixed';
    hiresDiv.style.top = '0';
    hiresDiv.style.left = '0';
    hiresDiv.style.width = '100%';
    hiresDiv.style.height = '100%';
    hiresDiv.style.zIndex = '9999';
    hiresDiv.style.backgroundImage = 'url(' + filename + ')';
    hiresDiv.style.backgroundSize = 'contain';
    hiresDiv.style.backgroundRepeat = 'no-repeat';
    hiresDiv.style.backgroundPosition = 'center';

    document.body.appendChild(hiresDiv);
}

function display_images(folders_dict) {
    console.log(folders_dict)
    const filePath = "../static/data/photos/LR/";
    const parentDiv = document.getElementById("viewer")
    parentDiv.innerHTML = '';
    
    folders_dict.forEach(fileData => {
        var div = document.createElement("div");
        var para = document.createElement("p");

        let folder = fileData['folder']
        let newFilePath = filePath + folder + "/";

        para.classList.add("header");
        para.innerText = folder;
        div.appendChild(para);

        fileData['files'].forEach(file => {
            imgSource = newFilePath + file;
            imagePath =   folder + "/" + file;
            var linkElement = document.createElement('a');
            var imgTag = document.createElement("img");

            linkElement.href = "/display_image/"+imagePath;
            imgTag.src = imgSource;
            imgTag.loading = 'lazy';

            linkElement.appendChild(imgTag);
            div.appendChild(linkElement);
        });
        parentDiv.appendChild(div);
    });
}

function loadImages(){
    fetch('/lowResImg')

    .then(response => response.json())
    .then(data=>{
    
        if(data.status != 200){
            console.log("Get status error - " + data.data + " | " + data.status);
        }else{
            folders_dict = data.data
            display_images(folders_dict)
        }
    })
};

function data(){
    const cpuTemp = document.getElementById("cpuTemp");
    const cpuFreq = document.getElementById("cpuFreq");
    const storage = document.getElementById("storage");
    const latestPhoto = document.getElementById("latestPhoto");


    fetch('/data')

    .then(response => response.json())
    .then(data=>{
    
        if(data.status != 200){
            console.log("Get status error - " + data.data + " | " + data.status);
        }else{
            // deviceData = [cpuTemp,cpuFreq,totalDisk,usedDisk]
            let lastPhoto = data.data[0];
            let deviceData = data.data[1];

            if (lastPhoto != null){
                latestPhoto.innerHTML = "Recent - " + lastPhoto;
            } else {
                latestPhoto.innerHTML = "None" 
            }
            cpuTemp.innerHTML = "CPU temp - " + deviceData[0] + "°C";
            cpuFreq.innerHTML = "CPU freq - " + deviceData[1] + "MHz";
            storage.innerHTML = "Storage - " + deviceData[3] + "/" + deviceData[2] + "GB";

        }
    })

}