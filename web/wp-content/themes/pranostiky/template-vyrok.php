<?php /* Template Name: Výrok */ ?>

<?php get_header() ?>
<?php if (have_posts()): while (have_posts()): the_post(); ?>
    <section class="s-intro first-section">
        <div class="container">
            <?php include(locate_template('template-parts/layout/breadcrumbs.php')) ?>
        </div>

        <div class="container pt-5">
            <div class="row align-items-start">
                <div class="s-intro__text-container text-white col col-md-6">
                    <h2 class="headline headline--type3 mb-3 animate-ready">Znenie výroku:</h2>
                    <h1 class="headline headline--type2 pb-4 animate-ready" data-delay="0.3"><?php the_field('pranostika_full')?></h1>
                    <div class="text-size-18 mt-4 mt-md-5 animate-ready" data-delay="0.7">
                        <p><strong>Ciele:</strong></p>
                        <?php the_field('pranostika_aim')?>
                    </div>
                </div>
                <div class="s-intro__text-box col col-md-5 offset-md-1 animate-ready" data-delay="0.5">
                    <h2 class="headline headline--type2 mb-3">Stručné hodnotenie:</h2>
                    <div class="text text--formatted">
                        <?php the_field('pranostika_short-conclusion')?>
                    </div>
                </div>
            </div>

            <div class="d-none d-md-block text-center mt-5">
                <img src="<?= get_template_directory_uri() ?>/images/mouse_icon.svg" height="30" class="s-intro__mouse">
            </div>
        </div>
    </section>

    <section class="s-page-content section text text--formatted">
        <div class="container">
            <?php the_content() ?>
        </div>
    </section>
<?php endwhile; endif; ?>
<?php get_footer() ?>
