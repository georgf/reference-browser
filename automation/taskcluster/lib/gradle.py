# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function
import json
import subprocess

from lib.variant import Variant


def get_debug_variants():
    print("Fetching build variants from gradle")
    output = _run_gradle_process('printBuildVariants')
    content = _extract_content_from_command_output(output, prefix='variants: ')
    variants = json.loads(content)

    if len(variants) == 0:
        raise ValueError("Could not get build variants from gradle")

    print("Got variants: {}".format(variants))
    return [Variant(variant_dict['name'], variant_dict['abi'], variant_dict['isSigned'],
                    variant_dict['buildType'])
            for variant_dict in variants
            if variant_dict['buildType'] == 'debug']


def get_geckoview_versions():
    print("Fetching geckoview version from gradle")
    output = _run_gradle_process('printGeckoviewVersions')
    nightly_version = _extract_content_from_command_output(output, prefix='nightly: ')
    nightly_version = nightly_version.strip('"')
    print('Got nightly version: "{}"'.format(nightly_version))
    return nightly_version


def _run_gradle_process(gradle_command):
    process = subprocess.Popen(["./gradlew", "--no-daemon", "--quiet", gradle_command], stdout=subprocess.PIPE)
    output, err = process.communicate()
    exit_code = process.wait()

    if exit_code is not 0:
        print("Gradle command returned error: {}".format(exit_code))

    return output


def _extract_content_from_command_output(output, prefix):
    variants_line = [line for line in output.split('\n') if line.startswith(prefix)][0]
    return variants_line.split(' ', 1)[1]
