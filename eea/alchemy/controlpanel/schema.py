""" Custom zope schema
"""
import json
from zope.interface import Interface
from zope.interface import implements
from zope.formlib.textwidgets import TextWidget
from zope.formlib.widget import renderElement
from zope.formlib.interfaces import ConversionError
from plone.app.form.widgets import ListSequenceWidget
from zope.schema.interfaces import IList
from zope.schema.interfaces import IFromUnicode
from plone.registry.field import List as ListRegistry
from plone.app.registry.exportimport.fields import PersistentFieldHandler

from zope import schema

#class ITable(IList):
    #""" Interface for Table field
    #"""

class ITableRow(IFromUnicode):
    """ Interface for TableRow field
    """

#class Table(schema.List):
    #""" Table field
    #"""
    #implements(ITable)

class TableRow(schema.TextLine):
    """ Pair of values
    """
    cells = 2
    delimiter = u'=>'
    implements(ITableRow)

class TableRowWidget(TextWidget):
    """ Widget
    """
    def __call__(self):
        res = u''
        value = self._getFormValue()
        if value is None or value == self.context.missing_value:
            value = []

        if isinstance(value, (str, unicode)):
            value = value.split(self.context.delimiter)

        for cell in range(0, self.context.cells):
            kwargs = {'type': self.type,
                      'name': self.name,
                      'id': self.name + '%s' % cell,
                      'value': value[cell] if len(value) > cell else u'',
                      'cssClass': self.cssClass,
                      'style': self.style,
                      'size': self.displayWidth,
                      'extra': self.extra
                      }
            if self.displayMaxWidth:
                kwargs['maxlength'] = self.displayMaxWidth

            res += renderElement(self.tag, **kwargs)
        return res

    def _toFieldValue(self, input):
        if self.convert_missing_value and input == self._missing:
            value = self.context.missing_value
        else:
            # We convert everything to unicode. This might seem a bit crude,
            # but anything contained in a TextWidget should be representable
            # as a string. Note that you always have the choice of overriding
            # the method.
            if isinstance(input, (list, tuple)):
                input = self.context.delimiter.join(input)

            try:
                value = unicode(input)
            except ValueError, v:
                raise ConversionError(_("Invalid text data"), v)
        return value

class TableWidget(ListSequenceWidget):
    """ Custom widget for table
    """
    def _getPresenceMarker(self, count=0):
        try:
            return super(TableWidget, self)._getPresenceMarker(count=count)
        except Exception:
            orig = ' originalValue="0"'
            return ('<input type="hidden" name="%s.count" value="%d"%s />' % (
                self.name, count, orig))
