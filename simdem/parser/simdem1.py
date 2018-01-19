""" This module hosts the ContextParser
"""

import logging
from collections import defaultdict
from mistletoe.base_renderer import BaseRenderer
from mistletoe import Document


class SimDem1Parser(object): # pylint: disable=R0903
    """ Parses markdown based off of Mistletoe renderer """

    @staticmethod
    def parse_file(file_path):
        """ The main meat for parsing the file. """
        with open(file_path, 'r') as fin:
            with SimDemMistletoeRenderer() as renderer:
                rendered = renderer.render(Document(fin))

        # Do stuff here
        return rendered


class SimDemMistletoeRenderer(BaseRenderer):
    """ Based off of https://gist.github.com/miyuchina/a06bd90d91b70be0906266760547da62
        Major Gotcha:  If this class calls a function that does not exist, it will NOT error
        This is due to the way that the Mistletoe Renderer works.  Or at least how I think it works.
    """
    section = None
    block = None

    def __init__(self):
        super().__init__()
        self.output = defaultdict(list)
        self.reset_section()

    def render_heading(self, token):
        """ Render for Heading: # """
        inner = self.render_inner(token)
        content = {'type': 'heading', 'level': token.level, 'content': inner}
        self.append_body(content)

        # Prerequisite Heading
        if inner.lower() == 'prerequisites':
            self.set_section('prerequisites')

        # Next Steps Heading
        elif inner.lower() == 'next steps':
            self.set_section('next_steps')

        # Validation Heading
        elif inner.lower() == 'validation':
            self.set_section('validation')

        else:
            logging.debug("parse_file():unable to determing header type.")
            self.reset_section()
        return inner

    def render_list(self, token):
        """ Render a markdown list """
        inner = self.render_inner(token)
        return inner

    def render_list_item(self, token):
        """ Render a markdown list item """
        inner = self.render_inner(token)
        return inner

    def render_link(self, token):
        """ Due to the way the parser works, we can only return strings
            We need to find another way to store link targets.
            Unfortunately, I can only think of storing them in an array right now
        """
        inner = self.render_inner(token)
        if self.section and 'next_steps' in self.section:
            self.append_next_step(inner, token.target)
        if self.section and 'prerequisites' in self.section:
            self.append_prereq(token.target)
        return inner

    def render_raw_text(self, token):
        """ Render raw text.  The only thing to look for is the result text indicator """
        if token.content == 'Results:':
            self.set_block('results')
            return ''
        return token.content

    def render_paragraph(self, token):
        """ Render for Paragraph """
        inner = self.render_inner(token)
        if inner:
            body = {'type': 'text', 'content': inner}
            self.append_body(body)
        return ''

    def render_block_code(self, token):
        """ Render a markdown block code """
        #lines = token.children[0].content.splitlines()
        content = token.children[0].content

        if self.section == 'validation':
            # Validation blocks aren't run like normal blocks
            if self.block == 'results':
                # Validation result blocks are expecially not checked like normal blocks
                self.set_validation_result(content)
            else:
                self.set_validation_command(content)
        else:
            if self.block == 'results':
                # Assume that the last body item is the command we're expecting results for
                self.output['body'][-1]['expected_result'] = content
            else:
                # Assume this is a normal code block to run block
                content = {'type': 'commands', 'content': content.splitlines()}
                self.append_body(content)

        inner = self.render_inner(token)
        # After this code block, reset the block type (e.g. No longer a "Result block")
        self.set_block(None)

        return inner

    def render_document(self, token):
        """ Render the entire markdown document """
        self.render_inner(token)
        return dict(self.output)

    def __getattr__(self, name):
        return lambda token: ''

    # Everything below here is boring setters

    def reset_section(self):
        """ If we encounter a new section, reset everything we know """
        self.section = None
        self.block = None

    def set_section(self, section):
        """ Set the section to the section name.  Duh """
        logging.debug('set_section(' + str(section) + ')')
        self.section = section

    def set_block(self, block):
        """ Set the block to the block name.  Duh """
        logging.debug('set_block(' + str(block) + ')')
        self.block = block

    def set_validation_command(self, cmds):
        """ Assuming validation commands should be a list """
        logging.debug('append_validation(' + str(cmds) + ')')
        self.output['validation'] = {'commands': cmds.splitlines()}

    def set_validation_result(self, result):
        """ Assuming validation results should be a list """
        logging.debug('append_validation(' + str(result) + ')')
        self.output['validation']['expected_result'] = result

    def append_body(self, body):
        """ Adding the meat of the work to the dict """
        logging.debug('append_body(' + str(body) + ')')
        self.output['body'].append(body)

    def append_prereq(self, target):
        """ Set Prereqs """
        logging.debug('append_prereq(' + target + ')')
        self.output['prerequisites'].append(target)

    def append_next_step(self, name, target):
        """ Add steps to next step section """
        logging.debug('append_next_step(' + name + ',' + target + ')')
        self.output['next_steps'].append({'title': name, 'target': target})
