odoo.define('quote_print.quotation_send', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    $(document).ready(function () {
        $('#loading').hide();
        $('.send_by_mail').on('click', function(e){
            $('#loading').show();
            var quote = e.target.value;
            if (quote) {
                ajax.jsonRpc('/online_quote/send_by_mail', 'call', {
                    'order_id': quote,
                }).then(function (data) {
                    $('#loading').hide();
                    alert('Mail send Successfully!');
                });
            }
        });
    });
});