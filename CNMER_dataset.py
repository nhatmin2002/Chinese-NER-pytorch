"""split the msra dataset for our model and build tags"""
import os
import random


def load_dataset(path_dataset):
    dataset = []  # Tạo một list mới để chứa tokens và labels
    tmp_tok, tmp_lab = [], []
    label_set = []
    with open(path_dataset, 'r', encoding='utf8') as reader:
        for line in reader:
            if "IMGID" in line: 
                a=1
            else:
                line = line.strip()
                cols = line.split('\t')
                if len(cols) < 2:
                    if len(tmp_tok) > 0:
                        dataset.append((tmp_tok, tmp_lab))  # Thêm tokens và labels vào dataset
                    tmp_tok = []
                    tmp_lab = []
                else:
                    tmp_tok.append(cols[0])
                    tmp_lab.append(cols[-1])
                    label_set.append(cols[-1])
    return dataset


def save_dataset(dataset, save_dir):
    """Write sentences.txt and tags.txt files in save_dir from dataset

    Args:
        dataset: ([(["a", "cat"], ["O", "O"]), ...])
        save_dir: (string)
    """
    # Create directory if it doesn't exist
    print('Saving in {}...'.format(save_dir))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Export the dataset
    with open(os.path.join(save_dir, 'sentences.txt'), 'w') as file_sentences, \
        open(os.path.join(save_dir, 'tags.txt'), 'w') as file_tags:
        for words, tags in dataset:
            file_sentences.write('{}\n'.format(' '.join(words)))
            file_tags.write('{}\n'.format(' '.join(tags)))
    print('- done.')

def build_tags(data_dir, tags_file):
    """Build tags from dataset
    """
    data_types = ['train', 'val', 'test']
    tags = set()
    for data_type in data_types:
        tags_path = os.path.join(data_dir, data_type, 'tags.txt')
        with open(tags_path, 'r') as file:
            for line in file:
                tag_seq = filter(len, line.strip().split(' '))
                tags.update(list(tag_seq))
    with open(tags_file, 'w') as file:
        file.write('\n'.join(tags))
    return tags


if __name__ == '__main__':
    # Check that the dataset exist, two balnk lines at the end of the file
    path_train_val = 'CNMERdata/train.txt'
    path_dev = 'CNMERdata/dev.txt'
    path_test = 'CNMERdata/test.txt'
    msg = '{} or {} file not found. Make sure you have downloaded the right dataset'.format(path_train_val, path_test)
    assert os.path.isfile(path_train_val) and os.path.isfile(path_test), msg

    # Load the dataset into memory
    print('Loading Resume dataset into memory...')
    dataset_train_val = load_dataset(path_train_val)
    dataset_dev = load_dataset(path_dev)
    dataset_test = load_dataset(path_test)
    print('- done.')

    # # Make a list that decides the order in which we go over the data
    # order_t = list(range(len(dataset_train_val)))
    # order_d = list(range(len(dataset_dev)))

    # random.seed(2019)
    # random.shuffle(order_t)
    # random.shuffle(order_d)

    # # Split the dataset into train, val(split with shuffle) and test
    # train_dataset = [dataset_train_val[idx] for idx in order_t[:]]  # 42000 for train
    # val_dataset = [dataset_dev[idx] for idx in order_d[:]]  # 3000 for val
    # test_dataset = dataset_test  # 3442 for test
    save_dataset(dataset_train_val, 'CNMERdata/train')
    save_dataset(dataset_dev, 'CNMERdata/val')
    save_dataset(dataset_test, 'CNMERdata/test')

    # Build tags from dataset
    build_tags('CNMERdata', 'CNMERdata/tags.txt')

