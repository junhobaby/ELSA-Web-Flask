function createOption(inputId, data, buttonId, schoolId) {
    console.log(data);
    var results = data.data;

    console.log('printing results');
    console.log(results);

    for (let i=0; i < results.length; i++) {

        console.log(results[i]);

        $(`${inputId}`).append(
            '<li class="list-group-item">' +
            `<input class="form-check-input me-1" type="checkbox" value="" id="address${schoolId}" data-school-id=schoolId data-address-id=${results[i].address_pk}>` +
            `<label class="form-check-label" for="address${schoolId}">${results[i].label}</label>` +
            '</li>'
        );
    }
};

$(document).ready(function () {

    var buttonClicked = 0;
    var schoolId = null;

    $('.search').click(function (e) {
        buttonClicked++;

        // get address input value
        var addressValue = $(`#schoolAddress${schoolId}`).val();
        schoolId = e.target.dataset.id;

        // send to python for processing
        $.ajax({
            url: '/owners/geocode/',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({"query": addressValue}),
            success: function (result) {
                createOption(`#searchResult${e.target.dataset.id}`, result, buttonClicked, schoolId);
            },
            error: function (error) {}
        });
    });

    // handle submit
    $("#updateSchool").submit(function(e) {
        // pull selected checkboxes
        var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')

        console.log(checkboxes);
        e.preventDefault();
    });

});