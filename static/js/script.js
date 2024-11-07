// static/js/script.js
function toggleAppliance(id) {
    $.ajax({
        url: "/toggle",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ id: id }),
        success: function(data) {
            let button = $(`[onclick="toggleAppliance('${id}')"]`);
            let img = button.siblings("img.appliance-img");

            // Toggle button style and text
            button.toggleClass('btn-on btn-off');
            button.text(data.status ? 'Turn Off' : 'Turn On');

            // Set image source based on appliance status
            let imgSrc = data.status 
                ? (data.name.includes('Light') ? '/static/images/light_on.png' : '/static/images/fan_on.gif') 
                : (data.name.includes('Light') ? '/static/images/light_off.png' : '/static/images/fan_off.png');
            img.attr("src", imgSrc);
        }
    });
}

