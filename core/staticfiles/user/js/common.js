var Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
});

$(function () {
    removeEmptyMenu();
    activeMenu();

    $('.datatable').each(function () {
        var pageLength = 10;
        if ($(this).is('[data-table-pagelength]')) pageLength = $(this).data('table-pagelength');

        var paging = true;
        if ($(this).is('[data-table-paging]')) paging = $(this).data('table-paging');

        var ordering = true;
        if ($(this).is('[data-table-ordering]')) ordering = $(this).data('table-ordering');

        $(this).DataTable({
            'paging': paging,
            'pageLength': pageLength,
            'lengthChange': true,
            'searching': true,
            'ordering': ordering,
            'info': true,
            'autoWidth': false,
            'language': datatable_language
        });
    });

    $('.select2').select2();
    $('.select2_autoWidth').select2({ dropdownAutoWidth: true });

    // $('.datetimepicker').datetimepicker({
    //     locale: 'vi'
    // });

    $('.datepicker').each(function() {
        var attr = $(this).attr('data-max-date');
        if (typeof attr !== typeof undefined && attr !== false) {
            var maxDate = $(this).data('max-date');
            $(this).datepicker({
                autoclose: true,
                format: 'dd/mm/yyyy',
                weekStart: 1,
                endDate: maxDate,
                language: 'vi'
            });
        }
        else {
            $(this).datepicker({
                autoclose: true,
                format: 'dd/mm/yyyy',
                weekStart: 1,
                language: 'vi'
            });
        }        
    });

    $('.monthpicker').datepicker({
        autoclose: true,
        format: 'mm/yyyy',
        weekStart: 1,
        viewMode: "months",
        minViewMode: "months",
        language: 'vi'
    });

    $('.multidate').datepicker({
        multidate: true,
        format: 'dd/mm/yyyy',
        weekStart: 1,
        language: 'vi'
    });

    // $('.timepicker').timepicker({
    //     showInputs: false,
    //     showMeridian: false
    // });
    $('.daterange_picker').daterangepicker({
        ranges: {
            'Hôm nay': [moment(), moment()],
            'Hôm qua': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            '7 gần nhất': [moment().subtract(6, 'days'), moment()],
            '30 ngày gần nhất': [moment().subtract(29, 'days'), moment()],
            'Tháng này': [moment().startOf('month'), moment().endOf('month')],
            'Tháng trước': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        //startDate: moment().subtract(29, 'days'),
        //endDate: moment(),
        language: datatable_language,
        locale: {
            format: 'DD/MM/YYYY',
            separator: " - ",
            applyLabel: "Áp dụng",
            cancelLabel: "Hủy bỏ",
            fromLabel: "Từ",
            toLabel: "Đến",
            customRangeLabel: "Tùy chọn",
            daysOfWeek: [
                "CN",
                "T2",
                "T3",
                "T4",
                "T5",
                "T6",
                "T7"
            ],
            monthNames: [
                "Tháng 1",
                "Tháng 2",
                "Tháng 3",
                "Tháng 4",
                "Tháng 5",
                "Tháng 6",
                "Tháng 7",
                "Tháng 8",
                "Tháng 9",
                "Tháng 10",
                "Tháng 11",
                "Tháng 12"
            ],
            firstDay: 1
        }
    });

    $('.input_image').each(function () {
        var input = $(this);
        var input_wrapper = input.parent();
        var input_hidden_id = input.data('hidden-id');
        var img_url = input.val();
        var img_class = input.data('img-class');
        var input_is_disabled = $(input).attr('disabled') == 'disabled';
        if (img_url.length == 0) img_url = '/static/savanna/images/default-image.jpg';

        var img_tag = '<img src="' + img_url + '" class="' + img_class + '" />';
        var btn_upload = '<button type="button" class="btn btn-default btn_upload"><i class="fa fa-upload"></i> Upload ảnh <input type="file" name="files" /></button>';

        if (input_is_disabled == false) $(btn_upload).insertAfter(input);
        $(img_tag).insertAfter(input);
        $(input).hide();

        $('button input[type="file"]', input_wrapper).change(function () {
            formdata = new FormData();
            if ($(this).prop('files').length > 0) {
                file = $(this).prop('files')[0];
                formdata.append("path", file);
                formdata.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
                $.LoadingOverlay('show');
                $.ajax({
                    type: "POST",
                    enctype: 'multipart/form-data',
                    url: upload_url,
                    data: formdata,
                    processData: false,
                    contentType: false,
                    cache: false,
                    timeout: 600000,
                    success: function (data) {
                        $(input).val(data.path);
                        $('img', input_wrapper).attr('src', data.path);
                        $('#id_' + input_hidden_id).val(data.id);
                        $.LoadingOverlay('hide');
                    },
                    error: function (e) {
                        console.log("ERROR : ", e);
                        $.LoadingOverlay('hide');
                    }
                });
            }
        });
    });

    $('.input_file').each(function () {
        var input = $(this);
        var input_wrapper = input.parent();
        var input_hidden_id = input.data('hidden-id');
        var preview_value = input.val();
        var preview_class = input.data('preview-class');
        var input_is_disabled = $(input).attr('disabled') == 'disabled';

        var icon = showIcon('file');
        var preview_div_tag = '<div class="' + preview_class + '">' + icon + preview_value + '</div>';
        var btn_upload = '<button type="button" class="btn btn-default btn_upload"><i class="fa fa-upload"></i> Upload file <input type="file" name="files" /></button>';

        if (input_is_disabled == false) $(btn_upload).insertAfter(input);
        $(preview_div_tag).insertAfter(input);
        $(input).hide();

        $('button input[type="file"]', input_wrapper).change(function () {
            formdata = new FormData();
            if ($(this).prop('files').length > 0) {
                file = $(this).prop('files')[0];
                formdata.append("path", file);
                formdata.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
                $.LoadingOverlay('show');
                $.ajax({
                    type: "POST",
                    enctype: 'multipart/form-data',
                    url: upload_url,
                    data: formdata,
                    processData: false,
                    contentType: false,
                    cache: false,
                    timeout: 600000,
                    success: function (data) {
                        var arr_path = data.path.split('/');
                        var arr_filename = arr_path[arr_path.length - 1].split('.');
                        var file_ext = arr_filename[arr_filename.length - 1];
                        var filename = arr_filename[0];
                        $(input).val(data.path);
                        $('div.' + preview_class, input_wrapper).html(showIcon(file_ext) + " " + filename);
                        $('#id_' + input_hidden_id).val(data.id);
                        $.LoadingOverlay('hide');
                    },
                    error: function (e) {
                        console.log("ERROR : ", e);
                        $.LoadingOverlay('hide');
                    }
                });
            }
        });
    });

    $('.quickSubmitForm input, .quickSubmitForm select').change(function () {
        $.LoadingOverlay('show');
        $('form.quickSubmitForm', $(this).parents()).submit();
    });

    $(document).on('click', '[data-modal-src]', function () {
        let url = $(this).data('modal-src');
        let modal_size = 'modal-lg';
        if ($(this).attr('data-modal-size')) modal_size = $(this).data('modal-size');
        showIframeModal(url, modal_size);
    });

    $('#searchSymbol').submit(function (e) {
        e.preventDefault();
        let symbol = $('input', $(this)).val().replace(/ /g,'').toUpperCase();
        let url = '/invest/stock-detail/' + symbol;
        showIframeModal(url, 'modal-xl');
        $('input', $(this)).val('');
    });
});

function showIcon(type) {
    type = type.toLowerCase();
    if (type == "pdf")
        return '<i class="fa fa-file-pdf-o" aria-hidden="true"></i>';
    else if (type == "doc" || type == "docx")
        return '<i class="fa fa-file-word-o" aria-hidden="true"></i>';
    else if (type == "xls" || type == "xlsx")
        return '<i class="fa fa-file-excel-o" aria-hidden="true"></i>';
    else if (type == "ppt" || type == "pptx")
        return '<i class="fa fa-file-powerpoint-o" aria-hidden="true"></i>';
    else if (type == "jpg" || type == "jpeg" || type == "gif" || type == "png" || type == "bmp")
        return '<i class="fa fa-file-image-o" aria-hidden="true"></i>';
    else
        return '<i class="fa fa-file" aria-hidden="true"></i>';
}

function showIframeModal(url, modal_size) {
    var iframe = '<iframe src="' + url + '"></iframe>';
    $('#iframeModal .modal-dialog').removeClass('modal-xl').removeClass('modal-lg').removeClass('modal-sm').addClass(modal_size);
    $('#iframeModal .modal-body').html(iframe);
    $('#iframeModal').modal('show');
}

function closeIframeModal() {
    $('#iframeModal').modal('hide');
}

function activeMenu() {
    var currentUrl = location.pathname;
    var menuItem = $('ul.nav-sidebar > li');

    $(menuItem).each(function (i, item) {
        if ($(item).hasClass('has-tree-view')) {
            var submenuItem = $('ul.nav-treeview > li', $(item));

            $(submenuItem).each(function (j, subitem) {
                var href = $('a', $(subitem)).attr('href');
                if (href == currentUrl) {
                    $('a', $(subitem)).addClass('active');
                    $(item).addClass('menu-open');
                }
            });
        }
        else {
            var href = $('a', $(item)).attr('href');
            if (href == currentUrl)
                $('a', $(item)).addClass('active');
        }
    });
}

function removeEmptyMenu() {
    $('ul.nav-treeview').each(function () {
        if ($('li', $(this)).length == 0) {
            $(this).parent().remove();
        }
    })
}

var datatable_language = {
    "sProcessing": "Đang xử lý...",
    "sLengthMenu": "Xem _MENU_ mục",
    "sZeroRecords": "Không tìm thấy dòng nào phù hợp",
    "sInfo": "Đang xem _START_ đến _END_ trong tổng số _TOTAL_ mục",
    "sInfoEmpty": "Đang xem 0 đến 0 trong tổng số 0 mục",
    "sInfoFiltered": "(được lọc từ _MAX_ mục)",
    "sInfoPostFix": "",
    "sSearch": "Tìm:",
    "sUrl": "",
    "oPaginate": {
        "sFirst": "Đầu",
        "sPrevious": "Trước",
        "sNext": "Tiếp",
        "sLast": "Cuối"
    }
}