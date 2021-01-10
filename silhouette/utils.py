import tempfile
import os as _os
import shutil as _shutil
import errno as _errno
import weakref as _weakref
import types as _types

class FileModifierError(Exception):
    pass

class FileModifier(object):

    def __init__(self, fname):
        self.__write_dict = {}
        self.__filename = fname
        self.__tempfile = tempfile.TemporaryFile()
        with open(fname, 'rb') as fp:
            for line in fp:
                self.__tempfile.write(line)
        self.__tempfile.seek(0)

    def write(self, s, line_number = 'END'):
        if line_number != 'END' and not isinstance(line_number, (int, float)):
            raise FileModifierError("Line number %s is not a valid number" % line_number)
        try:
            self.__write_dict[line_number].append(s)
        except KeyError:
            self.__write_dict[line_number] = [s]

    def writeline(self, s, line_number = 'END'):
        self.write('%s\n' % s, line_number)

    def writelines(self, s, line_number = 'END'):
        for ln in s:
            self.writeline(s, line_number)

    def __popline(self, index, fp):
        try:
            ilines = self.__write_dict.pop(index)
            for line in ilines:
                fp.write(line)
        except KeyError:
            pass

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        with open(self.__filename,'w') as fp:
            for index, line in enumerate(self.__tempfile.readlines()):
                self.__popline(index, fp)
                fp.write(line)
            for index in sorted(self.__write_dict):
                for line in self.__write_dict[index]:
                    fp.write(line)
        self.__tempfile.close()

class TemporaryDirectoryV2(object):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:
        with TemporaryDirectoryV2() as tmpdir:
            ...
    Upon exiting the context, the directory and everything contained
    in it are removed.
    """

    def __init__(self, suffix=None, prefix=None, dir=None):
        self.name = tempfile.mkdtemp(suffix, prefix, dir)
        self._finalizer = _weakref.finalize(
            self, self._cleanup, self.name,
            warn_message="Implicitly cleaning up {!r}".format(self))

    @classmethod
    def _rmtree(cls, name):
        def onerror(func, path, exc_info):
            if issubclass(exc_info[0], PermissionError):
                def resetperms(path):
                    try:
                        _os.chflags(path, 0)
                        _os.chmod(path, stat.S_IWRITE)
                    except AttributeError:
                        pass
                    _os.chmod(path, 0o700)

                try:
                    if path != name:
                        resetperms(_os.path.dirname(path))
                    resetperms(path)

                    try:
                        _os.unlink(path)
                    # PermissionError is raised on FreeBSD for directories
                    except (IsADirectoryError, PermissionError):
                        cls._rmtree(path)
                except FileNotFoundError:
                    pass
            elif issubclass(exc_info[0], FileNotFoundError):
                pass
            else:
                raise

        _shutil.rmtree(name, onerror=onerror)

    @classmethod
    def _cleanup(cls, name, warn_message):
        cls._rmtree(name)
        _warnings.warn(warn_message, ResourceWarning)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def cleanup(self):
        if self._finalizer.detach():
            self._rmtree(self.name)