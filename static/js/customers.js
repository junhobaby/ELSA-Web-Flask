$(document).ready(function () {
    var table = $('#customers').DataTable({
        columnDefs: [
            {
                targets: -1,
                data: null,
                defaultContent: '<button class="btn btn-primary btn-sm">Update</button>',
            },
        ],
    });

    $('#customers tbody').on('click', 'button', function () {
        var data = table.row($(this).parents('tr')).data();
        window.location.href = `/customers/${data[0]}`;
        return false;
    });
});
