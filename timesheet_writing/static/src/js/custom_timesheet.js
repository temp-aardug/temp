odoo.define('timesheet_writing.custom_timesheet', function (require) {
'use strict';

    var session = require('web.session');
    var rpc = require('web.rpc')

    $(document).ready(function () {
         $("select[name='project_id']").on('change',function(e){
            var project = $("select[name='project_id']").val()
            if (project){
                rpc.query({
                model: 'account.analytic.line',
                method: 'get_default_task',
                args: [[session.user_id], project],
            })
                .then(function (default_task) {
                if (default_task) {
                    $("select[name='task_id']")[0].value = default_task
                }
            })
            }
        });

        $('input[name="start_date"], select[name="work_type"], select[name="employee_id"], input[name="quantity"]').on('change', function (e) {
            var start_date = $('input[name="start_date"]').val() || '';
            var duration = $('input[name="quantity"]').val() || '';
            var work_type = $('select[name="work_type"]')[0];
            if (work_type){
                work_type = work_type.selectedOptions[0].text;
            }
            else{
                work_type = '';
            }
            rpc.query({model: 'res.users', method: 'read', args: [[session.user_id], ['name']]})
                .then(function (backend_result) {
                    if ($('select[name="employee_id"]')[0]){
                        var employee_id = $('select[name="employee_id"]')[0].selectedOptions[0].text;
                    }
                    else {
                        var employee_id = backend_result[0].name;
                    }
                    var desc = $('textarea[name="description"]')[0]
                    if (desc) {
                        $('textarea[name="description"]')[0].value = work_type + ' - ' + employee_id + ' - ' + start_date.split('-').reverse().join('/') + ' ' +' ' + 'Duration' + ' ' + duration;
                    }
                });
        });
    });
});
