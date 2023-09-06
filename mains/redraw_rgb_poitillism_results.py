import logging
from pathlib import Path
import pickle

from redraw import redraw_pointillism_as_svg

from genetic_algorithms.impl.pointillism import Pointillism


REDRAW_ELLIPSE_SCALES = [ 1.0, 1.5, 2.0 ]

RESULTS_ROOT = f'{Path(__file__).parent.parent}/results/'

NAMES = [
    'elk',
    'fish',
    'squirrel',
    'fox',
    'parrot',
]

PICKLES_TO_REDRAW_RGB = [
    'andrew-ly-5AftAzShDDQ-unsplash/gen_167651__dt_641094_ms__score_6398.pickle',
    'david-clode-oTMGUchAwTQ-unsplash/gen_112814__dt_387993_ms__score_4586.pickle',
    'hasse-lossius-j9CIeJZIECk-unsplash/gen_091695__dt_652002_ms__score_5288.pickle',
    'olga-kononenko-Ltyfaze30SA-unsplash/gen_111164__dt_985476_ms__score_5361.pickle',
    'tim-mossholder-cO5-QcKIR9o-unsplash/gen_127878__dt_204068_ms__score_4838.pickle',
]

PICKLES_TO_REDRAW_HSV = [
    'andrew-ly-5AftAzShDDQ-unsplash/gen_097694__dt_68843_ms__score_7517.pickle',
    'david-clode-oTMGUchAwTQ-unsplash/gen_107323__dt_993660_ms__score_4097.pickle',
    'hasse-lossius-j9CIeJZIECk-unsplash/gen_103418__dt_900430_ms__score_7310.pickle',
    'olga-kononenko-Ltyfaze30SA-unsplash/gen_112174__dt_874107_ms__score_6625.pickle',
    'tim-mossholder-cO5-QcKIR9o-unsplash/gen_117668__dt_985561_ms__score_6599.pickle',
]


def redraw_rgb_pointillis_results_at_scale(
        in_pickle_path : str,
        out_path : str,
        use_hsv : bool,
        ellipse_scale : float,
) -> None:
    logging.info( f'Reading "{in_pickle_path}"' )
    with open( in_pickle_path, 'rb' ) as pickle_file :
        specimen = Pointillism.Specimen( **pickle.load( pickle_file ) )
    result_svg = redraw_pointillism_as_svg( specimen, use_hsv, ellipse_scale )
    result_svg.saveas( out_path )
    logging.info( f'Wrote "{out_path}"' )


def redraw_rgb_pointillism_results() -> None:
    for ellipse_scale in REDRAW_ELLIPSE_SCALES:
        logging.info( f'Redrawing at scale "{ellipse_scale}"' )
        Path( f'{RESULTS_ROOT}/redrawn/{ellipse_scale}' ).mkdir( exist_ok = False )

        for in_name, out_name in zip( PICKLES_TO_REDRAW_RGB, NAMES ) :
            in_path = f'{RESULTS_ROOT}/rgb/{in_name}'
            out_path = f'{RESULTS_ROOT}/redrawn/{ellipse_scale}/{out_name}_rgb.svg'
            redraw_rgb_pointillis_results_at_scale(
                in_pickle_path = in_path,
                out_path = out_path,
                use_hsv = False,
                ellipse_scale = ellipse_scale
            )

        for in_name, out_name in zip( PICKLES_TO_REDRAW_HSV, NAMES ) :
            in_path = f'{RESULTS_ROOT}/hsv/{in_name}'
            out_path = f'{RESULTS_ROOT}/redrawn/{ellipse_scale}/{out_name}_hsv.svg'
            redraw_rgb_pointillis_results_at_scale(
                in_pickle_path = in_path,
                out_path = out_path,
                use_hsv = True,
                ellipse_scale = ellipse_scale
            )

    logging.info( "Done" )


if __name__ == "__main__":
    logging.basicConfig( level = logging.INFO )
    redraw_rgb_pointillism_results()
