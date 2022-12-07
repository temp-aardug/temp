function product_snippet(){
    var curr_page = $(document);
    url = curr_page.attr('location').pathname;
    if (url.indexOf('/shop/') == 0){
        var product_name = url.split('/')[2];
        var product = product_name.split('-');
        var product_id = product[product.length - 1];
        $.ajax({
            url: "/product/snippet/dynamic_value",
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({'jsonrpc': "2.0", 'method': "call", "params": {'product_id': parseInt(product_id)} }),
            async: false,
            success: function (result) {
                var record = result.result;
                if($('#xaa_ec_logo').length && record.xaa_ec_logo != false){
                    $('#xaa_ec_logo')[0].src='/web/image/product.template/'+ record.product_id +'/xaa_ec_logo';
                }
                if($('#xaa_ec_product_image').length && record.xaa_ec_product_image != false){
                    $('#xaa_ec_product_image')[0].src='/web/image/product.template/'+ record.product_id +'/xaa_ec_product_image';
                }
                if($('#xaa_ec_product_image_opt').length && record.xaa_ec_product_image_opt != false){
                    $('#xaa_ec_product_image_opt')[0].src='/web/image/product.template/'+ record.product_id +'/xaa_ec_product_image_opt';
                }
                if($('#xaa_ec_name').length && record.xaa_ec_name != false){
                    $('#xaa_ec_name').replaceWith('<p style="font-size: 20px;"><b>'+ record.xaa_ec_name +'</b></p>');
                }
                if($('#xaa_ec_point1_icon').length && record.xaa_ec_point1_icon != false){
                    $('#xaa_ec_point1_icon')[0].src='/web/image/product.template/'+ record.product_id +'/xaa_ec_point1_icon';
                }
                if($('#xaa_ec_point1_title').length && record.xaa_ec_point1_title != false){
                    $('#xaa_ec_point1_title').replaceWith('<p style="margin: auto; font-size: 16px;"><b>'+ record.xaa_ec_point1_title +'</b></p>');
                }
                if($('#xaa_ec_point1_desc').length && record.xaa_ec_point1_desc != false){
                    $('#xaa_ec_point1_desc').replaceWith('<p style="font-size: 14px;">'+ record.xaa_ec_point1_desc +'</p>');
                }
                if($('#xaa_ec_point2_icon').length && record.xaa_ec_point2_icon != false){
                    $('#xaa_ec_point2_icon')[0].src='/web/image/product.template/'+ record.product_id +'/xaa_ec_point2_icon';
                }
                if($('#xaa_ec_point2_title').length && record.xaa_ec_point2_title != false){
                    $('#xaa_ec_point2_title').replaceWith('<p style="margin: auto; font-size: 16px;"><b>'+ record.xaa_ec_point2_title +'</b></p>');
                }
                if($('#xaa_ec_point2_desc').length && record.xaa_ec_point2_desc != false){
                    $('#xaa_ec_point2_desc').replaceWith('<p style="font-size: 14px;">'+ record.xaa_ec_point2_desc +'</p>');
                }
                if($('#xaa_ec_point3_icon').length && record.xaa_ec_point3_icon != false){
                    $('#xaa_ec_point3_icon')[0].src='/web/image/product.template/'+ record.product_id +'/xaa_ec_point3_icon';
                }
                if($('#xaa_ec_point3_title').length && record.xaa_ec_point3_title != false){
                    $('#xaa_ec_point3_title').replaceWith('<p style="margin: auto; font-size: 16px;"><b>'+ record.xaa_ec_point3_title +'</b></p>');
                }
                if($('#xaa_ec_point3_desc').length && record.xaa_ec_point3_desc != false){
                    $('#xaa_ec_point3_desc').replaceWith('<p style="font-size: 14px;">'+ record.xaa_ec_point3_desc +'</p>');
                }
                if($('#xaa_ec_point4_icon').length && record.xaa_ec_point4_icon != false){
                    $('#xaa_ec_point4_icon')[0].src='/web/image/product.template/'+ record.product_id +'/xaa_ec_point4_icon';
                }
                if($('#xaa_ec_point4_title').length && record.xaa_ec_point4_title != false){
                    $('#xaa_ec_point4_title').replaceWith('<p style="margin: auto; font-size: 16px;"><b>'+ record.xaa_ec_point4_title +'</b></p>');
                }
                if($('#xaa_ec_point4_desc').length && record.xaa_ec_point4_desc != false){
                    $('#xaa_ec_point4_desc').replaceWith('<p style="font-size: 14px;">'+ record.xaa_ec_point4_desc +'</p>');
                }
                if($('#xaa_ec_point5_icon').length && record.xaa_ec_point5_icon != false){
                    $('#xaa_ec_point5_icon')[0].src='/web/image/product.template/'+ record.product_id +'/xaa_ec_point5_icon';
                }
                if($('#xaa_ec_point5_title').length && record.xaa_ec_point5_title != false){
                    $('#xaa_ec_point5_title').replaceWith('<p style="margin: auto; font-size: 16px;"><b>'+ record.xaa_ec_point5_title +'</b></p>');
                }
                if($('#xaa_ec_point5_desc').length && record.xaa_ec_point5_desc != false){
                    $('#xaa_ec_point5_desc').replaceWith('<p style="font-size: 14px;">'+ record.xaa_ec_point5_desc +'</p>');
                }
                if(!record.xaa_ec_point4_icon && !record.xaa_ec_point4_title && !record.xaa_ec_point4_desc){
                    $('#xaa_ec_point4_icon').remove();
                    $('#xaa_ec_point4_title').remove();
                    $('#xaa_ec_point4_desc').remove();
                }
                if(!record.xaa_ec_point5_icon && !record.xaa_ec_point5_title && !record.xaa_ec_point5_desc){
                    $('#xaa_ec_point5_icon').remove();
                    $('#xaa_ec_point5_title').remove();
                    $('#xaa_ec_point5_desc').remove();
                }
                if(!record.xaa_ec_product_image_opt){
                    $('#xaa_ec_product_image_opt').remove();
                }
            }
        });
    }
}
