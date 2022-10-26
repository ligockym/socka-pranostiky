<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'd88847_soc' );

/** MySQL database username */
define( 'DB_USER', 'a88847_soc' );

/** MySQL database password */
define( 'DB_PASSWORD', 'uKm6KBEM' );

/** MySQL hostname */
define( 'DB_HOST', 'wm77.wedos.net' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'W=M1;l/.Ql0Zs.kbTl4}L9xnhr8N}|fS>SUl~.X1jeiEf$RNu[J5 nJky_}Wg>Vv' );
define( 'SECURE_AUTH_KEY',  'vic-nQZF[!hT!nRz=86giC7CXeb@EVXbcgbr3SwtT><0wo<sDZS7D&U?(w8;F/MX' );
define( 'LOGGED_IN_KEY',    '5{0<TcEqhW&*At_?7k|W|{8Hf6st#g`DP>}}onb4O)m}A#^yIIE:4=_fcZK*FXsU' );
define( 'NONCE_KEY',        ';[z[2o>p-:@x$X1-Kw6}Q8hI[W9F+W,nJT+<c0N6briw(>yxG|{.>n9s))oP7dQ/' );
define( 'AUTH_SALT',        'zfMa6rP(?jGfJ!=/9tzY<1i2Q2}>##|S s9~SGz*{(S:]3^oaPyMG61#5#aN=b[7' );
define( 'SECURE_AUTH_SALT', ':Goe8qcS==#?}_p,ZQ~*?G#DK(Hxo`VNqb.4IY]qBZ|,s c.z_xm9:>v6.:l#[AD' );
define( 'LOGGED_IN_SALT',   '2.%TcQ4Y87Zgbnl0)Q{pERRTm5B<D}mLGXT#j8/BBM%vY7pwcG{4oOR.mW^)B;<u' );
define( 'NONCE_SALT',       'ZwR+`C:l6Vo3LeIfY9Hlj=?N [Wl0w?|Ft3B^@276Q571.X=kJ*LAb4FKkX>xl 9' );

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define( 'WP_DEBUG', false );

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', dirname( __FILE__ ) . '/' );
}

/** Sets up WordPress vars and included files. */
require_once( ABSPATH . 'wp-settings.php' );