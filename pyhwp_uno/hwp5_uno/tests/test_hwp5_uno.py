# -*- coding: utf-8 -*-
from unittest import TestCase
from unokit.remote import RemoteContextLayer


class TestBase(TestCase):

    layer = RemoteContextLayer


class OleStorageAdapterTest(TestBase):

    def get_adapter(self):
        from unokit.services import css
        from hwp5_uno import InputStreamFromFileLike
        from hwp5_uno import OleStorageAdapter
        f = file('fixtures/sample-5017.hwp', 'r')
        inputstream = InputStreamFromFileLike(f)
        oless = css.embed.OLESimpleStorage(inputstream)
        return OleStorageAdapter(oless)

    def test_iter(self):
        adapter = self.get_adapter()

        self.assertTrue('FileHeader' in adapter)
        self.assertTrue('DocInfo' in adapter)
        self.assertTrue('BodyText' in adapter)

    def test_getitem(self):
        adapter = self.get_adapter()

        bodytext = adapter['BodyText']
        self.assertTrue('Section0' in bodytext)

        from hwp5.filestructure import HwpFileHeader
        from hwp5.filestructure import HWP5_SIGNATURE

        fileheader = adapter['FileHeader']
        fileheader = HwpFileHeader(fileheader)
        self.assertEquals((5, 0, 1, 7), fileheader.version)
        self.assertEquals(HWP5_SIGNATURE, fileheader.signature)

        # reopen (just being careful)
        fileheader = adapter['FileHeader']
        fileheader = HwpFileHeader(fileheader)
        self.assertEquals((5, 0, 1, 7), fileheader.version)
        self.assertEquals(HWP5_SIGNATURE, fileheader.signature)


class HwpFileFromInputStreamTest(TestBase):

    def test_basic(self):
        from unokit.adapters import InputStreamFromFileLike
        from hwp5_uno import HwpFileFromInputStream
        with file('fixtures/sample-5017.hwp', 'r') as f:
            inputstream = InputStreamFromFileLike(f)
            hwpfile = HwpFileFromInputStream(inputstream)
            self.assertEquals((5, 0, 1, 7), hwpfile.fileheader.version)


class StorageFromInputStreamTest(TestBase):

    def test_basic(self):
        import uno
        from unokit.adapters import InputStreamFromFileLike
        from hwp5_uno import StorageFromInputStream
        from hwp5.hwp5odt import ODTPackage

        zipname = self.id()+'.zip'

        pkg = ODTPackage(zipname)
        try:
            from StringIO import StringIO
            data = StringIO('hello')
            pkg.insert_stream(data, 'abc.txt', 'text/plain')
        finally:
            pkg.close()

        with file(zipname, 'rb') as f:
            inputstream = InputStreamFromFileLike(f, dontclose=True)
            storage = StorageFromInputStream(inputstream)
            try:
                self.assertTrue(uno.getTypeByName('com.sun.star.embed.XStorage')
                                in storage.Types)
                self.assertEquals(set(['abc.txt']), set(storage.ElementNames))
            finally:
                storage.dispose()


class TypedetectTest(TestBase):
    def test_basic(self):
        from unokit.adapters import InputStreamFromFileLike
        from hwp5_uno import inputstream_is_hwp5file
        from hwp5_uno import typedetect
        with file('fixtures/sample-5017.hwp', 'rb') as f:
            inputstream = InputStreamFromFileLike(f, dontclose=True)
            self.assertTrue(inputstream_is_hwp5file(inputstream))
            self.assertEquals('hwp5', typedetect(inputstream))


class LoadHwp5FileTest(TestBase):

    def get_paragraphs(self, text):
        import unokit.util
        return unokit.util.enumerate(text)

    def get_text_portions(self, paragraph):
        import unokit.util
        return unokit.util.enumerate(paragraph)

    def get_text_contents(self, text_portion):
        import unokit.util
        if hasattr(text_portion, 'createContentEnumeration'):
            xenum = text_portion.createContentEnumeration('com.sun.star.text.TextContent')
            for text_content in unokit.util.iterate(xenum):
                yield text_content

    def test_basic(self):
        from unokit.services import css
        import unokit.util
        from hwp5.xmlmodel import Hwp5File
        from hwp5_uno import load_hwp5file_into_doc

        desktop = css.frame.Desktop()
        doc = desktop.loadComponentFromURL('private:factory/swriter', '_blank',
                                           0, tuple())
        hwp5file = Hwp5File('fixtures/sample-5017.hwp')

        load_hwp5file_into_doc(hwp5file, doc)

        text = doc.getText()

        paragraphs = list(self.get_paragraphs(text))

        p = paragraphs[0]
        text_portions = list(self.get_text_portions(p))
        tp = text_portions[0]
        self.assertEquals('Text', tp.TextPortionType)
        self.assertEquals(u'한글 ', tp.String)

        p = paragraphs[-1]
        tp = list(self.get_text_portions(p))[-1]
        self.assertEquals('Frame', tp.TextPortionType)
        tc = list(self.get_text_contents(tp))[-1]
        self.assertTrue('com.sun.star.drawing.GraphicObjectShape' in
                        tc.SupportedServiceNames)

        table = paragraphs[6]
        self.assertTrue('com.sun.star.text.TextTable' in
                        table.SupportedServiceNames)

        drawpage = doc.getDrawPage()
        shapes = list(unokit.util.enumerate(drawpage))

        self.assertEquals(2, len(shapes))

        self.assertEquals(1, shapes[0].Graphic.GraphicType)
        self.assertEquals('image/jpeg', shapes[0].Graphic.MimeType)
        self.assertEquals(2, shapes[0].Bitmap.GraphicType)
        self.assertEquals('image/x-vclgraphic', shapes[0].Bitmap.MimeType)
        self.assertEquals(28254, len(shapes[0].Bitmap.DIB))
        self.assertEquals('vnd.sun.star.GraphicObject:10000000000001F40000012C1F9CCF04',
                          shapes[0].GraphicURL)
        self.assertEquals(None, shapes[0].GraphicStreamURL)

        self.assertEquals(1, shapes[1].Graphic.GraphicType)
        self.assertEquals('image/png', shapes[1].Graphic.MimeType)
        self.assertEquals(2, shapes[1].Bitmap.GraphicType)
        self.assertEquals('image/x-vclgraphic', shapes[1].Bitmap.MimeType)
        self.assertEquals(374, len(shapes[1].Bitmap.DIB))
        self.assertEquals('vnd.sun.star.GraphicObject:1000020100000010000000108F049D12',
                          shapes[1].GraphicURL)
        self.assertEquals(None, shapes[1].GraphicStreamURL)