function createRadioOption(inputId, data, buttonId) {
    $(`${inputId}`).append(
            '<div class="form-check">' +
            `<input class="form-check-input" type="radio" name="searchResult" id="flexRadioDefault${buttonId}">` +
            '<label class="form-check-label" for="flexRadioDefault${buttonId}">' +
            `${data.query}` +
            '</label>' +
            '</div>'
    );
};

$(document).ready(function () {

    var buttonClicked = 0;
    $('.search').click(function (e) {
        buttonClicked++;
        // get address input value
        var addressValue = $(`#schoolAddress${e.target.dataset.id}`).val();

        // send to python for processing
        $.ajax({
            url: '/owners/geocode/',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({"query": addressValue}),
            success: function (result) {
                createRadioOption(`#searchResult${e.target.dataset.id}`, result, buttonClicked);
            },
            error: function (error) {}
        });
    });


});