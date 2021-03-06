#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

import sys

from mr_csv_worker.error_tracer import print_error


class CsvWorker:
    """ class for read and write csv files """

    def __init__(self):
        self.report = 'no report'

    def __str__(self):
        return "%s" % self.report

    def get_rows_list_from_csv(self, csv_file_path, encoding, delimiter=';',
                               start_row=0, end_row=None):
        """
        Get list of rows from CSV

        Parameters
        ----------
        :param csv_file_path: full path to source csv file
        :param encoding: csv file encoding
        :param start_row: 0 is defaul value
        :param end_row: max limit of rows - should be positive integer
        :param delimiter: columns delimiter

        """
        result = []
        try:
            with open(csv_file_path, 'r', encoding=encoding) as source_csv:
                data = source_csv.read().splitlines(True)
            if not end_row:
                end_row = len(data) - 1
            print(start_row, end_row)
            for idx, line in enumerate(data[start_row:end_row]):
                row = line.split(delimiter)
                result.append(row)
            print("result:  %s " % result)

            self.report = "File was read. There are %s row(s)" % len(result)
            return result
        except FileNotFoundError:
            print("File for READ with name '%s' was not found!" % csv_file_path)
            print_error()
            self.report = "Sorry, but i can't open file to read."
            return result
        except Exception as e:
            print(e)
            print_error(exception_info=sys.exc_info())
            self.report = "Sorry, but i can't read this file. Please check logs."
            return result

    def write_rows_from_list_of_dict(self, csv_file_path, fields_names_list,
                                     list_of_dict, print_header=True, delimiter=';'):
        """
        Print

        Parameters
        ----------
        :param csv_file_path: full path to source csv file
        :param fields_names_list: This values become a header or CSV file if header is enabled
        :param list_of_dict: List of dict - with key value == values from fields_names_list
        :param print_header: should i print header (first row) or not?
        :param delimiter: columns delimiter

        """
        try:
            with open(csv_file_path, 'w') as target_csv:
                writer = csv.DictWriter(target_csv, fieldnames=fields_names_list, delimiter=delimiter)
                if print_header:
                    writer.writeheader()
                if list_of_dict:
                    for row_dict in list_of_dict:
                        writer.writerow(rowdict=row_dict)
                    self.report = "'%s' file was wrote" % csv_file_path
                else:
                    self.report = "No incoming data for print. Please send me list of dict (rows)"
        except FileNotFoundError:
            error_text = "Wrong filename or incorrect PATH: %s" % csv_file_path
            print(error_text)
            self.report = error_text
        except PermissionError:
            error_text = "I have NO ACCESS save new CSV file to this location: %s" % csv_file_path
            print(error_text)
            self.report = error_text
        except Exception as e:
            print(e)
            print_error()
            error_text = "Can't write dict into file %s" % csv_file_path
            self.report = error_text
            self.report = error_text
