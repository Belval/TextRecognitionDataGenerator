import os
import pickle
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import seaborn
from PIL import Image
from collections import namedtuple

class HandwrittenTextGenerator(object):
    @classmethod
    def __sample(cls, e, mu1, mu2, std1, std2, rho):
        cov = np.array([[std1 * std1, std1 * std2 * rho],
                        [std1 * std2 * rho, std2 * std2]])
        mean = np.array([mu1, mu2])

        x, y = np.random.multivariate_normal(mean, cov)
        end = np.random.binomial(1, e)
        return np.array([x, y, end])


    @classmethod
    def __split_strokes(cls, points):
        points = np.array(points)
        strokes = []
        b = 0
        for e in range(len(points)):
            if points[e, 2] == 1.:
                strokes += [points[b: e + 1, :2].copy()]
                b = e + 1
        return strokes


    @classmethod
    def __cumsum(cls, points):
        sums = np.cumsum(points[:, :2], axis=0)
        return np.concatenate([sums, points[:, 2:]], axis=1)


    @classmethod
    def __sample_text(cls, sess, args_text, translation):
        # Original creator said it helps (https://github.com/Grzego/handwriting-generation/issues/3)
        args_text += ' '

        fields = ['coordinates', 'sequence', 'bias', 'e', 'pi', 'mu1', 'mu2', 'std1', 'std2',
                  'rho', 'window', 'kappa', 'phi', 'finish', 'zero_states']
        vs = namedtuple('Params', fields)(
            *[tf.get_collection(name)[0] for name in fields]
        )

        text = np.array([translation.get(c, 0) for c in args_text])
        sequence = np.eye(len(translation), dtype=np.float32)[text]
        sequence = np.expand_dims(np.concatenate([sequence, np.zeros((1, len(translation)))]), axis=0)

        coord = np.array([0., 0., 1.])
        coords = [coord]

        phi_data, window_data, kappa_data, stroke_data = [], [], [], []
        sess.run(vs.zero_states)
        for s in range(1, 60 * len(args_text) + 1):
            e, pi, mu1, mu2, std1, std2, rho, \
            finish, phi, window, kappa = sess.run([vs.e, vs.pi, vs.mu1, vs.mu2,
                                                   vs.std1, vs.std2, vs.rho, vs.finish,
                                                   vs.phi, vs.window, vs.kappa],
                                                  feed_dict={
                                                      vs.coordinates: coord[None, None, ...],
                                                      vs.sequence: sequence,
                                                      vs.bias: 1.
                                                  })
            phi_data += [phi[0, :]]
            window_data += [window[0, :]]
            kappa_data += [kappa[0, :]]
            # ---
            g = np.random.choice(np.arange(pi.shape[1]), p=pi[0])
            coord = cls.__sample(e[0, 0], mu1[0, g], mu2[0, g],
                           std1[0, g], std2[0, g], rho[0, g])
            coords += [coord]
            stroke_data += [[mu1[0, g], mu2[0, g], std1[0, g], std2[0, g], rho[0, g], coord[2]]]

            if finish[0, 0] > 0.8:
                break

        coords = np.array(coords)
        coords[-1, 2] = 1.

        return phi_data, window_data, kappa_data, stroke_data, coords

    @classmethod
    def __crop_white_borders(cls, image):
        image_data = np.asarray(image)
        non_empty_columns = np.where(image_data.min(axis=0)<255)[0]
        non_empty_rows = np.where(image_data.min(axis=1)<255)[0]
        cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

        image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1]

        return Image.fromarray(image_data_new)

    @classmethod
    def __join_images(cls, images):
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths) - 35 * len(images)
        max_height = max(heights)

        compound_image = Image.new('L', (total_width, max_height))

        x_offset = 0
        for im in images:
            compound_image.paste(im, (x_offset,0))
            x_offset += (im.size[0] - 35)

        return compound_image

    @classmethod
    def generate(cls, text):
        with open(os.path.join('handwritten_model', 'translation.pkl'), 'rb') as file:
            translation = pickle.load(file)

        config = tf.ConfigProto(
            device_count={'GPU': 0}
        )
        tf.reset_default_graph()
        with tf.Session(config=config) as sess:
            saver = tf.train.import_meta_graph('handwritten_model/model-29.meta')
            saver.restore(sess, 'handwritten_model/model-29')
            images = []
            for word in text.split(' '):
                _, window_data, kappa_data, stroke_data, coords = cls.__sample_text(sess, word, translation)

                strokes = np.array(stroke_data)
                strokes[:, :2] = np.cumsum(strokes[:, :2], axis=0)
                _, maxx = np.min(strokes[:, 0]), np.max(strokes[:, 0])
                miny, maxy = np.min(strokes[:, 1]), np.max(strokes[:, 1])

                fig, ax = plt.subplots(1, 1)
                fig.patch.set_visible(False)
                ax.axis('off')

                for stroke in cls.__split_strokes(cls.__cumsum(np.array(coords))):
                    plt.plot(stroke[:, 0], -stroke[:, 1], color='#080808')

                canvas = plt.get_current_fig_manager().canvas
                canvas.draw()

                image = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb()).convert('L')
                images.append(cls.__crop_white_borders(image))

                plt.close()

            return cls.__join_images(images)
