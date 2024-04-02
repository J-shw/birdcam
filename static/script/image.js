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

async function downloadImage(imagePath) {
    try {
      const response = await fetch(`/download/image/${imagePath}`, { method: 'GET' });
  
      if (response.ok) {
        const blob = await response.blob();
  
        // Create a temporary link element
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = imageName;
  
        // Append the link to the body and click it programmatically
        document.body.appendChild(link);
        link.click();
  
        // Clean up: remove the temporary link element
        document.body.removeChild(link);
      } else {
        console.error('Download failed:', response.statusText);
      }
    } catch (error) {
      console.error('Download error:', error);
    }
}