# -*- coding: utf-8 -*-
import argparse
from tempfile import TemporaryFile


def get_file_line_reader(file_object):
    """
    Function used for getting generator object used for reading lines from file
    :param file_object: file like object
    :return: generator object
    """
    while True:
        line = file_object.readline()
        if line:
            yield line
        else:
            break


def write_sorted_file_chunk(lines, temp_files_list):
    """
    Function used for writing sorted line chunks to temporary file
    :param lines: list of strings
    :param temp_files_list: list of file objects
    """
    lines.sort(key=lambda line: line.split(' ')[2])
    temp_file = TemporaryFile()
    temp_file.writelines(lines)
    temp_file.seek(0)
    temp_files_list.append(temp_file)


def merge_files(file_1_path, file_2_path, merged_file_path):
    """
    Function used for merging two files based on key in the second column of those files.
    Lines in merged file are sorted by that key.
    :param file_1_path: string, path to file_1
    :param file_2_path: string, path to file_2
    :param merged_file_path: string, path to merge_file
    """
    file_1 = open(file_1_path, 'r')
    file_2 = open(file_2_path, 'r')
    temp_merged_file = TemporaryFile()

    # merge file_1 and file_2 based on key in the second column in file
    file_1_reader = get_file_line_reader(file_1)
    for file_1_line in file_1_reader:
        file_1_line_split = file_1_line.split(' ')
        if len(file_1_line_split) < 2:
            continue

        code_1 = file_1_line_split[1]
        file_2_reader = get_file_line_reader(file_2)
        for file_2_line in file_2_reader:
            file_2_line_split = file_2_line.split(' ')
            if len(file_2_line_split) < 2:
                continue

            code_2 = file_2_line_split[1]
            if code_1 == code_2:
                data_1 = file_1_line_split[0]
                data_2 = file_2_line_split[0]
                combined_string = '{0} {1} {2}'.format(data_1, data_2, code_1)
                temp_merged_file.write(combined_string)
        file_2.seek(0)

    file_1.close()
    file_2.close()
    temp_merged_file.seek(0)
    temp_files_list = []

    # split temp_merged_file to temporary files with 100 lines or less each
    while True:
        lines = []
        for line in temp_merged_file:
            if not line:
                break
            lines.append(line)
            if len(lines) == 100:
                write_sorted_file_chunk(lines, temp_files_list)
                lines = []
        if lines:
            write_sorted_file_chunk(lines, temp_files_list)
        break
    temp_merged_file.close()

    # read first line from each temporary file and sort them by key in third column in file
    # only the line with the smallest key is written to merged_file, others are stored in sort_queue
    merged_file = open(merged_file_path, 'w+')
    sort_queue = {}
    while True:
        for index, temp_file in enumerate(temp_files_list):
            if index not in sort_queue:
                line = temp_file.readline()
                if line:
                    sort_queue[index] = line
        if not sort_queue:
            break
        lines_to_sort = sort_queue.values()
        lines_to_sort.sort(key=lambda temp_line: temp_line.split(' ')[2])
        smallest_item = lines_to_sort[0]
        for key in sort_queue:
            if sort_queue[key] == smallest_item:
                sort_queue.pop(key)
                break
        merged_file.write(smallest_item)

    merged_file.close()
    for temp_file in temp_files_list:
        temp_file.close()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file_1_path', help='path to first file')
    arg_parser.add_argument('file_2_path', help='path to second file')
    arg_parser.add_argument('merged_file_path', help='path to merged file')

    args = arg_parser.parse_args()

    merge_files(args.file_1_path, args.file_2_path, args.merged_file_path)