#!/usr/bin/env python3

# Copyright 2018 European Centre for Medium-Range Weather Forecasts (ECMWF)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.
import io
import os.path

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


version = "0.5.1"
setuptools.setup(
    name="rbase",
    # version=version,
    author="Dongdong Kong",
    author_email="kongdd.sysu@gmail.com",
    license="Apache 2.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "xarray",
        "matplotlib", 
        "metpy", 
        "PyPDF2", "PIL"
    ],
    zip_safe=True,
)
