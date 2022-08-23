function createOption(inputId, data, buttonId, schoolId) {
    console.log(data);
    var result = data.data;
    $(`${inputId}`).append(
        '<li class="list-group-item">' +
        `<input class="form-check-input me-1" type="checkbox" value="" id="address${schoolId}" data-school-id=${schoolId} data-address-id=${data.address_pk}>` +
        `<label class="form-check-label" for="address${schoolId}">${result.formatted_address}</label>` +
        '</li>'
    );
};

function createPayload(ownerId, checkboxesData) {
    console.log(checkboxesData);
    var schoolData = Array.prototype.map.call(checkboxesData, (element) => {
        return {"school_id": element.dataset.schoolId, "raw_address_id": element.dataset.addressId}
    })
    var payload = {"owner_id": ownerId, "schools": schoolData}
    return payload
};

$(document).ready(function () {

    var buttonClicked = 0;
    var schoolId = null;
    var addressValue = null;

    $('.search').click(function (e) {
        buttonClicked++;

        // get address input value
        schoolId=e.target.dataset.id;
        addressValue = $(`#schoolAddress${schoolId}`).val();

        // send to python for processing
        $.ajax({
            url: '/owners/geocode/',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({"query": addressValue}),
            success: function (result) {
                schoolId = e.target.dataset.id;
                createOption(`#searchResult${schoolId}`, result, buttonClicked, schoolId);
            },
            error: function (error) {}
        });
    });

    // handle submit
    $("#updateSchool").submit(function(e) {
        e.preventDefault();

        // pull selected checkboxes
        var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
        var ownerId = $('#ownerId').val();

        // payload: {"owner_id": 1, schools: [{"school_id": 1, "raw_address_id": 1}, {"school_id": 2, "raw_address_id": 2}]}
        // send to python for processing
        var payload = createPayload(ownerId, checkboxes)
        $.ajax({
            url: `/owners/${ownerId}/schools/`,
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(payload),
            success: function () {
                alert('Update complete!');
            },
            error: function (error) {
                console.log(error);
            }
        })
    });

});