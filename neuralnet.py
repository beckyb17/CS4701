#import tensorflow as tf
print("before")
import tensorflow_datasets as tfds

(train_X ,train_Y), (test_X,test_Y) = tfds.load('stanford_dogs')

print("after")