<?php get_header() ?>
<?php if (have_posts()): while (have_posts()): the_post(); ?>
    <section class="s-intro">
        <div class="container pt-5">
            <div class="row align-items-center">
                <div class="s-intro__text-container text-white col col-md-6">
                    <h1 class="headline headline--type1">Platia ešte pranostiky?</h1>
                    <p class="text-size-18 mt-2">Vydali sme sa na cestu zistiť či ešte múdro naších starých otcov a mám
                        platí aj v našom modernom svete.</p>
                </div>
                <img src="<?= get_template_directory_uri() ?>/images/mapka.svg" alt="Mapa"
                     class="col offset-md-1 col-md-5 mt-6 mt-md-0">
            </div>
            <div class="row mt-5">
                <div class="col text-size-18"><p>Stredoškolská odborná činnosť</p>
                    <p> Marián Ligocký, Monika Smolková, Tomáš Trlíček</p></div>
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
