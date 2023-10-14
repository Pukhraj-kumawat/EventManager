
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("profile-form");
    const submitButton = document.getElementById("remove-profile");
    const buttonClicked = document.getElementById('button-clicked')
    

    submitButton.addEventListener("click", function () {
        // Manually trigger the form submission
        buttonClicked.value = 'clicked';        
        form.submit();   
             
    });

});

if (document.getElementById('default-profile').src === 'staticfiles/images/No%20profile.jpeg'){

    document.getElementById('remove-profile').style.visibility = 'hidden';


}