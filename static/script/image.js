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