from unittest import TestCase

import logging

from archerdfu.core import find, dfu_progress
from pydfuutil.logger import logger

logger.setLevel(logging.DEBUG)


class TestDfuDevice(TestCase):

    def setUp(self):
        self.dev = find(False)
        self.dev.connect()

    def tearDown(self):
        self.dev.disconnect()

    # def test_upload_info(self):
    #     usb_page = 2048
    #     spi_fi_chunk = 4096
    #     info_size = 4 * spi_fi_chunk
    #     info_offset = 130 * spi_fi_chunk
    #
    #     # Call methods that internally use dfu._upload
    #     h1 = self.dev.do_upload(
    #         info_offset,
    #         spi_fi_chunk, usb_page
    #     )
    #     d1 = self.dev.do_upload(
    #         info_offset + spi_fi_chunk,
    #         info_size, usb_page
    #     )
    #
    #     print(len(h1), len(d1))
    #
    #     # Assert the first bytes to check correctness
    #     self.assertEqual(d1[:6], b'ARCHER')

    @dfu_progress
    def test_upload_mem_table(self):
        usb_page = 2048
        spi_fi_chunk = 4096
        mem_table_size = 3 * spi_fi_chunk
        mem_table_offset = (2 + 64) * spi_fi_chunk
        h1 = self.dev.do_upload(
            mem_table_offset,
            spi_fi_chunk, usb_page
        )
        d1 = self.dev.do_upload(
            mem_table_offset + spi_fi_chunk,
            mem_table_size - spi_fi_chunk, usb_page
        )

        self.assertEqual(len(h1), spi_fi_chunk)
        self.assertEqual(len(d1), mem_table_size-spi_fi_chunk)

        r1 = self.dev.do_download(
            mem_table_offset,
            h1, usb_page
        )
        self.assertEqual(r1, len(h1))
        self.dev.get_status()

        r2 = self.dev.do_download(
            mem_table_offset + spi_fi_chunk,
            d1, usb_page
        )
        self.assertEqual(r2, len(d1))
        self.dev.get_status()

        h2 = self.dev.do_upload(
            mem_table_offset,
            spi_fi_chunk, usb_page
        )
        self.assertEqual(h1, h2)
        self.dev.get_status()

        d2 = self.dev.do_upload(
            mem_table_offset + spi_fi_chunk,
            mem_table_size - spi_fi_chunk, usb_page
        )
        self.assertEqual(d1, d2)
        self.dev.get_status()
