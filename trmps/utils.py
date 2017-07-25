import tensorflow as tf
import urllib
import tarfile
import sys
import numpy as np

def check_nan(tensor, name, replace_nan=True):
    s = tf.reduce_sum(tensor)
    is_nan = tf.is_nan(s)
    tensor = tf.cond(is_nan, 
                     true_fn=lambda: tf.Print(tensor, [tensor], 
                                            message='{} is not finite'.format(name)), 
                     false_fn=lambda: tensor)
    if replace_nan:
        tensor = tf.where(tf.is_nan(tensor), 
                          tf.zeros_like(tensor), 
                          tensor)
    return tensor 

def getunzipped(url, name):
    try:
        name, hdrs = urllib.request.urlretrieve(url, name)
    except IOError as e:
        print('Cannot retrieve {}: {}'.format(url, e))
        return 
    z = tarfile.open(name, "r:gz")
    z.extractall()
    z.close()
    print('Data downloaded and unzipped')


class spinner(object):
    def __init__(self, jump = 400):
        self.index = 0
        self.jump = jump
        self.percentage = 0
        self.counter = 0
        
    def print_spinner(self, percentage):
        if float(percentage) == 100.0:
            sys.stdout.flush()
            print("\r" + str(100) + " % done")
        elif self.index % self.jump == 0:
            sys.stdout.flush()
            # Spinner to show progress 
            if self.counter == 0:
                print("\r" + str(percentage) + " % done", end="|")
                self.counter += 1
            elif self.counter == 1:
                print("\r" + str(percentage) + " % done", end="/")
                self.counter += 1
            elif self.counter == 2:
                print("\r" + str(percentage) + " % done", end="-")
                self.counter += 1
            elif self.counter == 3:
                print("\r" + str(percentage) + " % done", end="\\")
                self.counter = 0
        self.index += 1
        
# Adapted from https://stackoverflow.com/questions/29831489/numpy-1-hot-array
def convert_to_onehot(vector, num_classes=None):
    """
    Converts an input 1-D vector of integers into an output
    2-D array of one-hot vectors, where an i'th input value
    of j will set a '1' in the i'th row, j'th column of the
    output array.

    Example:
        v = np.array((1, 0, 4))
        one_hot_v = convertToOneHot(v)
        print one_hot_v

        [[0 1 0 0 0]
         [1 0 0 0 0]
         [0 0 0 0 1]]
    """
    assert isinstance(vector, np.ndarray)
    assert len(vector) > 0

    if num_classes is None:
        num_classes = np.max(vector)+1
    else:
        assert num_classes > 0
        assert num_classes >= np.max(vector)

    result = np.zeros(shape=(len(vector), num_classes))
    result[np.arange(len(vector)), vector] = 1
    return result.astype(int)







