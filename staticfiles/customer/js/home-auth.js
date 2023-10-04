const customerNavbar = document.querySelector('.customer-navbar')
customerNavbar.classList.remove('customer-navbar')

const Logo2 = document.querySelector('.logo-2');
Logo2.classList.remove('logo-2')

const DefaultProfile2 = document.querySelector('.default-profile-2');
DefaultProfile2.classList.remove('default-profile-2')

const welcomeMessage2 = document.querySelector('.welcome-message-2');
welcomeMessage2.classList.remove('welcome-message-2')


window.addEventListener('scroll',()=>{    
    if(window.scrollY >=70){
        customerNavbar.classList.add('customer-navbar')
        Logo2.classList.add('logo-2')                
        DefaultProfile2.classList.add('default-profile-2')
        welcomeMessage2.classList.add('welcome-message-2')

    } else{
        customerNavbar.classList.remove('customer-navbar')
        Logo2.classList.remove('logo-2')                
        DefaultProfile2.classList.remove('default-profile-2')
        welcomeMessage2.classList.remove('welcome-message-2')
    }
})