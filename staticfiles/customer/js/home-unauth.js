const unauthNavbar = document.querySelector('.unauth-navbar')
unauthNavbar.classList.remove('unauth-navbar')

const unauthLogo2 = document.querySelector('.unauth-logo-2');
unauthLogo2.classList.remove('unauth-logo-2')

const unauthDefaultProfile2 = document.querySelector('.unauth-default-profile-2');
unauthDefaultProfile2.classList.remove('unauth-default-profile-2')

const listYourBusiness = document.querySelector('.list-your-business-2');
listYourBusiness.classList.remove('list-your-business-2')


window.addEventListener('scroll',()=>{    
    if(window.scrollY >=70){
        unauthNavbar.classList.add('unauth-navbar')
        unauthLogo2.classList.add('unauth-logo-2')                
        unauthDefaultProfile2.classList.add('unauth-default-profile-2')
        listYourBusiness.classList.add('list-your-business-2')

    } else{
        unauthNavbar.classList.remove('unauth-navbar')
        unauthLogo2.classList.remove('unauth-logo-2')                
        unauthDefaultProfile2.classList.remove('unauth-default-profile-2')
        listYourBusiness.classList.remove('list-your-business-2')
    }
})



