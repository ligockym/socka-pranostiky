<div class="top-bar">
    <div class="top-bar__wrapper container">
        <div class="top-bar__top">
            <a href="<?= esc_url(get_home_url()) ?>" class="top-bar__logo">
                <img height="40" src="<?= get_template_directory_uri() ?>/images/logo-blue.svg"
                     alt="Štvorica troch duelantov logo" class="">

            </a>

            <div class="top-bar__nav-opener">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>

        <div class="top-bar__nav">
            <?php wp_nav_menu(['theme_location' => '']); ?>
        </div>
    </div>
</div>

