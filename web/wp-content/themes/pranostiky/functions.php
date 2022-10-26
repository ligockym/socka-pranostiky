<?php
/**
 * Functions file for AveNatura site.
 * All woocommerce settings found in config/woocommerce.php
 */


/*  Register Scripts and Style */
function theme_register_scripts()
{
    wp_enqueue_style('google-fonts', 'https://fonts.googleapis.com/css?family=Barlow+Semi+Condensed:600|Barlow:300,400&display=swap&subset=latin-ext');
    wp_enqueue_style('pranostiky-css', get_stylesheet_uri(), null, '0.0.1');

    wp_enqueue_script('jquery');
    wp_enqueue_script('micromodal', 'https://unpkg.com/micromodal/dist/micromodal.min.js', null, null, true);
    wp_enqueue_script('plotly', 'https://cdn.plot.ly/plotly-latest.min.js', null, null, false);
    wp_enqueue_script('fontawesome', 'https://kit.fontawesome.com/850a3f988d.js', null, null, true);
    wp_enqueue_script('axios', 'https://cdnjs.cloudflare.com/ajax/libs/axios/0.19.0/axios.min.js', null, null);
    wp_enqueue_script('vue-js', 'https://cdn.jsdelivr.net/npm/vue@2.6.11', null, null, false);
    wp_enqueue_script('pranostiky-core', esc_url(trailingslashit(get_template_directory_uri()) . 'js/core.js'), 'jquery', null, true);
    wp_enqueue_script('pranostiky-interactive-map', esc_url(trailingslashit(get_template_directory_uri()) . 'js/interactive-map.js'), 'jquery', null, true);

    /*
    wp_localize_script('pranostiky-core', 'rest_object',
        array(
            'api_nonce' => wp_create_nonce('wp_rest'),
            'api_url' => site_url('/wp-json/cart/change-quantity')
        ));*/
}

add_action('wp_enqueue_scripts', 'theme_register_scripts', 1);

/* Add menu support */
if (function_exists('add_theme_support')) {
    add_theme_support('menus');
}
/* Add post image support */
add_theme_support('post-thumbnails');
/* Add custom thumbnail sizes */
if (function_exists('add_image_size')) {
    // CUSTOM IMAGE SIZES
    add_image_size('gallery-thumbnail', 300, 200);
}

add_filter('jpeg_quality', function ($arg) {
    return 95;
});


/* Add widget support */
/*  EXCERPT
    Usage:

    <?php echo excerpt(100); ?>
*/
function excerpt($limit, $excerpt_default = null)
{
    if (!$excerpt_default) {
        $excerpt = explode(' ', get_the_excerpt(), $limit);
    } else {
        $excerpt = explode(' ', $excerpt_default, $limit);
    }
    if (count($excerpt) >= $limit) {
        array_pop($excerpt);
        $excerpt = implode(" ", $excerpt) . '...';
    } else {
        $excerpt = implode(" ", $excerpt);
    }
    $excerpt = preg_replace('`\[[^\]]*\]`', '', $excerpt);
    return $excerpt;
}

//add_filter('show_admin_bar', '__return_false');

function register_my_menus()
{
    register_nav_menus(
        array(
            'header-menu' => __('Hlavné menu'),
        )
    );
}

add_action('init', 'register_my_menus');

register_sidebar(array(
    'name' => 'Pätička - kontakt',
    'id' => 'footer-sidebar-1',
    'description' => 'Zobrazí sa v pätičke',
    'before_widget' => '<div>',
    'after_widget' => '</div>',
    'before_title' => '<h3 class="footer__item-headline">',
    'after_title' => '</h3>',
));

// Object of WP_term
function categories_slugs_to_string($categoryObject)
{
    $string = '';
    foreach ($categoryObject as $cat) {
        $string .= $cat->slug . ';';
    }
    return $string;
}

function ave_remove_private_protected_from_titles($format)
{
    return '%s';
}

add_filter('protected_title_format', 'ave_remove_private_protected_from_titles');

function get_custom_link($page)
{
    $links = [
        'home' => get_home_url()
    ];
    if (isset($links[$page])) {
        return $links[$page];
    }
    return '';
}

// Register video block for AdvancedCustomFields
function register_acf_block_types()
{

    // register a video block.

    acf_register_block_type(array(
        'name' => 'map-block',
        'title' => __('Interaktívna mapka'),
        'description' => __('Zobrazenie interaktívnej mapky'),
        'render_template' => 'template-parts/blocks/map-block/map-block.php',
        'category' => 'formatting',
        'icon' => 'admin-video',
        'keywords' => array('map', 'block'),
    ));


}

// Check if function exists and hook into setup.
if (function_exists('acf_register_block_type')) {
    add_action('acf/init', 'register_acf_block_types');
}

add_filter('excerpt_more', function () {
    return '...';
});

function time_ago($post_id = null)
{
    return human_time_diff(get_post_time('U', false, $post_id), current_time('timestamp')) . " " . __('dozadu');

}