# Copyright © 2020 Hashmap, Inc
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
import argparse
from pathlib import Path

from trainingopz.builders_and_generators.director import Director

testing_path = '../tests/ml_qookeys'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process the build and deploy an ML training process.')

    parser.add_argument('--project_path', '-p',
                        default=testing_path,
                        help='Path noting the root of the application.')

    args = parser.parse_args()

    args.project_path = str(Path(args.project_path).resolve())

    director = Director(project_path=args.project_path)

    director.build_and_run()
