function deleteImage(imagePath){
    if (window.confirm("Are you sure you want to delete this item?")) {

        fetch('/delete_image/'+imagePath)
        
        .then(response => response.json())
        .then(data=>{
            
            if(data.status != 200){
                alert("Item failed to deleted");
                console.log("Get status error - " + data.data + " | " + data.status);
            }else{
                alert("Item deleted");
                window.location.href = "/";
            }
        })
      }

}

function goHome() {
    window.location.href = '/';
}

async function downloadImage(imagePath, fileName) {
  console.log(imagePath);
  console.log(fileName);

  // <a href="/images/myw3schoolsimage.jpg" download> 
  let aTag = document.createElement('a');

  aTag.href = `static/${imagePath}`;
  aTag.download = fileName;
  document.body.appendChild(aTag);

  aTag.click();

  document.body.removeChild(aTag);
}