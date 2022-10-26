<?php get_header() ?>
<?php if (have_posts()): while (have_posts()): the_post(); ?>
    <section class="s-intro">
        <div class="container pt-5">
            <div class="row align-items-center">
                <div class="s-intro__text-container text-white col col-md-6">
                    <h1 class="headline headline--type1"><?php the_title()?></h1>
                </div>
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
