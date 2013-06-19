# Tools
import jinja2
import os
import Comm

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates/"),
    extensions=['jinja2.ext.autoescape'])


def render(self, template_values, template_url):
    template = JINJA_ENVIRONMENT.get_template(template_url)
    self.response.write(template.render(template_values))

errorTemplate = "error.html"
def renderError(self, code, message):
    template = JINJA_ENVIRONMENT.get_template(errorTemplate)
    self.response.write(template.render({'code':code,'message':message}))

stream_manager = Comm.streamer()