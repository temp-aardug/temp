odoo.define('odoo_mobile_timesheet.website_portal', function(require) {
    'use strict';
    require('web.dom_ready');
    

    var publicWidget = require('web.public.widget');

publicWidget.registry.MobileTimesheet = publicWidget.Widget.extend({
    selector: '.o_timesheet_probc',
    events: {
        "change select[name='project_id']" : "_onChangeProject",
        "change input-search": '_onChangeInputSearch',
    },
    start: function(ev){
        this._apply_custom_timesheet_css()
        this.state_options = $("select[name='task_id']:enabled option:not(:first)");
        this._onChangeProject()
    },
    _apply_custom_timesheet_css : function(ev){
        if ($("#portal_timesheet").html() == "True"){
            $("#footer").hide()
            $("nav.navbar-expand-lg").removeClass('navbar-light bg-light');
            $("nav.navbar-expand-lg").css({'background-color': "#875A7B"})
            var nav_length = $(".navbar-nav > li > a").length
            $("button.navbar-toggler").find("span.navbar-toggler-icon").html('<i class="fa fa-navicon"></i>').css({'color':"white"})
            for (var i=0; i<nav_length; i++){
                $(".navbar-nav > li > a")[i]['style']['color'] = "white"
            }
            var textarea_length = $("textarea").length
            for (var i=0; i<textarea_length; i++){
                $("textarea")[i]['style']['borderColor'] = "#27BB64"
            }
            $("textarea").focus(function(){
                $(this)[0]['style']['borderColor'] = ""
            });
            $("textarea").focusout(function(){
                $(this)[0]['style']['borderColor'] = "#27BB64"
            });

            var select_length = $("select").length
            for (var i=0; i<select_length; i++){
                $("select")[i]['style']['borderColor'] = "#27BB64"
            }
            $("select").focus(function(){
                $(this)[0]['style']['borderColor'] = ""
            });
            $("select").focusout(function(){
                $(this)[0]['style']['borderColor'] = "#27BB64"
            });
            var input_length = $("input").length
            for (var i=0; i<input_length; i++){
                $("input")[i]['style']['borderColor'] = "#27BB64"
            }
            $("input").focus(function(){
                $(this)[0]['style']['borderColor'] = ""
            });
            $("input").focusout(function(){
                $(this)[0]['style']['borderColor'] = "#27BB64"
            });
        }
    },
    _onChangeProject : function(ev){
        var project_id = this.$('select[name="project_id"]');
        var select = $("select[name='task_id']");
        this.state_options.detach();
        var displayed_state = this.state_options.filter("[data-project_id="+($(project_id).val() || 0)+"]");
        var nb = displayed_state.appendTo(select).length
        select.parent().toggle(nb>=0);
    },
    _onChangeInputSearch: function(ev){
        var input, filter, table, tr, td, i, date, name, project;
          input = document.getElementById("myInput");
          var vals = this.value;
          filter = input.value.toUpperCase();
          table = document.getElementById("timesheet_table");
          tr = table.getElementsByTagName("tr");
          for (i = 0; i < tr.length; i++) {
            date = tr[i].getElementsByTagName("td")[0];
            name = tr[i].getElementsByTagName("td")[1];
            if (date) {
              if (date.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
              } else if (name) {
                  if (name.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                  } else {
                    tr[i].style.display = "none";
                  }
            }
          }   
        }
    },
    
});


//        var state_options = $("select[name='task_id']:enabled option:not(:first)");
//        $('.o_website_portal_details').on('change', "select[name='project_id']", function () {
//            var select = $("select[name='task_id']");
//            state_options.detach();
//            var displayed_state = state_options.filter("[data-project_id="+($(this).val() || 0)+"]");
////            var nb = displayed_state.appendTo(select).show().size();
//            var nb = displayed_state.appendTo(select).length
//            select.parent().toggle(nb>=0);
//        });
//        $('.o_website_portal_details').find("select[name='project_id']").change();

//        });
//        $(".input-search input.myInputsearch").on("change", function () {
//          var input, filter, table, tr, td, i, date, name, project;
//          input = document.getElementById("myInput");
//          var vals = this.value;
//          filter = input.value.toUpperCase();
//          table = document.getElementById("timesheet_table");
//          tr = table.getElementsByTagName("tr");
//          for (i = 0; i < tr.length; i++) {
//            date = tr[i].getElementsByTagName("td")[0];
//            name = tr[i].getElementsByTagName("td")[1];
//            if (date) {
//              if (date.innerHTML.toUpperCase().indexOf(filter) > -1) {
//                tr[i].style.display = "";
//              } else if (name) {
//                  if (name.innerHTML.toUpperCase().indexOf(filter) > -1) {
//                    tr[i].style.display = "";
//                  } else {
//                    tr[i].style.display = "none";
//                  }
//            }
//          }   
//        }
//    });

//    if(!$('.o_website_portal_details').length) {
//        return $.Deferred().reject("DOM doesn't contain '.o_website_portal_details'");
//    }

    
});
