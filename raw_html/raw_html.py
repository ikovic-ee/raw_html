"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment
from webob.response import Response

from xblock_django.mixins import FileUploadMixin


class RawHtmlXBlock(XBlock, FileUploadMixin):
    content_text = String(help="Raw HTML content", default='', scope=Scope.content)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the RawHtmlXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/raw_html.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/raw_html.css"))
        frag.add_javascript(self.resource_string("static/js/src/raw_html.js"))
        frag.initialize_js('RawHtmlXBlock')
        return frag

    def studio_view(self, context=None):
        """
        The primary view of the TextImageXBlock, shown to students
        when viewing courses.
        """
        html_str = pkg_resources.resource_string(__name__, "static/html/studio_view.html")
        # display variables
        frag = Fragment(unicode(html_str).format(self=self))

        frag.add_css(self.resource_string("static/css/textimagexblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/studio_view.js"))
        frag.initialize_js('StudioEditSubmit')

        return frag

    @XBlock.handler
    def studio_submit(self, request, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        data = request.POST

        self.display_name = data['display_name']
        self.display_description = data['display_description']
        self.content_text = data['content_text']

        block_id = data['usage_id']
        if not isinstance(data['thumbnail'], basestring):
            upload = data['thumbnail']
            self.thumbnail_url = self.upload_to_s3('THUMBNAIL', upload.file, block_id, self.thumbnail_url)

        return Response(json_body={'result': 'success'})
