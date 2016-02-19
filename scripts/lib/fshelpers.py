# -*- Mode: Python; indent-tabs-mode: t; python-indent: 4; tab-width: 4 -*-
"""ACYLS functiont to work with file system"""

import os
import shutil
from base import IconFinder


class Prospector(IconFinder):
	""""Find icons on diffrent deep level in directory tree"""
	def __init__(self, root):
		self.root = root
		self.structure = {0: dict(zip(('root', 'directories'), next(os.walk(root))))}

	def dig(self, name, level):
		"""Choose active directory on given level"""
		if level - 1 in self.structure and name in self.structure[level - 1]['directories']:
			dest = os.path.join(self.structure[level - 1]['root'], name)
			self.structure[level] = dict(zip(('root', 'directories'), next(os.walk(dest))))
			self.structure[level]['directories'].sort()
			self.structure = {key: self.structure[key] for key in self.structure if key <= level}

	def get_icons(self, level):
		"""Get icon list from given level"""
		if level in self.structure:
			return self.get_svg_all(self.structure[level]['root'])

	def send_icons(self, level, dest):
		"""Merge files form given level to destination place"""
		if level in self.structure:
			source_root_dir = self.structure[level]['root']
			for source_dir, _, files in os.walk(source_root_dir):
				destination_dir = source_dir.replace(source_root_dir, dest)
				for file_ in files:
					shutil.copy(os.path.join(source_dir, file_), destination_dir)


class FileKeeper:
	"""Helper to work with user files.
	Trying to get file from current user directory, copy from backup directory if not found.
	"""
	def __init__(self, bakdir, curdir):
		self.bakdir = bakdir
		self.curdir = curdir

	def get(self, name):
		"""Get file by name"""
		fullname = os.path.join(self.curdir, name)
		if not os.path.isfile(fullname):
			shutil.copy(os.path.join(self.bakdir, name), self.curdir)
		return fullname
