import numpy as np
from sklearn.cluster import KMeans


def get_color_palette_for_image(image : np.ndarray, n_colors):
    clustering_obj = KMeans(n_clusters=n_colors)
    clustering_obj.fit(image)

    main_colors = np.array( clustering_obj.cluster_centers_ )

    hsv_deltas = [
        (  0,  0, 0),
        (  0, 50, 0),
        ( 15, 30, 0),
        (-15, 30, 0)
    ]

    full_palette = np.array()
    for hsv_delta in hsv_deltas:
        new_colors = np.add(main_colors, hsv_delta)
        full_palette.append(new_colors)

    # still need to apply a maximum

    return full_palette



    color_probabilities = compute_color_probabilities( pixels, palette, k = 9 )
    color = color_select( color_probabilities[ i ], palette )
        r = random.uniform( 0, 1 )
        i = bisect.bisect_left( probabilities, r )
        return palette[ i ] if i < len( palette ) else palette[ -1 ]


    return ColorPalette(clt.cluster_centers_)