


def to_bytes(data, encoding='utf-8'):
    """
    Converts the input data to bytes.

    Args:
        data: The input data to be converted. Can be of type str, int, float, or bytes.
        encoding: The encoding to use if the input is a string. Default is 'utf-8'.

    Returns:
        Bytes representation of the input data.

    Raises:
        TypeError: If the input data type is not supported.
    """
    if isinstance(data, bytes):
        return data
    elif isinstance(data, str):
        return data.encode(encoding)
    elif isinstance(data, (int, float)):
        return str(data).encode(encoding)
    else:
        raise TypeError(f"Unsupported data type: {type(data)}")
    



def to_file_format(data, file_format, encoding='utf-8'):
    """
    Converts the input data to bytes and appends the appropriate file format header.

    Args:
        data: The input data to be converted. Can be of type str, int, float, or bytes.
        file_format: The desired file format. Supported formats are 'png', 'jpeg', 'avi', 'mp4', 'mp3'.
        encoding: The encoding to use if the input is a string. Default is 'utf-8'.

    Returns:
        Bytes representation of the input data with the file format header.

    Raises:
        ValueError: If the file format is not supported.
    """
    file_headers = {
        'png': b'\x89PNG\r\n\x1a\n',
        'jpeg': b'\xff\xd8\xff',
        'jpg': b'\xff\xd8\xff',
        'avi': b'RIFF\x00\x00\x00\x00AVI ',
        'mp4': b'\x00\x00\x00\x18ftypmp42',
        'mp3': b'ID3',
        'gif': b'GIF89a',
        'bmp': b'BM',
        'wav': b'RIFF\x00\x00\x00\x00WAVE',
        'pdf': b'%PDF-',
        'zip': b'PK\x03\x04',
        'tar': b'ustar',
        '7z': b'7z\xbc\xaf\x27\x1c',
        'rar': b'Rar!\x1a\x07\x00',
        'exe': b'MZ',
        'dll': b'MZ',
        'txt': b'',
        'csv': b'',
        'json': b'',
        'xml': b'<?xml',
        'html': b'<!DOCTYPE html',
        'xlsx': b'PK\x03\x04',
        'docx': b'PK\x03\x04',
        'pptx': b'PK\x03\x04',
        'epub': b'PK\x03\x04',
        'flac': b'fLaC',
        'ogg': b'OggS',
        'ico': b'\x00\x00\x01\x00',
        'tiff': b'II*\x00',
        'psd': b'8BPS',
        'rtf': b'{\\rtf',
        'sqlite': b'SQLite format 3\x00',
        'apk': b'PK\x03\x04',
        'ipa': b'PK\x03\x04',
        'deb': b'!<arch>',
        'rpm': b'\xed\xab\xee\xdb',
        'iso': b'CD001',
        'dmg': b'xar!',
        'mov': b'\x00\x00\x00\x14ftypqt  ',
        'webm': b'\x1a\x45\xdf\xa3',
        'mkv': b'\x1a\x45\xdf\xa3',
        'ts': b'\x47',
        'm3u8': b'#EXTM3U',
        'svg': b'<?xml',
        'md': b'',
        'yaml': b'',
        'yml': b'',
        'ini': b'',
        'log': b'',
        'bat': b'@echo off',
        'sh': b'#!/bin/bash',
        'py': b'#!/usr/bin/env python',
        'java': b'',
        'c': b'',
        'cpp': b'',
        'cs': b'',
        'js': b'',
        'ts': b'',
        'php': b'<?php',
        'rb': b'#!/usr/bin/env ruby',
        'go': b'',
        'rs': b'',
        'swift': b'',
        'kt': b'',
        'dart': b'',
        'jsonl': b'',
        'ndjson': b'',
        'parquet': b'PAR1',
        'orc': b'ORC',
        'avro': b'Obj\x01',
        'feather': b'ARROW1',
        'arrow': b'ARROW1',
        'pickle': b'\x80',
        'pkl': b'\x80',
        'h5': b'\x89HDF\r\n\x1a\n',
        'hdf5': b'\x89HDF\r\n\x1a\n',
        'mat': b'MATLAB 5.0 MAT-file',
        'sav': b'$FL2',
        'spss': b'$FL2',
        'sas7bdat': b'SAS7BDAT',
        'dta': b'<stata_dta>',
        'rdata': b'RDX2',
        'rds': b'X\n',
        'sqlite3': b'SQLite format 3\x00',
        'db': b'SQLite format 3\x00',
        'msg': b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1',
        'eml': b'',
        'ics': b'BEGIN:VCALENDAR',
        'vcf': b'BEGIN:VCARD',
        'ics': b'BEGIN:VCALENDAR',
        'ics': b'BEGIN:VCALENDAR',
    }

    if file_format not in file_headers:
        raise ValueError(f"Unsupported file format: {file_format}")

    data_bytes = to_bytes(data, encoding)
    return file_headers[file_format] + data_bytes