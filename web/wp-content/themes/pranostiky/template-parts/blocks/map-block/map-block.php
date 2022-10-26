<?php

/**
 * Video Block Theme
 *
 * @param array $block The block settings and attributes.
 * @param string $content The block inner HTML (empty).
 * @param bool $is_preview True during AJAX preview.
 * @param   (int|string) $post_id The post ID this block is saved to.
 */

// Create id attribute allowing for custom "anchor" value.
$id = uniqid();
if (!empty($block['anchor'])) {
    $id = $block['anchor'];
}
?>
<div class="map-block my-5">
    <div class="map-block__text">
        <h3 class="text-size-16 text-medium mt-0 mb-4">Interaktívna mapka</h3>
        <div class="text text--formatted mb-4">
            <p>Prezrite si výsledky nášho výskumu v pripravenej mapke aj s možnosťou porovnávania a prezerania grafov
                pre samotné body mriežky.</p>
        </div>
        <a href="#" class="button-link smooth-scroll" data-micromodal-trigger="map-block-<?= $id ?>">Otvoriť interaktívnu mapu<i
                    class="icon icon--chevron-right ml-2 text-size-10"></i></a>
    </div>

    <div class="map-block__thumbnail" data-micromodal-trigger="map-block-<?= $id ?>">
        <img src="<?= get_template_directory_uri() ?>/images/map_bg.jpg" alt="Interaktívna mapa">
        <div class="map-block__thumbnail-opener">
            <div class="map-block__thumbnail-circle">
                <i class="fas fa-map-marked-alt"></i>
            </div>
            <span>otvoriť mapku</span>
        </div>
    </div>

</div>

<div class="modal micromodal-slide map-block__parent" id="map-block-<?= $id ?>" aria-hidden="true">
    <div class="modal__content">
        <div class="modal__overlay" tabindex="-1" data-micromodal-close>
            <div class="map-block__modal modal__container modal__container--small" role="dialog" aria-modal="true"
                 aria-labelledby="Interaktívna mapka">
                <div class="row align-items-center">
                    <div class="col-md-5 map-block__graph-container">
                        <img data-base-url="<?= content_url() ?>/interactive-maps/<?php the_field('slug') ?>/graphs"
                             src="<?= content_url() ?>/interactive-maps/<?php the_field('slug') ?>/graphs/1.svg"
                             class="map-block__graph-hover" width="100%" alt="Obrázok grafu">
                        <img data-base-url="<?= content_url() ?>/interactive-maps/<?php the_field('slug') ?>/graphs"
                             src="<?= content_url() ?>/interactive-maps/<?php the_field('slug') ?>/graphs/1.svg"
                             class="map-block__graph-click" width="100%" alt="Obrázok grafu">
                    </div>
                    <div class="col-md-5 d-none">
                        <div class="map-block__map-data mt-5">
                            <table>
                                <tr>
                                    <td>Korelácia:</td>
                                    <td><span data-field="success">0.4</span></td>
                                    <td><input type="checkbox" id="modal-graph-<?= $id ?>"><label
                                                for="modal-graph-<?= $id ?>">porovnať graf</td>
                                </tr>
                                <tr>
                                    <td>Úspešnosť:</td>
                                    <td><span data-field="percentage">60</span>%</td>
                                </tr>
                                <tr>
                                    <td>Výška:</td>
                                    <td><span data-field="station_altitude">83</span> m.n.m</td>
                                </tr>
                                <tr>
                                    <td>Krajiny:</td>
                                    <td><span data-field="station_country_name">Maďarsko</span></td>
                                </tr>
                                <tr>
                                    <td>Poloha:</td>
                                    <td><span data-field="station_lan">24,4</span>' <span
                                                data-field="station_lon">40,6</span>'
                                    </td>
                                </tr>
                            </table>

                        </div>
                    </div>
                    <div class="col-md-7">
                        <iframe class="map-block__iframe"
                                data-id="<?= $id ?>"
                                data-src="<?= content_url() ?>/interactive-maps/<?php the_field('slug'); ?>/<?php the_field('slug'); ?>.html"></iframe>
                        <p class="text-size-16 mt-0 text-center">Podľa pohybu myšky sa mení horný graf, po kliknutí na mapu sa zmení dolný graf.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>