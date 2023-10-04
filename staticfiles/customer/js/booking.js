uniqueVenueCity()
function uniqueVenueCity() {
    let cityArray = [];
    document.querySelectorAll('.venue-city')
        .forEach((city) => {
            cityArray.push(city.innerText);
            city.style.display = 'none'
        });
    cityArray.forEach((city) => {
        document.querySelector(`.venue-${city}`)
            .style.display = 'inline';
    })
};


uniqueVendorCity()
function uniqueVendorCity() {
    let cityArray = [];
    document.querySelectorAll('.vendor-city')
        .forEach((city) => {
            cityArray.push(city.innerText);
            city.style.display = 'none'
        });

    cityArray.forEach((city) => {
        document.querySelector(`.vendor-${city}`)
            .style.display = 'inline';
    })
};


console.log("wofking")