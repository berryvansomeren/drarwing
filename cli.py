import logging
from pathlib import Path

import cv2
import typer

from common.run import run
from my_genetic_algorithms.pointillism import Ellipsilly


logger = logging.getLogger(__name__)
app = typer.Typer()


@app.callback( invoke_without_command = True )
def default_entrypoint() :
    input_image_path = Path('C:/Users/Berry/Documents/development/drarwing/input_images/mario_yoshi.jpg' )
    output_directory_path = Path('C:/Users/Berry/Documents/development/drarwing/results/results_reset' )
    target_image = cv2.imread( str( input_image_path ) )
    assert target_image is not None, f"Could not read target_image: {input_image_path}"
    genetic_algorithm_strategy = Ellipsilly( target_image )
    run(
        output_directory_path,
        genetic_algorithm_strategy,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info('Initializing...')
    app()