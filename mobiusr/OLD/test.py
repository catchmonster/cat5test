##---------------------------------------------
## PROJECT: Cattest   FILE NAME: test
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 8/22/17:2:45 PM
##---------------------------------------------

import re as re_
import base64, sys
import datetime as datetime_
import warnings as warnings_

CurrentSubclassModule_ = None
ExternalEncoding = 'utf-8'
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

try:
	from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ImportError:
	GenerateDSNamespaceDefs_ = {}

Validate_simpletypes_ = True
if sys.version_info.major == 2:
	BaseStrType_ = basestring
else:
	BaseStrType_ = str


def quote_xml_aux(inStr):
	s1 = inStr.replace('&', '&amp;')
	s1 = s1.replace('<', '&lt;')
	s1 = s1.replace('>', '&gt;')
	return s1


class GDSParseError(Exception):
	pass


def showIndent(outfile, level, pretty_print=True):
	if pretty_print:
		for idx in range(level):
			outfile.write('    ')


def raise_parse_error(node, msg):
	msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline,)
	raise GDSParseError(msg)


def quote_xml(inStr):
	"Escape markup chars, but do not modify CDATA sections."
	if not inStr:
		return ''
	s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
	s2 = ''
	pos = 0
	matchobjects = CDATA_pattern_.finditer(s1)
	for mo in matchobjects:
		s3 = s1[pos:mo.start()]
		s2 += quote_xml_aux(s3)
		s2 += s1[mo.start():mo.end()]
		pos = mo.end()
	s3 = s1[pos:]
	s2 += quote_xml_aux(s3)
	return s2


