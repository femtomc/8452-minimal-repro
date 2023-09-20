# Copyright 2022 MIT Probabilistic Computing Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import nox


try:
    from nox_poetry import Session
    from nox_poetry import session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None

package = "minimal-repro"
python_version = "3.11"
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = ("lint", "build")


@session(python=python_version)
def lint(session: Session) -> None:
    session.run_always("poetry", "install", external=True)
    session.install(
        "isort", "black[jupyter]", "autoflake8", "flake8", "docformatter[tomli]"
    )

    # Source
    session.run("isort", "8452_minimal_repro")
    session.run("black", "8452_minimal_repro")
    session.run("docformatter", "--in-place", "--recursive", "8452_minimal_repro")
    session.run(
        "autoflake8", "--in-place", "--recursive", "--exclude", "__init__.py", "8452_minimal_repro"
    )
    session.run("flake8", "8452_minimal_repro")


@session(python=python_version)
def build(session):
    session.run_always(
        "poetry",
        "install",
        external=True,
    )
    session.run("poetry", "build")
