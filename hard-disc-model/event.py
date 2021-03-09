# MIT License
# -----------

# Copyright (c) 2021 Sorn Zupanic Maksumic (https://www.usn.no)
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
class Event:
    def __init__(self, time, i, j):
        self.time = time
        self.i = i
        self.j = j
        if i is not None:
            self.i_cc = self.i.cc
        if j is not None:
            self.j_cc = self.j.cc

    def invalid(self):
        invalid_i = self.i is not None and self.i_cc != self.i.cc
        invalid_j = self.j is not None and self.j_cc != self.j.cc
        if invalid_i or invalid_j:
            return True
        return False

    def __lt__(self, other):
        return self.time < other.time