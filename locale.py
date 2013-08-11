
import re
import datetime
import sublime
import sublime_plugin


class SublimeLocaleListener(sublime_plugin.EventListener):
    should_run = True

    def on_selection_modified_async(self, view):
        if self.should_run:
            print('running...')
            view.run_command('locale')
            self.should_run = False
            sublime.set_timeout_async(self.allow_run, 10000)

    def allow_run(self):
        self.should_run = True


class LocaleCommand(sublime_plugin.TextCommand):
    last_run = None

    def run(self, view):
        if not self.last_run:
            self.get_locale()
        else:
            if (datetime.datetime.now() - self.last_run).seconds > 5:
                self.get_locale()

    def get_locale(self):
        s = self.view.substr(sublime.Region(0, self.view.sel()[0].a))

        locale = None
        if self.in_python():
            locale = self.find_python_class(s)
        elif self.in_php():
            locale = self.find_php_class(s)
            print('php locale: {v}'.format(v=locale))

        self.set_locale(locale)
        self.last_run = datetime.datetime.now()

    def find_python_class(self, str_):
        matches = re.findall(r'\s*class\s(\w+)\(', str_)
        try:
            return matches[-1]
        except IndexError:
            return None

    def find_php_class(self, str_):
        matches = re.findall(r'\s*class\s(\w+)\b', str_)
        try:
            return matches[-1]
        except IndexError:
            return None

    def set_locale(self, locale):
        if not locale:
            self.view.erase_status('sublime_locale')
            return

        s = "Locale: %s" % locale
        self.view.set_status('sublime_locale', s)

    def current_scope(self):
        return self.view.scope_name(0)

    def in_python(self):
        return 'python' in self.current_scope()

    def in_php(self):
        return 'source.php' in self.current_scope()

    def in_js(self):
        return 'source.js' in self.current_scope()

    def in_coffee(self):
        return 'source.coffee' in self.current_scope()