class GeneratedsSuper(object):
	tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')

	class _FixedOffsetTZ(datetime_.tzinfo):
		def __init__(self, offset, name):
			self.__offset = datetime_.timedelta(minutes=offset)
			self.__name = name

		def utcoffset(self, dt):
			return self.__offset

		def tzname(self, dt):
			return self.__name

		def dst(self, dt):
			return None

	def gds_format_string(self, input_data, input_name=''):
		return input_data

	def gds_validate_string(self, input_data, node=None, input_name=''):
		if not input_data:
			return ''
		else:
			return input_data

	def gds_format_base64(self, input_data, input_name=''):
		return base64.b64encode(input_data)

	def gds_validate_base64(self, input_data, node=None, input_name=''):
		return input_data

	def gds_format_integer(self, input_data, input_name=''):
		return '%d' % input_data

	def gds_validate_integer(self, input_data, node=None, input_name=''):
		return input_data

	def gds_format_integer_list(self, input_data, input_name=''):
		return '%s' % ' '.join(input_data)

	def gds_validate_integer_list(
		self, input_data, node=None, input_name=''):
		values = input_data.split()
		for value in values:
			try:
				int(value)
			except (TypeError, ValueError):
				raise_parse_error(node, 'Requires sequence of integers')
		return values

	def gds_format_float(self, input_data, input_name=''):
		return ('%.15f' % input_data).rstrip('0')

	def gds_validate_float(self, input_data, node=None, input_name=''):
		return input_data

	def gds_format_float_list(self, input_data, input_name=''):
		return '%s' % ' '.join(input_data)

	def gds_validate_float_list(
		self, input_data, node=None, input_name=''):
		values = input_data.split()
		for value in values:
			try:
				float(value)
			except (TypeError, ValueError):
				raise_parse_error(node, 'Requires sequence of floats')
		return values

	def gds_format_double(self, input_data, input_name=''):
		return '%e' % input_data

	def gds_validate_double(self, input_data, node=None, input_name=''):
		return input_data

	def gds_format_double_list(self, input_data, input_name=''):
		return '%s' % ' '.join(input_data)

	def gds_validate_double_list(
		self, input_data, node=None, input_name=''):
		values = input_data.split()
		for value in values:
			try:
				float(value)
			except (TypeError, ValueError):
				raise_parse_error(node, 'Requires sequence of doubles')
		return values

	def gds_format_boolean(self, input_data, input_name=''):
		return ('%s' % input_data).lower()

	def gds_validate_boolean(self, input_data, node=None, input_name=''):
		return input_data

	def gds_format_boolean_list(self, input_data, input_name=''):
		return '%s' % ' '.join(input_data)

	def gds_validate_boolean_list(
		self, input_data, node=None, input_name=''):
		values = input_data.split()
		for value in values:
			if value not in ('true', '1', 'false', '0',):
				raise_parse_error(
					node,
					'Requires sequence of booleans '
					'("true", "1", "false", "0")')
		return values

	def gds_validate_datetime(self, input_data, node=None, input_name=''):
		return input_data

	def gds_format_datetime(self, input_data, input_name=''):
		if input_data.microsecond == 0:
			_svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
				input_data.year,
				input_data.month,
				input_data.day,
				input_data.hour,
				input_data.minute,
				input_data.second,
			)
		else:
			_svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
				input_data.year,
				input_data.month,
				input_data.day,
				input_data.hour,
				input_data.minute,
				input_data.second,
				('%f' % (float(input_data.microsecond) / 1000000))[2:],
			)
		if input_data.tzinfo is not None:
			tzoff = input_data.tzinfo.utcoffset(input_data)
			if tzoff is not None:
				total_seconds = tzoff.seconds + (86400 * tzoff.days)
				if total_seconds == 0:
					_svalue += 'Z'
				else:
					if total_seconds < 0:
						_svalue += '-'
						total_seconds *= -1
					else:
						_svalue += '+'
					hours = total_seconds // 3600
					minutes = (total_seconds - (hours * 3600)) // 60
					_svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
		return _svalue

	@classmethod
	def gds_parse_datetime(cls, input_data):
		tz = None
		if input_data[-1] == 'Z':
			tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
			input_data = input_data[:-1]
		else:
			results = GeneratedsSuper.tzoff_pattern.search(input_data)
			if results is not None:
				tzoff_parts = results.group(2).split(':')
				tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
				if results.group(1) == '-':
					tzoff *= -1
				tz = GeneratedsSuper._FixedOffsetTZ(
					tzoff, results.group(0))
				input_data = input_data[:-6]
		time_parts = input_data.split('.')
		if len(time_parts) > 1:
			micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
			input_data = '%s.%s' % (time_parts[0], micro_seconds,)
			dt = datetime_.datetime.strptime(
				input_data, '%Y-%m-%dT%H:%M:%S.%f')
		else:
			dt = datetime_.datetime.strptime(
				input_data, '%Y-%m-%dT%H:%M:%S')
		dt = dt.replace(tzinfo=tz)
		return dt

	def gds_validate_date(self, input_data, node=None, input_name=''):
		return input_data

	def gds_format_date(self, input_data, input_name=''):
		_svalue = '%04d-%02d-%02d' % (
			input_data.year,
			input_data.month,
			input_data.day,
		)
		try:
			if input_data.tzinfo is not None:
				tzoff = input_data.tzinfo.utcoffset(input_data)
				if tzoff is not None:
					total_seconds = tzoff.seconds + (86400 * tzoff.days)
					if total_seconds == 0:
						_svalue += 'Z'
					else:
						if total_seconds < 0:
							_svalue += '-'
							total_seconds *= -1
						else:
							_svalue += '+'
						hours = total_seconds // 3600
						minutes = (total_seconds - (hours * 3600)) // 60
						_svalue += '{0:02d}:{1:02d}'.format(
							hours, minutes)
		except AttributeError:
			pass
		return _svalue

	@classmethod
	def gds_parse_date(cls, input_data):
		tz = None
		if input_data[-1] == 'Z':
			tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
			input_data = input_data[:-1]
		else:
			results = GeneratedsSuper.tzoff_pattern.search(input_data)
			if results is not None:
				tzoff_parts = results.group(2).split(':')
				tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
				if results.group(1) == '-':
					tzoff *= -1
				tz = GeneratedsSuper._FixedOffsetTZ(
					tzoff, results.group(0))
				input_data = input_data[:-6]
		dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
		dt = dt.replace(tzinfo=tz)
		return dt.date()

	def gds_validate_time(self, input_data, node=None, input_name=''):
		return input_data

	def gds_format_time(self, input_data, input_name=''):
		if input_data.microsecond == 0:
			_svalue = '%02d:%02d:%02d' % (
				input_data.hour,
				input_data.minute,
				input_data.second,
			)
		else:
			_svalue = '%02d:%02d:%02d.%s' % (
				input_data.hour,
				input_data.minute,
				input_data.second,
				('%f' % (float(input_data.microsecond) / 1000000))[2:],
			)
		if input_data.tzinfo is not None:
			tzoff = input_data.tzinfo.utcoffset(input_data)
			if tzoff is not None:
				total_seconds = tzoff.seconds + (86400 * tzoff.days)
				if total_seconds == 0:
					_svalue += 'Z'
				else:
					if total_seconds < 0:
						_svalue += '-'
						total_seconds *= -1
					else:
						_svalue += '+'
					hours = total_seconds // 3600
					minutes = (total_seconds - (hours * 3600)) // 60
					_svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
		return _svalue

	def gds_validate_simple_patterns(self, patterns, target):
		# pat is a list of lists of strings/patterns.  We should:
		# - AND the outer elements
		# - OR the inner elements
		found1 = True
		for patterns1 in patterns:
			found2 = False
			for patterns2 in patterns1:
				if re_.search(patterns2, target) is not None:
					found2 = True
					break
			if not found2:
				found1 = False
				break
		return found1

	@classmethod
	def gds_parse_time(cls, input_data):
		tz = None
		if input_data[-1] == 'Z':
			tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
			input_data = input_data[:-1]
		else:
			results = GeneratedsSuper.tzoff_pattern.search(input_data)
			if results is not None:
				tzoff_parts = results.group(2).split(':')
				tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
				if results.group(1) == '-':
					tzoff *= -1
				tz = GeneratedsSuper._FixedOffsetTZ(
					tzoff, results.group(0))
				input_data = input_data[:-6]
		if len(input_data.split('.')) > 1:
			dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
		else:
			dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
		dt = dt.replace(tzinfo=tz)
		return dt.time()

	def gds_str_lower(self, instring):
		return instring.lower()

	def get_path_(self, node):
		path_list = []
		self.get_path_list_(node, path_list)
		path_list.reverse()
		path = '/'.join(path_list)
		return path

	Tag_strip_pattern_ = re_.compile(r'\{.*\}')

	def get_path_list_(self, node, path_list):
		if node is None:
			return
		tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
		if tag:
			path_list.append(tag)
		self.get_path_list_(node.getparent(), path_list)

	def get_class_obj_(self, node, default_class=None):
		class_obj1 = default_class
		if 'xsi' in node.nsmap:
			classname = node.get('{%s}type' % node.nsmap['xsi'])
			if classname is not None:
				names = classname.split(':')
				if len(names) == 2:
					classname = names[1]
				class_obj2 = globals().get(classname)
				if class_obj2 is not None:
					class_obj1 = class_obj2
		return class_obj1

	def gds_build_any(self, node, type_name=None):
		return None

	@classmethod
	def gds_reverse_node_mapping(cls, mapping):
		return dict(((v, k) for k, v in mapping.iteritems()))

	@staticmethod
	def gds_encode(instring):
		if sys.version_info.major == 2:
			return instring.encode(ExternalEncoding)
		else:
			return instring

	@staticmethod
	def convert_unicode(instring):
		if isinstance(instring, str):
			result = quote_xml(instring)
		elif sys.version_info.major == 2 and isinstance(instring, unicode):
			result = quote_xml(instring).encode('utf8')
		else:
			result = GeneratedsSuper.gds_encode(str(instring))
		return result

	def __eq__(self, other):
		if type(self) != type(other):
			return False
		return self.__dict__ == other.__dict__

	def __ne__(self, other):
		return not self.__eq__(other)


