var breakPoint1 = 768,
    breakPoint2 = 1170,
    breakPoint3 = 1600;

var Core = function () {

}

Core.prototype.init = function () {
    this._prepareAnimations();
    this._prepareAnalytics();
    this._prepareNavigation();
    this._prepareModals();

    var _this = this;
    jQuery('.scroll').click(function () {
        _this.scrollTo(jQuery(jQuery(this).attr('href')));
    });
}

Core.prototype._prepareAnalytics = function () {
    jQuery(document.body).on('click', '.ga', function (e) {
        var el = jQuery(e.currentTarget),
            evCat = el.attr('data-ga-category'),
            evAction = el.attr('data-ga-action'),
            evLabel = el.attr('data-ga-label'),
            evValue = el.attr('data-ga-value');
        gtag('event', evAction, {
            'event_category': evCat,
            'event_label': evLabel,
            'event_value': evValue
        });
    });
}

Core.prototype._prepareAnimations = function () {
    var elementsToAnimate = jQuery(".animate-ready, *[data-animation], *[data-delay]")
        .not('.animate-disabled, .animate-disabled *');

    /**
     *
     * @param proportionOfScreen
     * @param loaded if function is called after page was loaded or scrolled
     */
    var animateNewItems = function (proportionOfScreen, afterLoaded) {
        elementsToAnimate.not('.animated').each(function () {
            var $this = jQuery(this);
            var position = $this.offset().top,
                bottom_window = jQuery(window).scrollTop() + (jQuery(window).height() * proportionOfScreen);

            var delay = parseFloat($this.attr('data-delay'));
            if (!isNaN(delay) && afterLoaded) {
                $this.css('animation-delay', delay + "s");
            }

            if ((!$this.hasClass('.animated') && position < bottom_window)) {
                var classes = $this.attr('data-animation') ? "animated " + $this.attr('data-animation') : "animated fadeInUpLight";
                $this.addClass(classes).removeClass('animate-ready');
            }
        });
    };

    jQuery(window).on('load', animateNewItems(1.1, true)); // to show all items in viewport
    jQuery(window).on('scroll', function () {
        animateNewItems(0.9, false);
    });
    jQuery(window).on('runAnimations', function () {
        animateNewItems(0.9, false);
    });
};

/**
 * @param {jQuery} element
 */
Core.prototype.scrollTo = function (element) {
    var body = jQuery('html, body');

    /*body.on("scroll mousedown wheel DOMMouseScroll mousewheel keyup touchmove", function () {
        body.stop();
    });*/

    var position = element.offset().top - jQuery('.top-bar__top-bar').outerHeight();

    body.animate({scrollTop: position}, 500, 'easeInOutCubic', function () {
        body.off("scroll mousedown wheel DOMMouseScroll mousewheel keyup touchmove");
    });
};

Core.prototype.navigationClose = function () {
    var header = jQuery(".top-bar"),
        navMenu = header.find('.top-bar__nav');
    header.removeClass('top-bar--opened');
    navMenu.slideUp(300);
}

Core.prototype._prepareNavigation = function () {
    var header = jQuery(".top-bar"),
        navMenu = header.find('.top-bar__nav'),
        _this = this;
    jQuery(".top-bar__nav-opener").click(function () {
        if (header.hasClass('top-bar--opened')) {
            _this.navigationClose();
        } else {
            header.addClass('top-bar--opened');
            setTimeout(function () {
                navMenu.slideDown(300);
            });
        }
    });

    jQuery(window).on('scroll', function () {
        setTimeout(function () {
            if (header.offset().top == 0) {
                header.removeClass('top-bar--scrolled');
            } else {
                header.addClass('top-bar--scrolled');
            }
        }, 0);
    });

    jQuery(window).on('load resize', function () {
        if (jQuery(window).width() <= breakPoint1) { // smaller than breakpoint
            header.removeClass('top-bar--opened');
            navMenu.slideUp(0);
        } else {
            navMenu.slideDown(0);
        }
    });
}

Core.prototype._prepareModals = function () {
    MicroModal.init({
        onShow: modal => {
            const iframe = jQuery(modal).find('iframe');
            console.log(iframe.attr('src', iframe.attr('data-src')));
        }, // [1]
        onClose: modal => {
            const iframe = jQuery(modal).find('iframe');
            console.log(iframe.attr('src', iframe.attr('data-src')));
        }, // [2]
    });
    jQuery('.modal--default-open').each(function () {
        MicroModal.show(jQuery(this).attr('id'));
    });
}

jQuery(function () {
    var core = new Core();
    core.init();
});


