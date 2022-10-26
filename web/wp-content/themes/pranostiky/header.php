<!DOCTYPE html>
<html lang="sk" data-base-url="<?= get_template_directory_uri() ?>">
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title><?php if (is_home()) {
                bloginfo('name');
            } else {
                wp_title('');
            } ?></title>
        <?php wp_head(); ?>
    </head>
<body <?= body_class() ?>>

<div class="body-content">
<?php include 'template-parts/layout/main-nav.php'; ?>

