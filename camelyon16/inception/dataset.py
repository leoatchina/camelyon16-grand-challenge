from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import ABCMeta
from abc import abstractmethod
import os

import tensorflow as tf

PROCESSED_PATCHES_TRAIN = '/home/millpc/Documents/Arjun/Study/Thesis/CAMELYON16/data/CAMELYON16/Processed/' \
                                   'patch-based-classification/raw-data/train/'
PROCESSED_PATCHES_TRAIN_NEGATIVE = PROCESSED_PATCHES_TRAIN + 'label-0/'
PROCESSED_PATCHES_TRAIN_POSITIVE = PROCESSED_PATCHES_TRAIN + 'label-1/'

PROCESSED_PATCHES_VALIDATION = '/home/millpc/Documents/Arjun/Study/Thesis/CAMELYON16/data/CAMELYON16/' \
                                        'Processed/patch-based-classification/raw-data/validation/'
PROCESSED_PATCHES_VALIDATION_NEGATIVE = PROCESSED_PATCHES_VALIDATION + 'label-0/'
PROCESSED_PATCHES_VALIDATION_POSITIVE = PROCESSED_PATCHES_VALIDATION + 'label-1/'

DATA_DIR = '/home/arjun/MS/Thesis/CAMELYON-16/Data/Processed/tf-records/'


FLAGS = tf.app.flags.FLAGS

# Basic model parameters.
tf.app.flags.DEFINE_string('data_dir', DATA_DIR,
                           """Path to the processed data, i.e. """
                           """TFRecord of Example protos.""")


class Dataset(object):
    """A simple class for handling data sets."""
    __metaclass__ = ABCMeta

    def __init__(self, name, subset):
        """Initialize dataset using a subset and the path to the data."""
        assert subset in self.available_subsets(), self.available_subsets()
        self.name = name
        self.subset = subset

    def num_classes(self):
        """Returns the number of classes in the data set."""
        return 2  # [0, 1]

    def num_examples_per_epoch(self):
        """Returns the number of examples in the data subset."""
        if self.subset == 'train':
            return 250000
        if self.subset == 'validation':
            return 10000

    @abstractmethod
    def download_message(self):
        """Prints a download message for the Dataset."""
        pass

    def num_examples_per_shard(self):
        """Returns the number of examples in one shard."""
        if self.subset == 'train':
            return 1000
        if self.subset == 'validation':
            return 250

    def available_subsets(self):
        """Returns the list of available subsets."""
        return ['train', 'validation']

    def data_files(self):
        """Returns a python list of all (sharded) data subset files.

        Returns:
          python list of all (sharded) data set files.
        Raises:
          ValueError: if there are not data_files matching the subset.
        """
        tf_record_pattern = os.path.join(FLAGS.data_dir, '%s-*' % self.subset)
        data_files = tf.gfile.Glob(tf_record_pattern)
        if not data_files:
            print('No files found for dataset %s/%s at %s' % (self.name,
                                                              self.subset,
                                                              FLAGS.data_dir))

            self.download_message()
            exit(-1)
        return data_files

    def data_files_test(self):
        """Returns a python list of all (sharded) data subset files.

        Returns:
          python list of all (sharded) data set files.
        Raises:
          ValueError: if there are not data_files matching the subset.
        """
        tf_record_pattern = os.path.join('/home/millpc/Documents/Arjun/Study/Thesis/CAMELYON16/data/CAMELYON16/'
                                         'Processed/patch-based-classification/tf-records/', '%s-*' % self.subset)
        data_files = tf.gfile.Glob(tf_record_pattern)
        if not data_files:
            print('No files found for dataset %s/%s at %s' % (self.name,
                                                              self.subset,
                                                              FLAGS.data_dir))

            self.download_message()
            exit(-1)
        return data_files[:1]

    def reader(self):
        """Return a reader for a single entry from the data set.

        See io_ops.py for details of Reader class.

        Returns:
          Reader object that reads the data set.
        """
        return tf.TFRecordReader()