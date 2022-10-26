var breakPoint1 = 768,
    breakPoint2 = 1170,
    breakPoint3 = 1600;

var InteractiveMap = function () {

}

InteractiveMap.prototype.init = function () {
    var _this = this;
    _this._prepareMapHover();
}

InteractiveMap.prototype._changeGraphImage = function (eventType, data, parent) {
    let customdata = data.points[0].customdata;
    for (let key in customdata) {
        parent.find('[data-field=' + key + ']').html(customdata[key]);
    }
    let graph_img = parent.find('.map-block__graph-' + eventType),
        graph_img_url = graph_img.attr('data-base-url') + '/' + customdata['station_id'] + '.svg';
    graph_img.attr('src', graph_img_url);
}

InteractiveMap.prototype._prepareMapHover = function () {
    let _this = this;
    jQuery('.map-block__iframe').each(function () {
        let id = jQuery(this).attr('data-id'),
            iframe = jQuery('#map-block-' + id).find('iframe'),
            parent = jQuery(this).parents('.map-block__parent');

        iframe.on('load', function () {
            setTimeout(function () {
                var iframeDiv = iframe.contents().find('div[id]')[0];
                iframeDiv.on('plotly_hover', function (data) {
                    _this._changeGraphImage('hover', data, parent);
                });
                iframeDiv.on('plotly_click', function (data) {
                    _this._changeGraphImage('click', data, parent);
                });
            }, 0);
        });


    });

}

jQuery(function () {
    var interactiveMap = new InteractiveMap();
    interactiveMap.init();
});