def getSubclassFromModule_(module, class_):
	'''Get the subclass of a class from a specific module.'''
	name = class_.__name__ + 'Sub'
	if hasattr(module, name):
		return getattr(module, name)
	else:
		return None


class comments(GeneratedsSuper):
	member_data_items_ = {
	}
	subclass = None
	superclass = None

	def __init__(self):
		self.original_tagname_ = None

	def factory(*args_, **kwargs_):
		if CurrentSubclassModule_ is not None:
			subclass = getSubclassFromModule_(
				CurrentSubclassModule_, comments)
			if subclass is not None:
				return subclass(*args_, **kwargs_)
		if comments.subclass:
			return comments.subclass(*args_, **kwargs_)
		else:
			return comments(*args_, **kwargs_)

	factory = staticmethod(factory)

	def hasContent_(self):
		if (

		):
			return True
		else:
			return False

	def export(self, outfile, level, namespace_='', name_='comments', namespacedef_='', pretty_print=True):
		imported_ns_def_ = GenerateDSNamespaceDefs_.get('comments')
		if imported_ns_def_ is not None:
			namespacedef_ = imported_ns_def_
		if pretty_print:
			eol_ = '\n'
		else:
			eol_ = ''
		if self.original_tagname_ is not None:
			name_ = self.original_tagname_
		showIndent(outfile, level, pretty_print)
		outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '',))
		already_processed = set()
		self.exportAttributes(outfile, level, already_processed, namespace_, name_='comments')
		if self.hasContent_():
			outfile.write('>%s' % (eol_,))
			self.exportChildren(outfile, level + 1, namespace_='', name_='comments', pretty_print=pretty_print)
			outfile.write('</%s%s>%s' % (namespace_, name_, eol_))
		else:
			outfile.write('/>%s' % (eol_,))

	def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='comments'):
		pass

	def exportChildren(self, outfile, level, namespace_='', name_='comments', fromsubclass_=False, pretty_print=True):
		pass

	def build(self, node):
		already_processed = set()
		self.buildAttributes(node, node.attrib, already_processed)
		for child in node:
			nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
			self.buildChildren(child, node, nodeName_)
		return self

	def buildAttributes(self, node, attrs, already_processed):
		pass

	def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
		pass

	# end class comments


def main():
	c = comments()
	c.
	c.export('blvah', 0)


if __name__ == '__main__':
	# import pdb; pdb.set_trace()
	main()
