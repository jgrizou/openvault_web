import os
import uuid
import base64
import tempfile

import scipy
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import matplotlib
matplotlib.use("Agg")
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def scale_data_to_view_windows(data, view_bounds=(0.1, 0.9)):
    scaler = MinMaxScaler(view_bounds)
    scaler.fit(data)
    scaled_data = scaler.transform(data).tolist()
    return scaled_data, scaler


def generate_map_from_classifier(clf, bounds=(0., 1.), scaler=None, resolution=100j):
    grid_x, grid_y = np.mgrid[bounds[0]:bounds[1]:resolution, bounds[0]:bounds[1]:resolution]
    # trick on coordinate for imshow to display as a scatter plot
    X_flat_grid = np.vstack((grid_y.flatten(), 1 - grid_x.flatten())).T

    # the map is between bounds but if a scaler is used we project these to back to the original space that the classifier has been trained on
    if scaler:
        X_flat_grid = scaler.inverse_transform(X_flat_grid)

    pred_y_flat_grid = clf.predict_proba(X_flat_grid)[:, 1]
    pred_y_grid = pred_y_flat_grid.reshape(grid_x.shape)

    return pred_y_grid


def generate_map_from_dataset(points, labels, bounds=(0., 1.), scaler=None, resolution=100j):
    grid_x, grid_y = np.mgrid[bounds[0]:bounds[1]:resolution, bounds[0]:bounds[1]:resolution]
    # trick on coordinate for imshow to display as a scatter plot
    X_flat_grid = np.vstack((grid_y.flatten(), 1 - grid_x.flatten())).T

    # the map is between bounds but if a scaler is used we project these to back to the original space that the classifier has been trained on
    if scaler:
        X_flat_grid = scaler.inverse_transform(X_flat_grid)

    pred_y_flat_grid = np.mean(X_flat_grid, axis=1)

    sigma = 10
    distances = scipy.spatial.distance.cdist(X_flat_grid, points)
    rbf_values = np.exp(-np.power(sigma*distances, 2))
    index = np.expand_dims(np.argmax(rbf_values, axis=1), axis=1)

    color_intensity_for_map = 0.5  # must be less than 1
    weights = np.array([color_intensity_for_map if x else -color_intensity_for_map for x in labels])
    weighted_values = weights * rbf_values

    pred_y_flat_grid = np.take_along_axis(weighted_values, index, axis=1)

    # scale between 0 and 1 for later color mapping
    pred_y_flat_grid = (pred_y_flat_grid + 1) / 2

    # reshape to grid
    pred_y_grid = pred_y_flat_grid.reshape(grid_x.shape)

    return pred_y_grid


def flip_map_for_web(map_grid):
    # we flip because image on web have the y axis fliped
    return np.flip(map_grid, 0)

def save_map_to_file(map_grid, filename, bounds=(0., 1.), fig_width_inches=1):
    fig = plt.figure()
    fig.set_size_inches((fig_width_inches, fig_width_inches))
    ax = plt.Axes(fig, [bounds[0], bounds[0], bounds[1], bounds[1]])
    ax.set_axis_off()
    fig.add_axes(ax)

    # making color map
    alpha = 0.85
    n_steps = 100
    color_list = []
    # yellow to white
    c2 = np.linspace(255/255, 255/255, n_steps)
    c3 = np.linspace(200/255, 255/255, n_steps)
    c4 = np.linspace(000/255, 255/255, n_steps)
    for v2, v3, v4 in zip(c2, c3, c4):
        color_list.append([v2, v3, v4, alpha])
    #
    color_list.pop()
    # white to gray
    c1 = np.linspace(255/255, 160/255, n_steps)
    for v1 in c1:
        color_list.append([v1, v1, v1, alpha])

    c_class_map = matplotlib.colors.ListedColormap(color_list)
    plt.imshow(map_grid, cmap=c_class_map, extent=(0, 1, 0, 1), vmin=0, vmax=1)
    plt.savefig(filename, dpi=100)
    plt.close(fig)


def encode_png_base64(png_filename):
    # read image and convert it to a format I can send to the webpage, a base64 encoded png file.
    with open(png_filename, 'rb') as f:
        png_image_base64 = base64.b64encode(f.read()).decode()

    return 'data:image/png;base64,{}'.format(png_image_base64)


def generate_web_classifier_map(classifier, signal_scaler):

    classifier_map = generate_map_from_classifier(classifier, scaler=signal_scaler)
    classifier_map_web = flip_map_for_web(classifier_map)

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_map_filename = os.path.join(tmpdirname, '{}.png'.format(uuid.uuid4()))
        save_map_to_file(classifier_map_web, tmp_map_filename)
        encoded_map = encode_png_base64(tmp_map_filename)

    return encoded_map
